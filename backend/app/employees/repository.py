from sqlmodel import Session, col, func, select

from app.employees.schemas import CountryMetrics, DepartmentMetrics, EmployeeCreate, SalaryMetrics
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

    def delete(self, employee: Employee) -> None:
        self.session.delete(employee)
        self.session.commit()

    def update(self, employee: Employee, data: EmployeeCreate) -> Employee:
        for field, value in data.model_dump().items():
            setattr(employee, field, value)
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_metrics(self) -> SalaryMetrics:
        total = self.session.exec(select(func.count()).select_from(Employee)).one()
        avg = self.session.exec(select(func.avg(Employee.salary))).one()
        min_sal = self.session.exec(select(func.min(Employee.salary))).one()
        max_sal = self.session.exec(select(func.max(Employee.salary))).one()

        by_dept = self.session.exec(
            select(Employee.department, func.count(), func.avg(Employee.salary))
            .group_by(Employee.department)
            .order_by(Employee.department)
        ).all()

        by_country = self.session.exec(
            select(Employee.country, func.count(), func.avg(Employee.salary))
            .group_by(Employee.country)
            .order_by(Employee.country)
        ).all()

        return SalaryMetrics(
            total=total,
            average_salary=round(avg, 2) if avg else 0,
            min_salary=min_sal,
            max_salary=max_sal,
            by_department=[DepartmentMetrics(department=d, count=c, average_salary=round(a, 2)) for d, c, a in by_dept],
            by_country=[CountryMetrics(country=c, count=n, average_salary=round(a, 2)) for c, n, a in by_country],
        )

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
