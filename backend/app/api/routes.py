from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status, Request
from app.services.employee_service import (
    create_employee, get_employee_by_id, list_employees,
    update_employee, delete_employee
)
from app.utils.validators import validate_create, validate_update, ValidationError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("")
def get_employees(
    q: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    order_by: str = Query("id ASC")
):
    employees, total = list_employees(q, department, is_active, limit, offset, order_by)
    return {"data": [e.to_dict() for e in employees], "total": total, "limit": limit, "offset": offset}

@router.get("/{emp_id}")
def get_employee(emp_id: int):
    emp = get_employee_by_id(emp_id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp.to_dict()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee_route(request: Request):
    body = await request.json()
    logger.info(f"POST /employees request body: {body}")
    try:
        payload = validate_create(body)
        logger.info(f"Validation passed, payload: {payload}")
        emp = create_employee(payload)
        logger.info(f"Employee created successfully: {emp.to_dict()}")
        return emp.to_dict()
    except ValidationError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("create_employee failed")
        # In development, surface the DB error to help debugging. In production, hide details.
        if "Duplicate" in str(e) or "Duplicate entry" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{emp_id}")
async def update_employee_route(emp_id: int, request: Request):
    body = await request.json()
    try:
        payload = validate_update(body)
        emp = update_employee(emp_id, payload)
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")
        return emp.to_dict()
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.delete("/{emp_id}")
def delete_employee_route(emp_id: int):
    ok = delete_employee(emp_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"deleted": True}
