


#Creating a basic FastAPI app loger
import logging
import uvicorn
import sys
from loguru import logger
from fastapi import FastAPI, Request

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Log the message with Loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
            )

# logger = logging.getLogger(__name__) this line will be ade by loguru for formatting
# formmatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
#     )
# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(formmatter)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)

for name in logging.root.manager.loggerDict:
    # print(f"Configuring logger: {name}")
    if name in ("uvicorn"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        # uvicorn_logger.addHandler(handler)
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.addHandler(InterceptHandler())

app = FastAPI(title="Basic FastAPI Logger Example .01")

@app.get("/")
async def root(request: Request) -> dict[str,str]:
    logger.info("Health chck")
    return {"Status": "Empilweni Healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
