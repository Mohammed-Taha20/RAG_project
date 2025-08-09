from helpers.config import get_settings, Settings
import os
import random
import string
class BaseController:
    """
    Base controller class that provides access to application settings.
    """
    def __init__(self):
        self.app_settings = get_settings()
        self.basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filepath = os.path.join(self.basepath, "assist" , "files")
        self.database_dir = os.path.join(self.basepath, "assist", "databases")

    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    #def get_db_path(self,db_name:str):
    #    db_dir = os.path.join(self.database_dir,db_name)
    #
    #    if not os.path.exists(db_dir):
    #        os.makedirs(db_dir)
    #
    #    return db_dir