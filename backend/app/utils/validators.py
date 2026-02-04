import re
from datetime import date

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class ValidationError(Exception):
    pass

def parse_bool(val):
    if isinstance(val, bool): return val
    if isinstance(val, str): return val.lower() in ("1", "true", "yes", "on")
    if isinstance(val, int): return val == 1
    return False

def parse_date(val):
    if val in (None, ""): return None
    if isinstance(val, date): return val
    return date.fromisoformat(val)  # raises ValueError if invalid

def validate_create(body: dict) -> dict:
    # Required
    for key in ("first_name", "last_name", "email"):
        if not body.get(key):
            raise ValidationError(f"{key} is required")

    # Email
    if not EMAIL_RE.match(body["email"]):
        raise ValidationError("email is invalid")

    # Lengths
    if len(body["first_name"]) > 100: raise ValidationError("first_name too long")
    if len(body["last_name"]) > 100: raise ValidationError("last_name too long")
    if body.get("phone") and len(body["phone"]) > 20: raise ValidationError("phone too long")

    # Salary
    salary = body.get("salary")
    if salary in (None, ""):
        salary = None
    else:
        salary = float(salary)
        if salary < 0: raise ValidationError("salary must be >= 0")

    # Date
    date_hired = parse_date(body.get("date_hired"))

    return {
        "first_name": body["first_name"].strip(),
        "last_name": body["last_name"].strip(),
        "email": body["email"].strip().lower(),
        "phone": body.get("phone"),
        "department": body.get("department"),
        "title": body.get("title"),
        "salary": salary,
        "date_hired": date_hired,
        "is_active": parse_bool(body.get("is_active", True)),
    }

def validate_update(body: dict) -> dict:
    clean = {}
    if "first_name" in body:
        if not body["first_name"]: raise ValidationError("first_name cannot be empty")
        if len(body["first_name"]) > 100: raise ValidationError("first_name too long")
        clean["first_name"] = body["first_name"].strip()

    if "last_name" in body:
        if not body["last_name"]: raise ValidationError("last_name cannot be empty")
        if len(body["last_name"]) > 100: raise ValidationError("last_name too long")
        clean["last_name"] = body["last_name"].strip()

    if "phone" in body:
        if body["phone"] and len(body["phone"]) > 20: raise ValidationError("phone too long")
        clean["phone"] = body["phone"]

    if "department" in body: clean["department"] = body["department"]
    if "title" in body: clean["title"] = body["title"]

    if "salary" in body:
        if body["salary"] in (None, ""):
            clean["salary"] = None
        else:
            s = float(body["salary"])
            if s < 0: raise ValidationError("salary must be >= 0")
            clean["salary"] = s

    if "date_hired" in body:
        clean["date_hired"] = parse_date(body["date_hired"])

    if "is_active" in body:
        clean["is_active"] = parse_bool(body["is_active"])

    return clean