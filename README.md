# IFCB Focus Microservice

A stateless microservice for computing focus metrics on IFCB (Imaging FlowCytobot) bins using the ifcb-focus v1.0.1 student model.

## API Endpoint

- `GET /focus_metric/{bin_id}` — Returns the focus score for the specified IFCB bin.

### Response

Plain text content type with a single float value representing the focus score (e.g., `0.8542`).

## Setup

1. Copy `.env.template` to `.env` and configure the paths:

```bash
cp .env.template .env
```

2. Edit `.env` to set your local paths:

```env
# Path to IFCB data directory containing .roi, .adc, and .hdr files
COMPOSE_IFCB_DATA_DIR=/path/to/ifcb/data

# Path to directory containing slim_student_model.pkl
COMPOSE_MODEL_DIR=/path/to/models

# Port for the service (default: 8001)
COMPOSE_PORT=8001
```

## Run with Docker Compose

```bash
docker compose up --build
```

## Request Example

```bash
curl http://localhost:8001/focus_metric/D20130823T160901_IFCB010
```

### Example Response

```
0.8542
```

## Requirements

- IFCB data directory with bin files (.roi, .adc, .hdr)
- Pre-trained `slim_student_model.pkl` from ifcb-focus v1.0.1
- Docker and Docker Compose
