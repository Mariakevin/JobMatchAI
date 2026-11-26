# Getting started

This guide starts the frontend and backend locally for development. It assumes a terminal and Git are available.

## Prerequisites

- Python 3.10 or newer.
- Node.js 20 or newer and npm.
- Git.

The repository does not currently include a Python lockfile or a pyproject.toml; backend dependencies are declared in requirements.txt. Frontend dependencies and scripts are declared in package.json and pinned more precisely by package-lock.json.

## 1. Clone the repository

~~~bash
git clone https://github.com/Mariakevin/JobMatchAI.git
cd JobMatchAI
~~~

## 2. Create the Python environment

Linux and macOS:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

Windows PowerShell:

~~~powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

The backend requirements currently include FastAPI, Uvicorn, python-multipart, pypdf, and python-docx.

## 3. Start the backend

From the repository root, with the virtual environment activated:

~~~bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
~~~

The API is available at:

- Health check: http://127.0.0.1:8000/api/health
- Interactive OpenAPI UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

Keep this terminal running.

## 4. Install and start the frontend

Open a second terminal in the repository root:

~~~bash
npm install
npm run dev
~~~

Vite prints the local development URL. The default is usually http://localhost:5173.

The Vite configuration proxies requests whose path begins with /api to http://localhost:8000. For the standard local setup, no separate frontend API URL is required.

## 5. Verify the application

1. Open the Vite URL in a browser.
2. Confirm that the workspace renders.
3. Upload a text-based PDF, DOCX, or TXT resume, or paste resume text.
4. Review the extracted profile and correct inaccurate fields.
5. Enter one or more internship descriptions.
6. Run the analysis and inspect the eligibility ledger, skill evidence, practical fit, warnings, and score breakdown.

The initial UI contains a demonstration internship. Treat it as sample content, not a real vacancy or employer.

## 6. Run the automated tests

With the Python virtual environment activated:

~~~bash
python -m unittest discover -s tests -v
~~~

Build the frontend:

~~~bash
npm run build
~~~

For test coverage and known security boundaries, see [Testing and security](testing-security.md).

## Configuration notes

- Backend upload and parsing limits are defined in api/resume_parser.py.
- The backend API version returned by the health endpoint is currently 0.2.0.
- The frontend can read VITE_API_BASE_URL for a non-proxied API base URL; otherwise it uses same-origin relative /api paths.
- The frontend request helper applies a 30-second timeout.
- The current CORS allow-list in api/main.py is limited to localhost development origins. It must be configured deliberately before a different frontend origin is used.

## Troubleshooting

### The frontend loads, but analysis fails

Check that the backend is running on port 8000. Open http://127.0.0.1:8000/api/health directly and confirm it returns JSON with status set to ok.

### Resume upload reports that no text was found

The current PDF path extracts embedded text; it does not perform OCR. Scanned or image-only PDFs must be converted to selectable text or entered using the paste field.

### The browser reports a CORS error

The backend currently allows the two localhost frontend origins listed in api/main.py. Add the exact development origin to the allow-list if your local setup uses another host or port.

### Dependency or interpreter errors

Confirm the active interpreter is inside .venv, then reinstall requirements.txt. Confirm Node.js and npm meet the prerequisites before running npm install.
