"""Economy contracts (Phase 0 placeholders)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Offer(BaseModel):
    """A proposed trade offer."""

    offer_id: str = Field(min_length=1)
    maker_id: str = Field(min_length=1)
    give_material: str = Field(min_length=1)
    give_qty: float = Field(gt=0.0)
    want_material: str = Field(min_length=1)
    want_qty: float = Field(gt=0.0)


class Transaction(BaseModel):
    """An accepted trade, committed by the simulation."""

    tx_id: str = Field(min_length=1)
    offer_id: str = Field(min_length=1)
    taker_id: str = Field(min_length=1)
    tick: int = Field(ge=0)
