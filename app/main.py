


"""Basic FastAPI + Loguru example with working logging interception.

This file configures Loguru as the application's logger and intercepts
standard library logging (including uvicorn) so messages go through Loguru's
formatting and sinks.
"""

import sys
import logging
from loguru import logger
from fastapi import FastAPI, Request


class InterceptHandler(logging.Handler):
    """Intercepts stdlib logging and forwards it to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        # Try to get a matching Loguru level, fallback to record.levelno
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno

        # Find the first frame outside of the logging module to get correct depth
        frame = logging.currentframe()
        depth = 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Configure Loguru
logger.remove()  # remove default handler
logger.add(sys.stdout, colorize=True, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")

# Redirect stdlib logging to Loguru
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# Uvicorn creates several loggers; ensure they are intercepted as well.
for uv_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    uv_logger = logging.getLogger(uv_name)
    uv_logger.handlers = [InterceptHandler()]
    uv_logger.setLevel(logging.INFO)


app = FastAPI(title="Basic FastAPI Logger Example .01")


@app.get("/")
async def root(request: Request) -> dict[str, str]:
    logger.info("Health check")
    return {"Status": "Empilweni Healthy"}


if __name__ == "__main__":
    # Run via `python -m uvicorn app.main:app` or run this file directly
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
