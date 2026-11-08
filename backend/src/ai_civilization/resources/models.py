"""Resource contracts: conservation is enforced by validators, not agents."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Material(BaseModel):
    """A material definition."""

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    unit: str = Field(default="unit")


class StockEntry(BaseModel):
    """Quantity of a material held by an owner."""

    owner_id: str = Field(min_length=1)
    material_id: str = Field(min_length=1)
    quantity: float = Field(ge=0.0)


class Transfer(BaseModel):
    """A proposed transfer. Validators must check conservation."""

    from_owner: str
    to_owner: str
    material_id: str = Field(min_length=1)
    quantity: float = Field(gt=0.0)
