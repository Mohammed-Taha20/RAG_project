from helpers.config import Settings , get_settings
class MyBaseModel:
    def __init__(self, dp_client:object):
        self.dp_client = dp_client
        self.settings: Settings = get_settings()
    
