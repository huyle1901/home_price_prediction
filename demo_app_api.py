from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import json

from fastapi.middleware.cors import CORSMiddleware



# Load model và danh sách các cột
with open('model_predict_house_price.pickle', 'rb') as file:
    model = pickle.load(file)

# Load danh sách các cột từ JSON
with open('columns.json', 'r') as file:
    data_columns = json.load(file)["data_columns"]

# Khởi tạo ứng dụng FastAPI
app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

# Cấu hình CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Cho phép frontend (Live Server) truy cập
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, ...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# Lớp định nghĩa input
class HouseData(BaseModel):
    location: str
    sqft: float
    bath: int
    bhk: int

@app.post("/predict")
def predict_price(data: HouseData):
    # Kiểm tra nếu location không hợp lệ
    if data.location.lower() not in data_columns:
        raise HTTPException(status_code=400, detail="Invalid location")

    # Tạo vector đầu vào (số lượng cột bằng với số cột trong mô hình)
    x = np.zeros(len(data_columns))

    # Gán giá trị cho các cột đầu vào
    x[0] = data.sqft  # Cột 'total_sqft'
    x[1] = data.bath  # Cột 'bath'
    x[2] = data.bhk   # Cột 'bhk'

    # Tìm chỉ số của cột location và đặt giá trị 1
    location_index = data_columns.index(data.location.lower())
    x[location_index] = 1

    # Dự đoán giá nhà
    predicted_price = model.predict([x])[0]

    # Trả về giá trị dự đoán
    return {"predicted_price": predicted_price}


@app.get("/locations")
def get_locations():
    # Lấy danh sách các vị trí (loại bỏ các cột không phải 'location')
    valid_locations = data_columns[3:]  # Các cột 'location' bắt đầu từ index 3
    return {"locations": valid_locations}