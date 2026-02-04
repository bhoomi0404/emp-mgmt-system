from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Employee:
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    department: Optional[str]
    title: Optional[str]
    salary: Optional[float]
    date_hired: Optional[date]
    is_active: bool = True

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "title": self.title,
            "salary": float(self.salary) if self.salary is not None else None,
            "date_hired": self.date_hired.isoformat() if self.date_hired else None,
            "is_active": bool(self.is_active),
            "full_name": self.full_name,
        }

    @classmethod
    def from_row(cls, row: dict) -> "Employee":
        return cls(
            id=row.get("id"),
            first_name=row.get("first_name", ""),
            last_name=row.get("last_name", ""),
            email=row.get("email", ""),
            phone=row.get("phone"),
            department=row.get("department"),
            title=row.get("title"),
            salary=float(row["salary"]) if row.get("salary") is not None else None,
            date_hired=row.get("date_hired"),
            is_active=bool(row.get("is_active", 1)),
        )