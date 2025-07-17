from .BaseController import BaseController
from fastapi import UploadFile, Depends
from models import Responsesignal
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
    def get_project_path(self, project_id):
        project_path = os.path.join(self.filepath, project_id)

        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return project_path