
FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY devsecops_module /app/devsecops_module
COPY main_app.py /app/
COPY run_orchestrator.sh /app/

RUN chmod +x /app/run_orchestrator.sh

EXPOSE 8000


CMD ["/app/run_orchestrator.sh"]