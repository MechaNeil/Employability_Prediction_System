FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY . /workspace

CMD ["uvicorn", "employability_1.app.main:app", "--host", "0.0.0.0", "--port", "8001"]

