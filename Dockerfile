FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1

WORKDIR /app

COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt \
    && groupadd --system forecast \
    && useradd --system --gid forecast forecast \
    && install -d -o forecast -g forecast /app/logs

COPY app.py .
COPY config/ config/
COPY src/ src/
COPY static/ static/
COPY templates/ templates/

USER forecast
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--threads", "2", "--access-logfile", "-", "app:app"]
