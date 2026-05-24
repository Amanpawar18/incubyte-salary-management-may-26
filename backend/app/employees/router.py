from fastapi import APIRouter, Depends, Query
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


@router.get("/metrics")
def get_metrics(service: EmployeeService = Depends(get_service)):
    return {"data": service.get_metrics().model_dump()}


@router.get("/{employee_id}")
def get_employee(employee_id: int, service: EmployeeService = Depends(get_service)):
    return {"data": service.get_by_id(employee_id).model_dump()}


@router.put("/{employee_id}")
def update_employee(employee_id: int, data: EmployeeCreate, service: EmployeeService = Depends(get_service)):
    return {"data": service.update(employee_id, data).model_dump()}


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, service: EmployeeService = Depends(get_service)):
    service.delete(employee_id)


@router.get("")
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    name: str | None = None,
    country: str | None = None,
    service: EmployeeService = Depends(get_service),
):
    result = service.list_paginated(page, page_size, name, country)
    return {"data": result.model_dump()}
