from fastapi import FastAPI, APIRouter,Depends ,UploadFile ,status ,Request,File
from typing import Optional
from fastapi.responses import JSONResponse
from .schema.nlp import PushRequest ,  SearchRequest
from models import ProjectModel
from models.enums import Responsesignal
from controller import NlpController
from models.ChunkModel import ChunkModel

import logging

logger  = logging.getLogger("uvicorn.error")

nlp_router  = APIRouter(prefix="/api/v1/nlp" , tags=["api_v1" , "nlp"])

@nlp_router.post("/index/push/{project_id}")
async def index_project(request:Request , project_id :str ,push_request:Optional[PushRequest] = None ):
    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)
    chunk_model = await ChunkModel.create_instance(dp_client=request.app.state.dp_client)
    project = await project_model.get_project_create_one(
        project_id=project_id
    )
    nlp_controller = NlpController(vectordb_client = request.app.state.vectordb_client,
                                  generation_client = request.app.state.generation_client,
                                 embedding_client = request.app.state.embedding_client,
                                 template_parser=request.app.state.template_client)
    
    page_no= 1
    is_finished=False
    idx=0
    while not is_finished:
        page_chunks = await chunk_model.get_all_project_chunks(project_id =project.id , page_no=page_no)
        if not page_chunks or len(page_chunks)==0:
            is_finished=True
            break
        page_no+=1
        
        chunk_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)
        is_inserted = nlp_controller.index_into_vector_db(project=project , chunk=page_chunks,chunk_ids=chunk_ids,do_reset=push_request.do_reset if push_request else 0)
        if not is_inserted:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={
                                    "signal":Responsesignal.inserting_into_vectorDB_error.value

                                })
    
    return JSONResponse( content={
                            "signal":Responsesignal.inserting_into_vectorDB_success.value,
                            "inserted pages count": page_no,
                            "inserted chunks count": idx
                        })

@nlp_router.get("/index/info/{project_id}")
async def get_vector_db_info(request:Request , project_id :str):
    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)

    project = await project_model.get_project_create_one(
        project_id=project_id
    )

    nlp_controller = NlpController(vectordb_client = request.app.state.vectordb_client,
                                  generation_client = request.app.state.generation_client,
                                 embedding_client = request.app.state.embedding_client,
                                 template_parser=request.app.state.template_client)

    collection_info = nlp_controller.get_vector_dbcollection_info(project=project)
    
    return JSONResponse( content={
                            "signal":Responsesignal.vectorDB_info_retrieved.value,
                            "collection_info": collection_info
                        }) 
    

@nlp_router.post("/index/search/{project_id}")
async def search_vector_db(request:Request , project_id :str ,search_request :SearchRequest ):

    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)

    project = await project_model.get_project_create_one(
        project_id=project_id
    )

    nlp_controller = NlpController(vectordb_client = request.app.state.vectordb_client,
                                  generation_client = request.app.state.generation_client,
                                 embedding_client = request.app.state.embedding_client,
                                 template_parser=request.app.state.template_client)

    search_result = nlp_controller.search_by_vector(project=project , text=search_request.text , limit=search_request.limit)

    if not search_result or len(search_result)==0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={
                                "signal":Responsesignal.vectorDB_search_not_found.value
                            })

    return JSONResponse( content={
        "signal":Responsesignal.vectorDB_search_success.value,
        "results": search_result
        
        })

@nlp_router.post("/index/answer/{project_id}")
async def answer_QA(request:Request , project_id :str ,search_request :SearchRequest ):

    project_model =await ProjectModel.create_instance(dp_client=request.app.state.dp_client)

    project = await project_model.get_project_create_one(
        project_id=project_id
    )

    nlp_controller = NlpController(vectordb_client = request.app.state.vectordb_client,
                                  generation_client = request.app.state.generation_client,
                                 embedding_client = request.app.state.embedding_client,
                                 template_parser=request.app.state.template_client)

    answer,full_prompt,chat_history = nlp_controller.answer_rag_questions(project=project , query=search_request.text , limit=search_request.limit)

    if not answer or len(answer)==0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={
                                "signal":Responsesignal.Rag_answer_error.value
                            })

    return JSONResponse( content={
        "signal":Responsesignal.Rag_answer_success.value,
        "answer": answer,
        "full_prompt": full_prompt,
        "chat_history": chat_history
    })

        