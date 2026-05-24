from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.employees.repository import EmployeeRepository
from app.employees.schemas import EmployeeCreate
from app.employees.service import EmployeeService

router = APIRouter()


def get_service(session: Session = Depends(get_session)) -> EmployeeService:
    return EmployeeService(EmployeeRepository(session))


@router.post("", status_code=201)
def create_employee(data: EmployeeCreate, service: EmployeeService = Depends(get_service)):
    employee = service.create(data)
    return {"data": employee.model_dump()}
