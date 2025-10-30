"""Pydantic models for the FastAPI layer."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator


class ChartRequest(BaseModel):
    """Input payload for generating a chart."""

    day: int
    month: int
    year: int
    hour_branch: int
    gender: int
    name: Optional[str] = None
    solar_calendar: bool = True
    timezone: int = 7

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: int) -> int:
        if value not in (1, -1):
            raise ValueError("gender must be 1 (male) or -1 (female)")
        return value

    @field_validator("hour_branch")
    @classmethod
    def validate_hour_branch(cls, value: int) -> int:
        if value < 1 or value > 12:
            raise ValueError("hour_branch must be between 1 and 12")
        return value


class StarInfo(BaseModel):
    star_id: int
    name: str
    element: str
    category: int
    strength: Optional[str] = None
    direction: Optional[str] = None
    am_duong: Optional[int] = None
    trang_sinh: int = 0
    css_class: Optional[str] = None


class HouseInfo(BaseModel):
    house_number: int
    branch: str
    name: str
    element: str
    am_duong: int
    is_body_house: bool
    tuan_trung: bool = False
    triet_lo: bool = False
    major_period: Optional[int] = None
    minor_period: Optional[str] = None
    stars: List[StarInfo]


class ChartResponse(BaseModel):
    id: Optional[int]
    request: ChartRequest
    houses: List[HouseInfo]
    extra: Dict[str, Any]
