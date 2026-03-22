# Federated Learning System

Federated Learning implementation using:

- Random Forest for classification
- FastAPI for service communication
- Docker Compose for hospital node simulation
- Local machine for central orchestration

This project trains a base model, distributes learning to two hospital nodes, aggregates the resulting models into a new global model, and evaluates global performance.

## 1. System Overview

### Objective

Build a privacy-preserving, distributed learning workflow where each hospital trains locally and only model artifacts are exchanged with the central server.

### High-Level Architecture

- `main_server` (local): orchestration, aggregation, evaluation, dashboard
- `hospital_1` (docker): local retraining on Set-2
- `hospital_2` (docker): local retraining on Set-3
- `shared`: dataset split and schema constants
- `dataset`: generated split outputs in set folders (`Set-1`, `Set-2`, `Set-3`)

### Why this is Federated

- Training is distributed across institutions.
- The central server aggregates model behavior instead of pooling raw data during orchestration.
- Hospitals expose model artifacts through controlled endpoints.

## 2. Project Structure

```text
federated-ml/
├── main_server/
│   └── app/
│       ├── api/routes.py
│       ├── core/config.py
│       ├── services/
│       │   ├── training.py
│       │   ├── aggregation.py
│       │   ├── evaluation.py
│       │   ├── inference.py
│       │   └── status.py
│       ├── views/model_view.py
│       └── main.py
├── hospital_1/
│   └── app/
│       ├── api/routes.py
│       ├── views/model_view.py
│       └── services/training.py
├── hospital_2/
│   └── app/
│       ├── api/routes.py
│       ├── views/model_view.py
│       └── services/training.py
├── shared/
│   ├── constants.py
│   └── data_split.py
├── dataset/
├── docker-compose.yml
└── requirements.txt
```

## 3. Data Pipeline

Source dataset: `Student-Employability-Datasets.csv`

### Split Strategy

1. Remove non-feature column: `Name of Student`
2. Map target labels:
	 - `LessEmployable -> 0`
	 - `Employable -> 1`
3. Stratified split full dataset into federated set totals:
	 - Set-1 total: 1250
	 - Set-2 total: 1000
	 - Set-3 total: 732
4. Stratified split each set into train/test using an 80/20 ratio:
	 - Set-1: 1000 train, 250 test
	 - Set-2: 800 train, 200 test
	 - Set-3: 586 train, 146 test

Current split summary from the dataset in this repository:

| Dataset | Training | Testing | Total |
|---|---:|---:|---:|
| Set-1 | 1000 | 250 | 1250 |
| Set-2 | 800 | 200 | 1000 |
| Set-3 | 586 | 146 | 732 |
| Total | 2386 | 596 | 2982 |

Implementation details:

- Stratified sampling (`stratify=y`)
- Deterministic seed (`random_state=42`)
- Feature consistency validation before saving

Generated files:

- `dataset/Set-1/set-1_train_data.csv`
- `dataset/Set-1/set-1_test_data.csv`
- `dataset/Set-2/set-2_train_data.csv`
- `dataset/Set-2/set-2_test_data.csv`
- `dataset/Set-3/set-3_train_data.csv`
- `dataset/Set-3/set-3_test_data.csv`

Command:

```bash
python -m shared.data_split
```

## 4. Model Lifecycle

### 4.1 Initial Main Model Training

- Service: `main_server.app.services.training`
- Algorithm: `RandomForestClassifier(n_estimators=100, random_state=42)`
- Training data: `dataset/Set-1/set-1_train_data.csv`
- Artifact output: `main_server/app/models/model.pkl`

Command:

```bash
python -m main_server.app.services.training
```

### 4.2 Hospital Retraining

Each hospital:

1. Loads latest available global model (`main_model_v2.pkl`), or falls back to base model (`model.pkl`)
2. Retrains locally using:
	 - Hospital-1 -> `dataset/Set-2/set-2_train_data.csv`
	 - Hospital-2 -> `dataset/Set-3/set-3_train_data.csv`
3. Saves local artifact:
	 - `hospital_1/app/models/hospital_model.pkl`
	 - `hospital_2/app/models/hospital_model.pkl`

### 4.3 Aggregation

- Service: `main_server.app.services.aggregation`
- Strategy: Majority voting ensemble over predictions from 3 models:
	- main base model
	- hospital_1 model
	- hospital_2 model
- Tie-break: class `1` is chosen when votes are equal
- Output: `main_server/app/models/main_model_v2.pkl`

### 4.4 Evaluation

- Service: `main_server.app.services.evaluation`
- Dataset: combined test splits
	 - `dataset/Set-1/set-1_test_data.csv`
	 - `dataset/Set-2/set-2_test_data.csv`
	 - `dataset/Set-3/set-3_test_data.csv`
- Metrics:
	- Accuracy
	- Precision
	- Recall
	- F1-score

## 5. Runtime Orchestration Flow

### Sequence

1. Generate split files
2. Train main model
3. Start hospital containers
4. Hospitals retrain automatically at startup
5. Start main server
6. Trigger aggregation endpoint
7. Evaluate global model

### Inter-service Communication

During `GET /aggregate`, main server performs:

1. `POST /retrain` on both hospitals
2. `GET /model` from both hospitals
3. Loads all models using `joblib`
4. Builds majority-vote ensemble
5. Saves global model
6. Computes evaluation metrics

### Reliability Features

- Retry with exponential backoff for hospital requests
- Configurable request retries and timeout using env vars:
	- `REQUEST_RETRIES`
	- `REQUEST_TIMEOUT_SECONDS`
- Structured orchestration logs in main server

## 6. API Reference

### Main Server (port 8000)

- `GET /` -> Interactive dashboard
- `GET /health` -> Main server status
- `GET /status` -> Combined runtime status (hospitals, model artifacts, metrics)
- `GET /model-version` -> Metadata for base/global model files
- `POST /train` -> Train initial main model on Set-1
- `POST /deploy` -> Simulate deployment of latest central model to hospitals
- `POST /retrain-hospitals` -> Trigger retraining on both hospitals
- `GET /aggregate` -> Trigger federated retrain + model aggregation
- `GET /evaluate` -> Evaluate current global model on all three test splits
- `POST /predict` -> Predict employability for provided records

Sample `POST /predict` payload:

```json
{
	"records": [
		{
			"GENERAL APPEARANCE": 4,
			"MANNER OF SPEAKING": 4,
			"PHYSICAL CONDITION": 4,
			"MENTAL ALERTNESS": 4,
			"SELF-CONFIDENCE": 4,
			"ABILITY TO PRESENT IDEAS": 4,
			"COMMUNICATION SKILLS": 4,
			"Student Performance Rating": 5
		}
	]
}
```

### Hospital Services (ports 8001, 8002)

- `GET /health` -> Hospital status
- `POST /retrain` -> Local retraining trigger
- `GET /model` -> Return local model artifact as file response

## 7. Dashboard Functionality

Dashboard URL: `http://localhost:8000/`

Features:

- Live system status visualization
- Main/Hospital/Global model cards
- Action buttons for train/aggregate/evaluate
- Workflow health indicators
- Lightweight performance chart
- Activity log with API outcomes
- Poll-based status refresh

## 8. Deployment and Run Guide

### Prerequisites

- Python 3.12+
- Docker + Docker Compose plugin

### Commands

```bash
cd federated-ml
pip install -r requirements.txt

python -m shared.data_split
python -m main_server.app.services.training

docker compose up --build

uvicorn main_server.app.main:app --host 0.0.0.0 --port 8000
```

### Trigger full flow

```bash
curl -X POST http://localhost:8000/train -H "Content-Type: application/json" -d '{"dataset":"set1"}'
curl -X POST http://localhost:8001/retrain -H "Content-Type: application/json" -d '{"dataset":"set2","retrain_from_main":true}'
curl -X POST http://localhost:8002/retrain -H "Content-Type: application/json" -d '{"dataset":"set3","retrain_from_main":true}'
curl http://localhost:8000/aggregate
curl http://localhost:8000/evaluate
```

## 9. Key Functionalities Summary

1. Federated-style training orchestration across two hospital nodes
2. Deterministic, stratified data preparation pipeline
3. Automatic retraining in containers at startup
4. Majority-vote global model aggregation for Random Forest compatibility
5. Real-time dashboard monitoring of service/model health
6. Prediction API for downstream integration
7. End-to-end evaluation with core classification metrics
8. Retry/backoff resilience for hospital communication
9. Model version/status introspection endpoints

## 10. Known Limitations

1. Aggregation is voting-based, not parameter averaging (by design for tree models).
2. No authentication layer between services.
3. No persistent database for experiment tracking.
4. Hospitals currently read split files from shared project volume (simulation mode).

## 11. Recommended Next Improvements

1. Add weighted voting based on local validation performance.
2. Add authentication (API key/token) for hospital endpoints.
3. Add model registry/version history storage.
4. Add structured JSON logging export and observability dashboards.
5. Add automated tests for split integrity, endpoint contracts, and aggregation behavior.
