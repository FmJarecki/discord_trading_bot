FROM python:3.10.12

WORKDIR /app

COPY src/ src/
COPY tests/ tests/
COPY requirements.txt .
COPY pyproject.toml .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]