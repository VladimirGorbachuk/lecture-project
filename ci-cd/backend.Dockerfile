FROM python:3.9-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY ./backend/requirements/web_api.requirements.txt .
RUN pip install -r web_api.requirements.txt

FROM python:3.9-slim
COPY --from=builder /opt/venv /opt/venv
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
COPY ./backend/src ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]