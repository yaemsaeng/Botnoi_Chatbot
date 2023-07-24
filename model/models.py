from typing import Optional
from pydantic import BaseModel

class insert_base64(BaseModel):
    base64 : Optional[str]

    class Config:
        schema_extra = {
            "example" : {
                "base64":"input_base64_text",
            }
        }

class update_chat_name(BaseModel):
    chat_name: str
    
    class Config:
        schema_extra = {
            "example" : {
                "modify_chat_name":"input_new_chat_name",
            }
        }
    
