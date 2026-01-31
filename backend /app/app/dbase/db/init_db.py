from sqlalchemy.orm import Session
from app.models import user, item
from app.crud import user as crud_user

def init_db(db: Session) -> None:
    """
    Создает начальные данные (например, первого суперпользователя)
    """
    from app.core.config import settings

    if not crud_user.user.get_by_email(db, email=settings.FIRST_SUPERUSER):
        crud_user.user.create(
            db,
            obj_in={
                "email": settings.FIRST_SUPERUSER,
                "password": settings.FIRST_SUPERUSER_PASSWORD,
                "full_name": "Admin",
                "is_superuser": True,
            },
        )
