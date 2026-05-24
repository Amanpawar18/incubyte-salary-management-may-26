from fastapi import HTTPException

from app.employees.repository import EmployeeRepository
from app.employees.schemas import EmployeeCreate, EmployeeRead


class EmployeeService:
    def __init__(self, repository: EmployeeRepository) -> None:
        self.repo = repository

    def create(self, data: EmployeeCreate) -> EmployeeRead:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=409, detail="An employee with this email already exists")
        employee = self.repo.create(data)
        return EmployeeRead.model_validate(employee)
