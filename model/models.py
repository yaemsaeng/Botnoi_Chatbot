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

class insert_chat_name(BaseModel):
    customer_id: str
    chat_name: str
    chat_history: dict = {}

    class Config:
         schema_extra = {
                "example" : {
                    "customer_id" : "input_customer_id",
                    "chat_name":"input_chat_name",
                }
            }

class update_chat_name(BaseModel):
    chat_name: str
    
    class Config:
        schema_extra = {
            "example" : {
                "chat_name":"input_new_chat_name",
            }
        }
    