from sqlmodel import Session, col, func, select

from app.employees.schemas import EmployeeCreate
from app.models import Employee


class EmployeeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.model_dump())
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_by_email(self, email: str) -> Employee | None:
        return self.session.exec(select(Employee).where(Employee.email == email)).first()

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.session.get(Employee, employee_id)

    def update(self, employee: Employee, data: EmployeeCreate) -> Employee:
        for field, value in data.model_dump().items():
            setattr(employee, field, value)
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_paginated(
        self,
        page: int,
        page_size: int,
        name: str | None = None,
        country: str | None = None,
    ) -> tuple[list[Employee], int]:
        query = select(Employee)
        count_query = select(func.count()).select_from(Employee)

        if name:
            query = query.where(col(Employee.full_name).contains(name))
            count_query = count_query.where(col(Employee.full_name).contains(name))
        if country:
            query = query.where(func.lower(Employee.country) == func.lower(country))
            count_query = count_query.where(func.lower(Employee.country) == func.lower(country))

        total = self.session.exec(count_query).one()
        offset = (page - 1) * page_size
        items = list(self.session.exec(query.order_by(Employee.id).offset(offset).limit(page_size)).all())
        return items, total
