from typing import List, Optional, Tuple
from mysql.connector import Error
from loguru import logger
from app.db.connection import get_conn
from app.models.employee import Employee

def _row_to_employee(row: dict) -> Employee:
    return Employee.from_row(row)

def create_employee(payload: dict) -> Employee:
    logger.info(f"Creating employee with payload: {payload}")
    conn = get_conn()
    try:
        with conn.cursor(dictionary=True) as cur:
            sql = """
            INSERT INTO employees
            (first_name,last_name,email,phone,department,title,salary,date_hired,is_active)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            vals = (
                payload["first_name"], payload["last_name"], payload["email"], payload.get("phone"),
                payload.get("department"), payload.get("title"), payload.get("salary"),
                payload.get("date_hired"), 1 if payload.get("is_active", True) else 0
            )
            logger.info(f"Executing SQL with values: {vals}")
            cur.execute(sql, vals)
            conn.commit()
            logger.info(f"Employee inserted, lastrowid: {cur.lastrowid}")
            new_id = cur.lastrowid
            return get_employee_by_id(new_id)
    except Error as e:
        logger.error(f"Database error during employee creation: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def get_employee_by_id(emp_id: int) -> Optional[Employee]:
    conn = get_conn()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
            row = cur.fetchone()
            return _row_to_employee(row) if row else None
    finally:
        conn.close()

def list_employees(
    q: Optional[str] = None,
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "id ASC",
) -> Tuple[List[Employee], int]:
    conn = get_conn()
    try:
        filters = []
        params = []

        if q:
            filters.append("(first_name LIKE %s OR last_name LIKE %s OR email LIKE %s)")
            like = f"%{q}%"
            params.extend([like, like, like])

        if department:
            filters.append("department = %s")
            params.append(department)

        if is_active is not None:
            filters.append("is_active = %s")
            params.append(1 if is_active else 0)

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        count_sql = f"SELECT COUNT(*) AS total FROM employees {where_clause}"
        data_sql = f"SELECT * FROM employees {where_clause} ORDER BY {order_by} LIMIT %s OFFSET %s"

        with conn.cursor(dictionary=True) as cur:
            cur.execute(count_sql, tuple(params))
            total = cur.fetchone()["total"]

            cur.execute(data_sql, tuple(params + [limit, offset]))
            rows = cur.fetchall()
            return ([_row_to_employee(r) for r in rows], total)
    finally:
        conn.close()

def update_employee(emp_id: int, payload: dict) -> Optional[Employee]:
    updates = []
    params = []
    for field, value in payload.items():
        updates.append(f"{field}=%s")
        params.append(value)

    if not updates:
        return get_employee_by_id(emp_id)

    params.append(emp_id)

    conn = get_conn()
    try:
        with conn.cursor(dictionary=True) as cur:
            sql = f"UPDATE employees SET {', '.join(updates)} WHERE id=%s"
            cur.execute(sql, tuple(params))
            conn.commit()
            return get_employee_by_id(emp_id)
    except Error:
        conn.rollback()
        raise
    finally:
        conn.close()

def delete_employee(emp_id: int) -> bool:
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
            conn.commit()
            return cur.rowcount > 0
    except Error:
        conn.rollback()
        raise
    finally:
        conn.close()