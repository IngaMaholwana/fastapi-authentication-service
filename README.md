# Basic FastAPI Logger Example

This small example demonstrates how to integrate Loguru with FastAPI and
redirect the standard library logging (including uvicorn logs) into Loguru so
that all logs benefit from Loguru formatting and sinks.

Installation (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app

You can run two ways:

- Using uvicorn (recommended for development):

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Or run the file directly (it calls uvicorn):

```powershell
python .\app\main.py
```

Visit http://127.0.0.1:8000/ to see the health endpoint.

Notes
- If you don't see colored/pretty logs, ensure your terminal supports ANSI colors and that the `loguru` package is installed.
- The code intercepts `uvicorn`, `uvicorn.error`, and `uvicorn.access` loggers and routes them through Loguru.
