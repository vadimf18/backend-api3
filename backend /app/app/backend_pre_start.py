import logging
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import SessionLocal

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Retry configuration
# -------------------------------
MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
)
def wait_for_db() -> None:
    """Wait until the database is ready."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception as e:
        logger.error("Database not ready yet: %s", e)
        raise


def main() -> None:
    logger.info("Initializing service: waiting for DB")
    wait_for_db()
    logger.info("Database is ready, service initialization complete")


if __name__ == "__main__":
    main()
