import re
import os
import logging
import aiofiles

from fastapi import FastAPI, APIRouter,Depends ,UploadFile ,status ,Request,File
from fastapi.responses import JSONResponse

from .schema.data import process_request
from helpers.config import get_settings , Settings
from controller import dataController , ProjectController ,BaseController ,ProcessController
from models.enums import Responsesignal , Assist_type_enum
from models.schema import DataChunck , Assist
from models import ProjectModel,ChunkModel,AssistModel



logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix= "/api/v1/data" , tags=["api_v1","data"])

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
        
    
    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)

    project = await project_model.get_project_create_one(
        project_id=project_id
    )

    # validate the file properties
    data_controller = dataController()

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.file_default_chunk_size):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": Responsesignal.file_upload_failed.value
            }
        )

    assist_model = await AssistModel.create_instance(dp_client=request.app.state.dp_client)

    Assist_resourses = Assist(
        assist_project_id = project.id,
        assist_type = Assist_type_enum.File.value ,
        assist_name = file_id,
        assist_size = int(os.path.getsize(file_path))
        )
    
    assist_rec = await assist_model.create_assist(assist=Assist_resourses)

    return JSONResponse(
            content={
                "signal": Responsesignal.file_uploaded_successfully.value,
                "file_id": str(assist_rec.id),
            }
        )

@data_router.post("/process_file/{project_id}")
async def process_file(request: Request,project_id: str, process_request: process_request):
    File_id  = process_request.file_id
    CHUNK_SIZE = process_request.chunksize
    OVERLAP_SIZE = process_request.overlab_size
    do_reset= process_request.do_reset
    


    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)

    project = await project_model.get_project_create_one(
        project_id=project_id
    )
    assist_model = await AssistModel.create_instance(dp_client=request.app.state.dp_client)

    assist_records = await assist_model.get_all_project_assists(assist_project_id=project.id, assist_type=Assist_type_enum.File.value)

    file_ids = [ # Extract file IDs from assist records
        rec.assist_name
        for rec in assist_records if rec.assist_size > 0
        ]
    if File_id not in file_ids: # Check if the provided file ID exists
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "signal": Responsesignal.file_not_found.value
            }
        )

    process_controller = ProcessController(project_id=project_id)
    file_contents = process_controller.get_file_content(file_id=File_id)
    if file_contents is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "signal": Responsesignal.file_not_found.value
            }
        )

    file_chunks  = process_controller.file_content_processing(file_content= file_contents,file_id= File_id,chunk_size=CHUNK_SIZE ,overlab_size= OVERLAP_SIZE)

    if file_chunks == []:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": Responsesignal.processing_failed.value
            }
        )
    chunk_recs = [
        DataChunck(
            chunck_order=i+1,
            chunck_project_id=project.id,
            chunck_text=chunk.page_content,
            chunck_metadata= chunk.metadata
                    
            )
        for i,chunk in enumerate(file_chunks) if chunk is not None
        ]

    chunk_model = await ChunkModel.create_instance(dp_client=request.app.state.dp_client)
    deleted_count= 0
    if do_reset == 1 :
        deleted_count = await chunk_model.reset()
    
    inserted_count = await chunk_model.insert_many_chunks(chunk=chunk_recs)
    return JSONResponse({
        "content":Responsesignal.processing_successful.value,
        "inserted_count":inserted_count,
        "deleted_count": deleted_count
    })


@data_router.post("/process_all_files/{project_id}")
async def process_all_files(request:Request,project_id: str, process_request: process_request):
    file_id = process_request.file_id
    if file_id is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": Responsesignal.donot_insert_file_id.value
            }
        )
    CHUNK_SIZE = process_request.chunksize
    OVERLAP_SIZE = process_request.overlab_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(dp_client=request.app.state.dp_client)
    project = await project_model.get_project_create_one(project_id=project_id)
    process_controller = ProcessController(project_id=project_id)
    assist_model = await AssistModel.create_instance(dp_client=request.app.state.dp_client)

    assist_records = await assist_model.get_all_project_assists(assist_project_id=project.id, assist_type=Assist_type_enum.File.value)

    file_ids = [ # Extract file IDs from assist records
        rec.assist_name
        for rec in assist_records if rec.assist_size > 0
        ]

    if not file_ids: # No files found for processing
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "signal": Responsesignal.No_files_found.value
            }
        )
    chunk_model = await ChunkModel.create_instance(dp_client=request.app.state.dp_client)

    num_rec = 0
    inserted_count = 0
    deleted_count = 0
    if do_reset == 1 :
        deleted_count += await chunk_model.reset()

    for File_id in file_ids: # Iterate through each file ID and process it
        num_rec += 1
        file_contents = process_controller.get_file_content(file_id=File_id)
        file_chunks  = process_controller.file_content_processing(file_content= file_contents,file_id= File_id,chunk_size=CHUNK_SIZE ,overlab_size= OVERLAP_SIZE)

        if file_chunks == []:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": Responsesignal.processing_failed.value
                }
            )
        chunk_recs = [
            DataChunck(
                chunck_order=i+1,
                chunck_project_id=project.id,
                chunck_text=chunk.page_content,
                chunck_metadata= chunk.metadata
                        
                )
            for i,chunk in enumerate(file_chunks) if chunk is not None
            ] 
        inserted_count += await chunk_model.insert_many_chunks(chunk=chunk_recs)

    return JSONResponse({
        "content":Responsesignal.processing_successful.value,
        "inserted_count":inserted_count,
        "deleted_count": deleted_count,
        "processed_files": num_rec,
        "file_ids_count": len(file_ids)

    })

    
