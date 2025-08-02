from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader
from models.enums import Processingextension
from langchain_text_splitters import RecursiveCharacterTextSplitter
class ProcessController(BaseController):
    """
    Controller for managing processes.
    Inherits from BaseController to utilize common functionalities.
    """
    def __init__(self , project_id : str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=self.project_id)


    def get_file_extension (self, file_id:str):
        extension = os.path.splitext(file_id)[-1]
        return extension if extension else None



    def get_file_loader(self , file_id:str):
        #file_id = file_id.strip().replace('\n', '').replace('\r', '')
        #file_id = os.path.normpath(file_id)
        file_ext = self.get_file_extension(file_id=file_id)

        file_path = os.path.normpath(os.path.join(self.project_path, file_id))
        if not os.path.exists(file_path):
            return None

        if file_ext == Processingextension.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_ext == Processingextension.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {file_ext}")




    def get_file_content(self, file_id: str):
        """
        Retrieves the content of a file based on its ID.
        :param file_id: The ID of the file to retrieve.
        :return: The content of the file.
        """
        loader = self.get_file_loader(file_id=file_id)
        if not loader:
            return None
      
        return loader.load()

    def file_content_processing(self , file_content : list ,file_id : str , chunk_size : int  , overlab_size :int ):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlab_size,
            length_function=len
            )
        if file_content and isinstance(file_content[0], str):
            file_content_text = file_content
            file_content_metadata = [{} for _ in file_content]
        else:
            file_content_text = [rec.page_content for rec in file_content]
            file_content_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
        )

        return chunks