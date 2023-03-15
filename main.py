from uuid import UUID, uuid4
import phonenumbers
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel, validator, EmailStr, Field

app = FastAPI()


class Contact(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    name: str = ...
    phone: str
    email: EmailStr
    notes: str = ''

    @validator('phone')
    def validate_phone(cls, v):
        try:
            p = phonenumbers.parse(v, 'IL')
            if phonenumbers.is_valid_number(p):
                return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            raise ValueError('Invalid phone number')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError('Invalid phone number')


contacts = {}


def search_by_email(email):
    return [c for c in contacts.values() if c.email == email]


def search_by_phone(phone):
    return [c for c in contacts.values() if c.phone == phone]


def search_by_email_or_phone(email, phone):
    return [c for c in contacts.values() if c.email == email or c.phone == phone]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/contacts")
def all_contacts():
    return contacts


@app.post("/contacts")
def create_contact(contact: Contact):
    if search_by_email_or_phone(contact.email, contact.phone):
        raise HTTPException(status_code=400, detail="Contact already exists")

    contacts[contact.uuid] = contact
    return contact


@app.get("/contacts/{contact_id}")
def read_contact(contact_id: int):
    return contacts[contact_id]


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: Contact):
    contacts[contact_id] = contact
    return contact


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    del contacts[contact_id]
    return "Deleted"


handler = Mangum(app, lifespan="off")
