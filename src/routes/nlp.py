from fastapi import FastAPI, APIRouter,Depends ,UploadFile ,status ,Request,File
from fastapi.responses import JSONResponse
from schema.nlp import PushRequest
from models import ProjectModel
from models.enums import Responsesignal
from controller import NlpController
from models.ChunkModel import ChunkModel

import logging

logger  = logging.getLogger("uvicorn.error")

nlp_router  = APIRouter(prefix="/api/v1/nlp" , tags=["api_v1" , "nlp"])

@nlp_router.post("/index/push/{project_id}")
async def index_project(request:Request , project_id :str ,push_request:PushRequest ):
    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)
    chunk_model = await ChunkModel.create_instance(dp_client=request.app.state.dp_client)
    project = await project_model.get_project_create_one(
        project_id=project_id
    )
    nlp_controller = NlpController(vectordb_client = request.app.vectordb_client, generation_client = request.app.generation_client, embedding_client = request.app.embedding_client)
    
    page_no= 1
    is_finished=False
    while not is_finished:
        page_chunks = chunk_model.get_all_project_chunks(project_id =project.id , page_no=page_no)
        if not page_chunks or len(page_chunks)==0:
            is_finished=True
            break
        page_no+=1
        
        is_inserted = nlp_controller.index_into_vector_db(project=project , chunk=page_chunks,do_reset=PushRequest.do_reset)
        if not is_inserted:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={
                                    "signal":Responsesignal.inserting_into_vectorDB_error.value

                                })
    
    return JSONResponse( content={
                            "signal":Responsesignal.inserting_into_vectorDB_success.value,
                            "inserted pages count": page_no
                        })

        