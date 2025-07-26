import re
from fastapi import FastAPI, APIRouter,Depends ,UploadFile ,status ,Request,File
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controller import dataController , ProjectController ,BaseController ,ProcessController
from models import Responsesignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
import logging
from .schema.data import process_request
import aiofiles
from models.schema import DataChunck

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix= "/api/v1/data" , tags=["api_v1","data"])

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
        
    
    project_model = ProjectModel(dp_client=request.app.state.dp_client)

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

    return JSONResponse(
            content={
                "signal": Responsesignal.file_uploaded_successfully.value,
                "file_id": file_id,
            }
        )

@data_router.post("/process/{project_id}")
async def process_data(request: Request,project_id: str, process_request: process_request):
    File_id  = process_request.file_id
    CHUNK_SIZE = process_request.chunksize
    OVERLAP_SIZE = process_request.overlab_size
    do_reset= process_request.do_reset
    


    project_model = ProjectModel(dp_client=request.app.state.dp_client)

    project = await project_model.get_project_create_one(
        project_id=project_id
    )

    process_controller = ProcessController(project_id=project_id)
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

    chunk_model = ChunkModel(dp_client=request.app.state.dp_client)
    if do_reset == 1 :
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project_id)
    
    inserted_count = await chunk_model.insert_many_chunks(chunk=chunk_recs)
    return JSONResponse({
        "content":Responsesignal.processing_successful.value,
        "inserted_count":inserted_count
    })