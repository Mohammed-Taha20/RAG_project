from .MyBaseModel import MyBaseModel
from .schema import Project
from .enums.db_enum import DBEnum

class ProjectModel(MyBaseModel):
    def __init__(self, dp_client):
        super().__init__(dp_client)
        self.collection = self.dp_client[DBEnum.CollectionProjectName.value]

    async def create_project(self, project_data: Project):
        result = await self.collection.insert_one(project_data.dict(by_alias=True , exclude_unset= True))
        Project.id = result.inserted_id
        return Project

    async def get_project_create_one(self, project_id: str):
        project_data = await self.collection.find_one({"project_id": project_id})
        if project_data:
            return Project(**project_data)
        else : 
            project = Project(project_id=project_id)
            project = await self.create_project(project)
            return project

    async def get_all_projects(self, page_num = 1 , page_size =10):
        total_documents  = await self.collection.count_documents({})
        total_pages = (total_documents + page_size - 1) // page_size

        curses = self.collection.find().skip((page_num - 1) * page_size).limit(page_size)

        projects = []
        async for document in curses:
              projects.append(Project(**document))

        return projects, total_pages
        