"""Item API for IT Release Readiness & Governance."""

from __future__ import annotations

import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

SERVICE_NAME = os.getenv("SERVICE_NAME", "it-release-readiness-governance-backend")

app = FastAPI(title=SERVICE_NAME, version="0.1.0")


class Health(BaseModel):
    """Payload returned by the liveness probe."""

    status: str
    service: str


class Item(BaseModel):
    """A single item."""

    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=120)


class ItemCreate(BaseModel):
    """Payload accepted when creating an item."""

    name: str = Field(min_length=1, max_length=120)


class ItemList(BaseModel):
    """Envelope so the response can grow without breaking clients."""

    items: list[Item]


_ITEMS: list[Item] = [Item(id=1, name="first item")]
_NEXT_ID = 2


@app.get("/health", response_model=Health)
def health() -> Health:
    """Liveness/readiness probe used by Docker and the platform."""
    return Health(status="ok", service=SERVICE_NAME)


@app.get("/api/v1/items", response_model=ItemList)
def list_items() -> ItemList:
    """Return the in-memory collection (swap in a repository later)."""
    return ItemList(items=list(_ITEMS))


@app.post("/api/v1/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate) -> Item:
    """Append an item to the in-memory store."""
    global _NEXT_ID
    item = Item(id=_NEXT_ID, name=payload.name)
    _NEXT_ID += 1
    _ITEMS.append(item)
    return item
