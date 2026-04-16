# Minutes of Meeting — SKF Predictive Maintenance Platform
**Date:** April 10, 2026  
**Attendees:** Johan (PO), Maria (Tech Lead), Anders (UX), Priya (Data Scientist), Lars (DevOps)  
**Project:** SKF Smart Bearing Health Monitoring System  

---

## Objective
Build a cloud-based platform that monitors bearing health in real-time using IoT sensor data, applies predictive ML models, and provides actionable maintenance recommendations to plant operators.

---

## Key Decisions & Requirements

### 1. Dashboard & Visualization
- Operators need a **real-time dashboard** showing bearing health scores across all machines on the factory floor.
- Each bearing should have a **health indicator** (Green / Yellow / Red) based on vibration and temperature thresholds.
- Users should be able to **drill down** into individual bearing details: vibration spectrum, temperature trends, and predicted remaining useful life (RUL).
- The dashboard must support **multi-plant views** — operators managing multiple factories should switch between sites easily.
- Maria mentioned we need **role-based access**: Plant Manager sees all machines, Operator sees only their assigned line.

### 2. IoT Data Ingestion
- Sensors send data every **5 seconds** via MQTT protocol.
- We need an **ingestion pipeline** that handles at least 10,000 sensor readings per second.
- Raw data should be stored in a **time-series database** (Azure Data Explorer or InfluxDB).
- Data older than 90 days should be automatically **archived to cold storage**.
- Anders raised a concern: we need a **data quality check layer** — reject malformed or out-of-range readings before they reach the ML models.

### 3. Predictive ML Models
- Priya will build models for **Remaining Useful Life (RUL)** prediction and **anomaly detection**.
- Models should be retrained **monthly** using the latest operational data.
- The platform should support **A/B testing** of models — run two models in parallel and compare accuracy.
- Alert thresholds should be **configurable per machine type** — a high-speed spindle bearing has different thresholds than a conveyor roller bearing.
- Priya needs an **MLOps pipeline**: model versioning, automated retraining, and rollback capabilities.

### 4. Alerting & Notifications
- When a bearing health score drops below threshold, send **push notifications** to the operator's mobile app.
- Critical alerts (Red status) should also trigger **SMS and email** to the maintenance supervisor.
- All alerts must be **logged with timestamp** and operator acknowledgment tracking.
- Johan requested an **escalation workflow**: if an alert is not acknowledged within 30 minutes, escalate to the plant manager.

### 5. Maintenance Work Order Integration
- When an operator acknowledges an alert, the system should **auto-generate a maintenance work order** in SAP PM.
- Work orders should include: machine ID, bearing ID, predicted failure mode, recommended action, and estimated downtime.
- Completed work orders should feed back into the ML model as **ground truth data** for retraining.

### 6. Reporting & Analytics
- Monthly **reliability reports** showing: Mean Time Between Failures (MTBF), prediction accuracy, and cost savings from predictive vs. reactive maintenance.
- Export reports as **PDF and Excel**.
- Lars asked for an **admin dashboard** showing system health: data pipeline throughput, model inference latency, and API response times.

---

## Non-Functional Requirements
- **Performance:** Dashboard must load within 2 seconds for up to 500 simultaneous users.
- **Availability:** 99.9% uptime SLA — deploy across two Azure regions with automatic failover.
- **Security:** All data encrypted at rest and in transit. Comply with ISO 27001 and GDPR.
- **Scalability:** Architecture must handle 50 factories and 100,000 bearings without redesign.

---

## Action Items
| Owner | Action | Deadline |
|-------|--------|----------|
| Maria | Draft the data ingestion architecture diagram | April 15 |
| Priya | Deliver first RUL model prototype | April 22 |
| Anders | Create wireframes for the operator dashboard | April 18 |
| Lars | Set up Azure Kubernetes Service (AKS) staging environment | April 17 |
| Johan | Finalize SAP PM integration requirements with plant team | April 20 |

---

## Next Meeting
April 17, 2026 — Sprint Planning for Sprint 1
