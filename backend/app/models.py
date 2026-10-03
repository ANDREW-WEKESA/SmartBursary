from datetime import datetime, date
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, Text, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(40), default="")
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30), default="applicant")
    constituency: Mapped[str] = mapped_column(String(100), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    # Profile fields
    profile_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    national_id: Mapped[str] = mapped_column(String(100), default="")
    gender: Mapped[str] = mapped_column(String(20), default="")
    county: Mapped[str] = mapped_column(String(100), default="")
    sub_county: Mapped[str] = mapped_column(String(100), default="")
    address: Mapped[str] = mapped_column(Text, default="")
    guardian_name: Mapped[str] = mapped_column(String(160), default="")
    guardian_phone: Mapped[str] = mapped_column(String(40), default="")
    guardian_relationship: Mapped[str] = mapped_column(String(50), default="")
    # Educational details
    institution: Mapped[str] = mapped_column(String(180), default="")
    student_number: Mapped[str] = mapped_column(String(100), default="")
    course: Mapped[str] = mapped_column(String(180), default="")
    year_of_study: Mapped[str] = mapped_column(String(40), default="")
    admission_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Financial information
    monthly_household_income: Mapped[int] = mapped_column(Integer, default=0)
    household_size: Mapped[int] = mapped_column(Integer, default=1)
    # Profile documents
    has_national_id_doc: Mapped[bool] = mapped_column(Boolean, default=False)
    has_student_id_doc: Mapped[bool] = mapped_column(Boolean, default=False)
    has_admission_letter: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    applications: Mapped[list["Application"]] = relationship(back_populates="applicant")
    profile_documents: Mapped[list["ProfileDocument"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Bursary(Base):
    __tablename__ = "bursaries"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    eligibility: Mapped[str] = mapped_column(Text, default="")
    constituency: Mapped[str] = mapped_column(String(100), default="")
    amount_kes: Mapped[int] = mapped_column(Integer, default=0)
    show_amount: Mapped[bool] = mapped_column(Boolean, default=True)
    deadline: Mapped[date] = mapped_column(Date)
    required_documents: Mapped[str] = mapped_column(Text, default="[]")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("application_number", name="uq_application_number"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    application_number: Mapped[str] = mapped_column(String(40), index=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    bursary_id: Mapped[int] = mapped_column(ForeignKey("bursaries.id"), index=True)
    institution: Mapped[str] = mapped_column(String(180))
    student_number: Mapped[str] = mapped_column(String(100), index=True)
    national_id: Mapped[str] = mapped_column(String(100), default="")
    monthly_household_income: Mapped[int] = mapped_column(Integer, default=0)
    household_size: Mapped[int] = mapped_column(Integer, default=1)
    course: Mapped[str] = mapped_column(String(180), default="")
    year_of_study: Mapped[str] = mapped_column(String(40), default="")
    reason: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="Submitted", index=True)
    priority_score: Mapped[int] = mapped_column(Integer, default=0)
    financial_need: Mapped[str] = mapped_column(String(20), default="MEDIUM")
    education_need: Mapped[str] = mapped_column(String(20), default="MEDIUM")
    duplicate_risk: Mapped[str] = mapped_column(String(20), default="LOW")
    reviewer_comment: Mapped[str] = mapped_column(Text, default="")
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    applicant: Mapped[User] = relationship(back_populates="applications")
    bursary: Mapped[Bursary] = relationship()
    documents: Mapped[list["Document"]] = relationship(back_populates="application", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), index=True)
    document_type: Mapped[str] = mapped_column(String(180))
    original_filename: Mapped[str] = mapped_column(String(255))
    stored_filename: Mapped[str] = mapped_column(String(255), unique=True)
    content_type: Mapped[str] = mapped_column(String(120), default="application/octet-stream")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    verification_status: Mapped[str] = mapped_column(String(30), default="Pending")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    application: Mapped[Application] = relationship(back_populates="documents")

class ProfileDocument(Base):
    __tablename__ = "profile_documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    document_type: Mapped[str] = mapped_column(String(180))
    original_filename: Mapped[str] = mapped_column(String(255))
    stored_filename: Mapped[str] = mapped_column(String(255), unique=True)
    content_type: Mapped[str] = mapped_column(String(120), default="application/octet-stream")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship(back_populates="profile_documents")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    actor_name: Mapped[str] = mapped_column(String(160), default="System")
    action: Mapped[str] = mapped_column(String(180))
    entity_type: Mapped[str] = mapped_column(String(80), default="")
    entity_id: Mapped[str] = mapped_column(String(80), default="")
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    message: Mapped[str] = mapped_column(Text)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class EmailOTP(Base):
    __tablename__ = "email_otps"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), index=True)
    otp_code: Mapped[str] = mapped_column(String(6))
    purpose: Mapped[str] = mapped_column(String(50), default="registration")  # registration, password_reset
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
