from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    date_of_birth: str
    email: EmailStr
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None

    @field_validator('date_of_birth', 'enrollment_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
