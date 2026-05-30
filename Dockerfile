FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -e .

EXPOSE 8080

CMD ["uvicorn", "agentic_lab.api:app", "--host", "0.0.0.0", "--port", "8080"]
