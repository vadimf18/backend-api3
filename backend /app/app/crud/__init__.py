"""
Package for CRUD operations.

Provides instantiated CRUD objects for each model.
"""

from .crud_item import item
from .crud_user import user

# Examples for future CRUDBase usage:
# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate
# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
