from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    phone: str = Field(default="", max_length=40)
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int; full_name: str; email: EmailStr; phone: str; role: str; profile_complete: bool
    model_config = ConfigDict(from_attributes=True)

class ProfileUpdateIn(BaseModel):
    date_of_birth: date | None = None
    national_id: str = ""
    gender: str = ""
    county: str = ""
    sub_county: str = ""
    address: str = ""
    guardian_name: str = ""
    guardian_phone: str = ""
    guardian_relationship: str = ""
    institution: str = ""
    student_number: str = ""
    course: str = ""
    year_of_study: str = ""
    admission_year: int | None = None
    monthly_household_income: int = Field(default=0, ge=0)
    household_size: int = Field(default=1, ge=1, le=50)

class ProfileDocumentOut(BaseModel):
    id: int; document_type: str; original_filename: str; size_bytes: int; uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProfileOut(BaseModel):
    id: int; full_name: str; email: EmailStr; phone: str
    profile_complete: bool
    date_of_birth: date | None; national_id: str; gender: str; county: str; sub_county: str; address: str
    guardian_name: str; guardian_phone: str; guardian_relationship: str
    institution: str; student_number: str; course: str; year_of_study: str; admission_year: int | None
    monthly_household_income: int; household_size: int
    has_national_id_doc: bool; has_student_id_doc: bool; has_admission_letter: bool
    profile_documents: list[ProfileDocumentOut]
    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserOut

class BursaryIn(BaseModel):
    name: str = Field(min_length=3, max_length=180)
    description: str = ""
    eligibility: str = ""
    amount_kes: int = Field(ge=0)
    deadline: date
    required_documents: list[str] = []
    active: bool = True

class BursaryOut(BaseModel):
    id: int; name: str; description: str; eligibility: str; amount_kes: int; deadline: date; required_documents: list[str]; active: bool

class ApplicationIn(BaseModel):
    bursary_id: int
    institution: str = Field(min_length=2, max_length=180)
    student_number: str = Field(min_length=2, max_length=100)
    national_id: str = ""
    monthly_household_income: int = Field(ge=0)
    household_size: int = Field(ge=1, le=50)
    course: str = ""
    year_of_study: str = ""
    reason: str = ""

class StatusIn(BaseModel):
    status: str
    reviewer_comment: str = ""

class DocumentOut(BaseModel):
    id: int; document_type: str; original_filename: str; size_bytes: int; verification_status: str; uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ApplicationOut(BaseModel):
    id: int; application_number: str; applicant_id: int; applicant_name: str; applicant_email: str; bursary_id: int; bursary_name: str; amount_kes: int; institution: str; student_number: str; national_id: str; monthly_household_income: int; household_size: int; course: str; year_of_study: str; reason: str; status: str; priority_score: int; financial_need: str; education_need: str; duplicate_risk: str; reviewer_comment: str; submitted_at: datetime; updated_at: datetime; documents: list[DocumentOut]


class StaffUserIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    role: str = Field(pattern="^(admin|reviewer)$")
