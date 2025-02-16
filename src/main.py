import uvicorn
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uuid

app = FastAPI()

# Temporary storage (replace with database later)
phone_numbers = {}

# Pydantic model for validation
class PhoneNumber(BaseModel):
    name: str
    number: str  # Ensure it's a string to keep leading zeros

@app.get("/")
def root():
    return {"message": "Hello, FastAPI - Phone API"}

# Get all phone numbers
@app.get("/phones")
def get_all_phones():
    return phone_numbers

# Get phone number by ID
@app.get("/phone/{phone_id}")
def get_phone(phone_id: str):
    if phone_id not in phone_numbers:
        return {"error": "Phone number not found"}
    return {"id": phone_id, "data": phone_numbers[phone_id]}

# Add a new phone number
@app.post("/phone")
def add_phone(phone: PhoneNumber = Body()):
    phone_id = str(uuid.uuid4())  # Generate a unique ID
    phone_numbers[phone_id] = phone.model_dump()
    return {"message": "Phone number added", "id": phone_id, "data": phone.model_dump()}

# Update a phone number
@app.put("/phone/{phone_id}")
def update_phone(phone_id: str, new_phone: PhoneNumber = Body()):
    if phone_id not in phone_numbers:
        return {"error": "Phone number not found"}
    phone_numbers[phone_id] = new_phone.model_dump()
    return {"message": "Phone number updated", "id": phone_id, "data": new_phone.model_dump()}

# Delete a phone number
@app.delete("/phone/{phone_id}")
def delete_phone(phone_id: str):
    if phone_id not in phone_numbers:
        return {"error": "Phone number not found"}
    del phone_numbers[phone_id]
    return {"message": "Phone number deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5000)
