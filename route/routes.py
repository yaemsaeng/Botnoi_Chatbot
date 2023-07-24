from fastapi import APIRouter
from config.db import collection
import firebase_admin
from firebase_admin import credentials, storage
import base64
from model.models import insert_base64,update_chat_name
import requests
from datetime import datetime

Router = APIRouter()

cred = credentials.Certificate("./firebase/chatbotnoipdf-firebase-adminsdk-kqkcv-6855ab9086.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'chatbotnoipdf.appspot.com'})
bucket = storage.bucket()

@Router.get("/")
def read_root():
    return  "Hello Welcome to my Chatbot PDF"

@Router.post("/insert_new_chat", tags=["new chat"])
async def create_upload_file(data: insert_base64,customer_id:str,chat_name:str):
    # ดีโค้ดไฟล์จาก base64 เป็นไฟล์ PDF
    file_base64 = data.base64
    file_data = base64.b64decode(file_base64)
    
    # อัปโหลดไฟล์ PDF เข้าสู่ Firebase Storage
    randoms = file_base64[11 : 21]
    
    blob = bucket.blob(f"pdf/{randoms}.pdf")  #f" " คือ วิธีการสร้างสตริงที่อนุญาตให้แทรกค่าของตัวแปรหรือนิพจน์ลงในสตริงได้อย่างสะดวก ด้วยการใช้เครื่องหมาย {}
    blob.upload_from_string(file_data, content_type='application/pdf')
    
    # กำหนดสิทธิ์ในการเข้าถึงไฟล์ใน Firebase Storage ให้เป็นสาธารณะ
    blob.make_public()

    url = blob.public_url

    get_next_chat_id = collection.count_documents({}) + 1 ## เป็นการนับจำนวน documents ใน database เพื่อให้ chat id สามารถ generat ขึ้นมาเองได้โดยไม่ต้อง

    new_chat = {
        "customer_id": customer_id,
        "chat_id" : get_next_chat_id,
        "chat_name": chat_name,
        "chat_history": {},
        "pdf_url": url,
        "isWaiting": "false",
    }

    collection.insert_one(dict(new_chat))
    
    return new_chat
    

@Router.get("/chat_gpt_response", tags=["chat_bot"])
async def get_chat_response(chat_id:int ,chat_name : str ,query: str, customer_id: str):
    url = f"https://mekhav-2e2xbtpg2q-uc.a.run.app/chatgptresponse?query={query}&customer_id={customer_id}"
    response = requests.get(url)
    json_data = response.json()
    

    # สร้างเวลาปัจจุบัน
    current_timestamp = datetime.now().isoformat()
    # ส่วนที่ต้องการเพิ่ม
    chat_history_update = {
        "message_user":query, #เก็บเป็นค่า input ของผู้ใช้
        "message_bot": json_data, #เก็บเป็นค่าที่ chat ตอบกับมา
        "timestamp": current_timestamp
    }
    document = collection.find_one({"customer_id": customer_id,"chat_id":chat_id,"chat_name": chat_name})
    if document:#ถ้ามีข้อมูล
        # หาดัชนีใหม่ที่ต้องการสร้าง
        new_index = str(len(document.get("chat_history", {})))

        # อัปเดตเอกสาร
        result = collection.update_one(
            {"customer_id": customer_id,"chat_id":chat_id,"chat_name": chat_name},
            {"$set": {"chat_history." + new_index: chat_history_update}}
        )
    
    return json_data

@Router.get("/all_chat_name", tags=["all_chat_name"])
async def all_chat_histoy(customer_id: str):
    # ดึงข้อมูลทั้งหมดจากเอกสารที่มี customer_id เป็น "1234"
    result = collection.find({"customer_id": customer_id}, {"chat_name": 1})

    # สร้างรายการว่างเพื่อเก็บ chat_history
    all_chat_name = []

    # วนลูปผลลัพธ์และเพิ่ม chat_history เข้าไปในรายการ
    for doc in result:
        chat_history = doc.get("chat_name")
        all_chat_name.append(chat_history)

    return {"all_chat_name": all_chat_name}


@Router.get("/show_chat_history", tags=["show_chat_history"])
async def all_chat_histoy(customer_id: str,chat_id:int,chat_name:str):
    result = collection.find({"customer_id": customer_id, "chat_id":chat_id, "chat_name": chat_name})

    show_chat_history = []

    for doc in result:
        chat_history = doc.get("chat_history")
        show_chat_history.append(chat_history)

    return show_chat_history

@Router.put("/update_chat_name", tags=["data_update"])
async def update_chat_name(data:update_chat_name,customer_id: str,chat_id: int,chat_name:str):
    collection.find_one_and_update(
        {
            "customer_id": customer_id,
            "chat_id":chat_id,
            "chat_name": chat_name
        }, 
        {
         "$set": dict(data)
        })

@Router.delete("/delete" ,tags=["data_delete"])
async def delete(customer_id: str,chat_id:int,chat_name:str):
    collection.find_one_and_delete({"customer_id": customer_id, "chat_name": chat_name,"chat_id":chat_id})
    

