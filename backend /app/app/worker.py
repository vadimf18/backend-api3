from typing import Any

from raven import Client
from app.core.celery_app import celery_app
from app.core.config import settings

# -------------------------------
# Sentry client
# -------------------------------
client_sentry = Client(settings.SENTRY_DSN)


# -------------------------------
# Celery tasks
# -------------------------------
@celery_app.task(acks_late=True, bind=True)
def test_celery(self, word: str) -> str:
    """
    Simple test Celery task.
    
    Args:
        word (str): input word
    
    Returns:
        str: formatted return string
    """
    try:
        result = f"test task return {word}"
        return result
    except Exception as exc:
        # Capture the exception in Sentry
        client_sentry.captureException()
        raise exc
