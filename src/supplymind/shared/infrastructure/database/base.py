"""Shared SQLAlchemy declarative base."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


# -------------------
# Declarative base
# -------------------

class Base(DeclarativeBase):
    """Base class for all PostgreSQL ORM models."""
