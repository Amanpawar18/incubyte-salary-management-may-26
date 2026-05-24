from fastapi import HTTPException

from app.employees.repository import EmployeeRepository
from app.employees.schemas import EmployeeCreate, EmployeePage, EmployeeRead


class EmployeeService:
    def __init__(self, repository: EmployeeRepository) -> None:
        self.repo = repository

    def create(self, data: EmployeeCreate) -> EmployeeRead:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=409, detail="An employee with this email already exists")
        employee = self.repo.create(data)
        return EmployeeRead.model_validate(employee)

    def get_by_id(self, employee_id: int) -> EmployeeRead:
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead.model_validate(employee)

    def list_paginated(
        self,
        page: int,
        page_size: int,
        name: str | None,
        country: str | None,
    ) -> EmployeePage:
        items, total = self.repo.get_paginated(page, page_size, name, country)
        return EmployeePage(
            items=[EmployeeRead.model_validate(e) for e in items],
            total=total,
            page=page,
            page_size=page_size,
        )
