FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY . /workspace

CMD ["sh", "-c", "python -m hospital_1.app.services.training && uvicorn hospital_1.app.main:app --host 0.0.0.0 --port 8001"]
