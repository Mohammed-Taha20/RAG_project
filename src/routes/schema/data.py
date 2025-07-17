from pydantic import BaseModel
from typing import List, Optional

class process_request(BaseModel):
    file_id : str
    chunksize : Optional[int] = 200
    overlab_size : Optional[int] = 40
    do_reset : Optional[bool] = False
