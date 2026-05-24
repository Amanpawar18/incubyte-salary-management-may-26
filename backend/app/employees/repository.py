from sqlmodel import Session, select

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
