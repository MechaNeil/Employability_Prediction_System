# Federated Learning System (FastAPI + Docker + Random Forest)

## 1) Project Setup

```bash
cd federated-ml
pip install -r requirements.txt
```

## 2) Generate Dataset Splits

This creates:
- dataset/set1.csv
- dataset/set2.csv
- dataset/set3.csv
- dataset/test.csv

```bash
python -m shared.data_split
```

## 3) Train Initial Main Model

```bash
python -m main_server.app.services.training
```

## 4) Start Hospital Containers (auto retrain on startup)

```bash
docker-compose up --build
```

## 5) Run Main Server Locally

```bash
uvicorn main_server.app.main:app --host 0.0.0.0 --port 8000
```

## 6) Execute Federated Aggregation + Evaluation

```bash
# trigger aggregation flow
curl http://localhost:8000/aggregate

# evaluate latest global model
curl http://localhost:8000/evaluate
```

## Main Endpoints
- POST /train
- GET /aggregate
- GET /evaluate
- GET /health

## Hospital Endpoints
- POST /retrain
- GET /model
- GET /health

## Notes
- Random Forest aggregation uses majority voting over predictions.
- Main server runs locally; hospitals run in Docker.
- Hospitals retrain automatically before API starts.
