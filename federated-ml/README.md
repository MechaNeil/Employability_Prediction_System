# Federated Learning System

Federated Learning implementation using:

- Random Forest for classification
- FastAPI for service communication
- Docker Compose for hospital node simulation
- Local machine for central orchestration

This project uses a main-model-centric federated loop:

1. Train a base model on main_server
2. Push that main model to hospital_1 and hospital_2 as their local base
3. Retrain locally in each hospital
4. Deploy latest hospital models back to main_server
5. Aggregate contributors to create the next trainable main_model version
6. Push the updated main_model again and repeat the cycle

## 1. System Overview

### Objective

Build a privacy-preserving, distributed learning workflow where each hospital trains locally and only model artifacts are exchanged with the central server.

### High-Level Architecture

- main_server (local): orchestration, aggregation, evaluation, dashboard, model registry
- hospital_1 (docker): local train/retrain/evaluate/deploy/delete for hospital_1_model
- hospital_2 (docker): local train/retrain/evaluate/deploy/delete for hospital_2_model
- shared: dataset split and schema constants
- dataset: generated split outputs in set folders (Set-1, Set-2, Set-3)

### Why this is Federated

- Training is distributed across institutions.
- Hospitals never send raw training data to main_server.
- Main_server coordinates model artifact exchange and version progression.

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
│       │   ├── orchestration.py
│       │   ├── evaluation.py
│       │   ├── inference.py
│       │   ├── status.py
│       │   └── model_registry.py
│       ├── views/templates/dashboard.html
│       └── main.py
├── hospital_1/
│   └── app/
│       ├── api/routes.py
│       ├── core/config.py
│       ├── services/
│       │   ├── training.py
│       │   ├── deployment.py
│       │   └── model_registry.py
│       ├── views/templates/dashboard.html
│       └── main.py
├── hospital_2/
│   └── app/
│       ├── api/routes.py
│       ├── core/config.py
│       ├── services/
│       │   ├── training.py
│       │   ├── deployment.py
│       │   └── model_registry.py
│       ├── views/templates/dashboard.html
│       └── main.py
├── shared/
│   ├── constants.py
│   └── data_split.py
├── dataset/
├── docker-compose.yml
└── requirements.txt
```

## 3. Data Pipeline

Source dataset: Student-Employability-Datasets.csv

### Split Strategy

1. Remove non-feature column: Name of Student
2. Map target labels:
   - LessEmployable -> 0
   - Employable -> 1
3. Stratified split full dataset into federated set totals:
   - Set-1 total: 1250
   - Set-2 total: 1000
   - Set-3 total: 732
4. Stratified split each set into train/test using 80/20 ratio:
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

Generated files:

- dataset/Set-1/set-1_train_data.csv
- dataset/Set-1/set-1_test_data.csv
- dataset/Set-2/set-2_train_data.csv
- dataset/Set-2/set-2_test_data.csv
- dataset/Set-3/set-3_train_data.csv
- dataset/Set-3/set-3_test_data.csv

Command:

```bash
python -m shared.data_split
```

## 4. Model Lifecycle (Current Architecture)

### 4.1 Main Model Training

- Service: main_server.app.services.training
- Algorithm: RandomForestClassifier(n_estimators=100, random_state=42)
- Typical dataset: Set-1 train split
- Writes canonical artifact: main_server/app/models/model.pkl
- Registers new main_model version in registry

### 4.2 Push Base Model to Hospitals

- Service: main_server.app.services.orchestration -> POST /deploy
- Main server pushes active main_model artifact to:
  - hospital_1 /model/upload
  - hospital_2 /model/upload
- Hospitals store uploaded artifact as new local active version

### 4.3 Hospital Local Retraining

Each hospital retrains locally using /train or /retrain:

- hospital_1 default train dataset: Set-2
- hospital_2 default train dataset: Set-3
- retrain_from_main=true attempts to initialize from active main_model
- if main model is unavailable, hospital falls back to local fresh train

### 4.4 Deploy Hospital Models Back to Main

- hospital_1: POST /deploy-to-main (model_family hospital_1_model)
- hospital_2: POST /deploy-to-main (model_family hospital_2_model)
- main_server stores uploaded versions in model registry

### 4.5 Aggregation Updates main_model (No global_model Family)

- Service: main_server.app.services.aggregation
- Aggregation uses contributors:
  - current active main_model
  - active hospital_1_model (if available)
  - active hospital_2_model (if available)
- Builds pseudo-label votes from contributors over combined train datasets
- Trains a new RandomForest model from pseudo-labels
- Registers result as next main_model version

### 4.6 Evaluation

- Service: main_server.app.services.evaluation
- /evaluate evaluates active main_model
- Supports all test sets combined or a selected set
- Metrics: Accuracy, Precision, Recall, F1

## 5. Runtime Orchestration Flow

### Recommended Sequence

1. Generate split files
2. Start hospital containers
3. Start main_server
4. Train main model
5. Push main model to hospitals
6. Retrain in hospital_1 and hospital_2
7. Deploy hospital models to main_server
8. Aggregate to update main_model
9. Re-push updated main_model and repeat

### Inter-service Communication Notes

- main_server -> hospitals for base push uses /model/upload
- hospitals -> main_server for return deploy uses /remote-models/upload
- Hospitals include URL fallbacks for main upload endpoint:
  - host.docker.internal
  - main_server
  - localhost

## 6. API Reference

### Main Server (port 8000)

- GET / -> Interactive dashboard
- GET /health -> Main server status
- GET /status -> Combined runtime status (hospitals, model artifacts, metrics)
- GET /model-version -> Registry overview
- POST /train -> Train main model
- POST /deploy -> Push active main_model to hospitals
- POST /retrain-hospitals -> Informational endpoint (hospitals retrain locally)
- GET /aggregate -> Aggregate contributors and update main_model
- GET /evaluate -> Evaluate active main_model
- POST /predict -> Predict employability for provided records
- POST /remote-models/upload -> Receive uploaded models from hospitals/manual forward
- POST /models/delete-version -> Delete selected version in a family
- POST /models/delete-family -> Delete selected family
- POST /models/delete-all -> Remove all model artifacts in main models directory

### Hospital Services (ports 8001, 8002)

- GET /health -> Hospital status
- GET /status -> Local hospital status and version/eval summaries
- GET /model-version -> Active local version + all local versions
- POST /train -> Local train/retrain based on payload
- POST /retrain -> Retrain-focused endpoint (defaults per hospital)
- POST /evaluate -> Evaluate active local model
- POST /deploy-to-main -> Upload active local model to main_server
- GET /model -> Download active local model artifact
- POST /model/upload -> Upload model artifact into local registry
- POST /model/activate -> Switch active local version
- POST /model/delete-version -> Delete selected local version (local family only)
- POST /model/delete-family -> Delete local family (local family only)

## 7. Dashboard Functionality

Main dashboard URL: http://localhost:8000/

### Main Dashboard Features

- Live system status visualization
- 3 model cards (Main, Hospital-1, Hospital-2)
- Workflow timeline including aggregation state
- Action controls for train, deploy, aggregate, evaluate
- Version management (delete version/family/all)
- Version comparison and activity logs
- Poll-based status refresh

### Hospital Dashboard Features

- Local version registry view
- Local train/retrain/evaluate
- Activate local version
- Deploy active local model to main_server
- Delete selected local version or local family

## 8. Deployment and Run Guide

### Prerequisites

- Python 3.11+
- Docker + Docker Compose plugin

### Commands

```bash
cd federated-ml
pip install -r requirements.txt

python -m shared.data_split

# start hospitals
Docker compose up --build -d

# start main server
uvicorn main_server.app.main:app --host 0.0.0.0 --port 8000
```

### Trigger one full federated cycle (example)

```bash
# main train
curl -X POST http://localhost:8000/train -H "Content-Type: application/json" -d '{"dataset":"set1"}'

# push main model to hospitals
curl -X POST http://localhost:8000/deploy

# retrain locally at hospitals
curl -X POST http://localhost:8001/retrain -H "Content-Type: application/json" -d '{"dataset":"set2","retrain_from_main":true}'
curl -X POST http://localhost:8002/retrain -H "Content-Type: application/json" -d '{"dataset":"set3","retrain_from_main":true}'

# deploy local hospital models back to main
curl -X POST http://localhost:8001/deploy-to-main -H "Content-Type: application/json" -d '{}'
curl -X POST http://localhost:8002/deploy-to-main -H "Content-Type: application/json" -d '{}'

# aggregate and evaluate main
curl http://localhost:8000/aggregate
curl http://localhost:8000/evaluate
```

## 9. Key Functionalities Summary

1. Main-model-centric federated lifecycle (no separate global_model family)
2. Deterministic, stratified data preparation pipeline
3. Bi-directional model exchange between main and hospitals
4. Trainable aggregated main_model version updates
5. Main and hospital dashboards for monitoring and control
6. Local-only delete controls on hospital model families
7. End-to-end evaluation with classification metrics
8. Registry-backed version tracking across all services

## 10. Known Limitations

1. Aggregation is distillation-from-votes, not tree-parameter averaging.
2. No authentication layer between services.
3. No persistent external database for experiments.
4. In mixed host/container setups, upload endpoint reachability still depends on environment networking.

## 11. Recommended Next Improvements

1. Add weighted contributor voting prior to distillation.
2. Add authentication/authorization for inter-service APIs.
3. Add integration tests for full cycle and failure paths.
4. Add structured observability (metrics + traces + logs).
5. Add CI checks for API contract and workflow regression.
