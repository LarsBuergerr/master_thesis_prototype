# Backend image — FastAPI wrapper around the core analyzer.
# Build context is the REPO ROOT (the image needs src/ next to backend/):
#   docker build -f backend/Dockerfile .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# git: reporting/run metadata uses GitPython (harmless if the repo isn't mounted).
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependency layers first so code changes don't bust the pip cache.
COPY requirements.txt ./requirements-core.txt
COPY backend/requirements.txt ./requirements-web.txt
RUN pip install --no-cache-dir -r requirements-core.txt -r requirements-web.txt

COPY src/ ./src/
COPY backend/ ./backend/
# Referenz-Konfiguration der Evaluation: das Backend liefert sie über
# GET /config/default aus, das Frontend startet damit jeden Lauf. Fehlt sie,
# liefen Analysen im Container mit anderen Gewichten als die Arbeit ausweist.
COPY conf/ ./conf/

# Job database lives on a volume so results survive container rebuilds.
ENV ANALYZER_DB_PATH=/data/analyzer.db
RUN mkdir -p /data

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
