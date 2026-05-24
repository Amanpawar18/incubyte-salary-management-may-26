import re
from datetime import datetime

from pydantic import BaseModel, field_validator


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    department: str
    country: str
    salary: float
    email: str

    @field_validator("full_name", "job_title", "department", "country")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v

    @field_validator("salary")
    @classmethod
    def salary_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("must be greater than 0")
        return v

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("must be a valid email address")
        return v


class EmployeeUpdate(EmployeeCreate):
    pass


class EmployeeRead(BaseModel):
    id: int
    full_name: str
    job_title: str
    department: str
    country: str
    salary: float
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EmployeePage(BaseModel):
    items: list[EmployeeRead]
    total: int
    page: int
    page_size: int


class DepartmentMetrics(BaseModel):
    department: str
    count: int
    average_salary: float


class CountryMetrics(BaseModel):
    country: str
    count: int
    average_salary: float


class SalaryMetrics(BaseModel):
    total: int
    average_salary: float
    min_salary: float | None
    max_salary: float | None
    by_department: list[DepartmentMetrics]
    by_country: list[CountryMetrics]
