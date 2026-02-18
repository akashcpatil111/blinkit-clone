# Blinkit Clone - Microservices & Flutter Architecture

**Intern Assignment Submission**

## 📋 Project Overview
A minimal B2C quick-commerce application built with a **Microservices Architecture**.
- **Backend**: Python (FastAPI) - 4 Independent Services
- **Frontend**: Flutter (Mobile App)
- **Database**: MongoDB (Per-service collections)
- **Infrastructure**: Docker & Kubernetes

## 🏗️ Architecture

The system is split into 4 isolated microservices as required:

1.  **User Service** (`Port 8001`)
    - Handles Registration & Login (JWT Auth).
    - Manages User Profile & Addresses.
2.  **Product Service** (`Port 8002`)
    - Manages Product Catalog & Categories.
    - Includes **Data Seeding Script** (Selenium based).
3.  **Order Service** (`Port 8003`)
    - Manages Cart (Backend API compliant) & Order Creation.
    - Stores Order History.
4.  **Delivery Service** (`Port 8004`)
    - Manages Delivery Lifecycle.
    - **Auto-Simulation**: Background task automatically moves status from `PLACED` -> `DELIVERED`.

## 🛠️ How to Run (Evaluator Guide)

### Prerequisites
- Docker Desktop (Recommended)
- OR Python 3.10+ and MongoDB installed locally.

### Method 1: Docker Compose (Easiest)
1.  Open terminal in root directory.
2.  Run:
    ```bash
    docker-compose up --build
    ```
    *This starts all 4 services and MongoDB.*

### Method 2: Manual / Local Run
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure MongoDB is running locally on port `27017`.
3.  Start each service in a separate terminal:
    ```bash
    uvicorn services.user_service.main:app --port 8001
    uvicorn services.product_service.main:app --port 8002
    uvicorn services.order_service.main:app --port 8003
    uvicorn services.delivery_service.main:app --port 8004
    ```

### Running the Frontend (Flutter)
1.  Navigate to app directory:
    ```bash
    cd frontend/blinkit_mobile
    ```
2.  Run on emulator:
    ```bash
    flutter run
    ```
    *Note: The app is configured to connect to `10.0.2.2` (Android Emulator localhost). If running on iOS or Web, update `baseUrl` in `lib/services/api_service.dart`.*

## 📦 Data Seeding
To populate the app with real data from Blinkit:
1.  Ensure Chrome is installed.
2.  Run:
    ```bash
    python services/product_service/seed_from_blinkit.py
    ```

## 🔍 Transparency Statement (AI Usage)
In compliance with the assignment transparency requirement:
- **Architecture Design**: AI assisted in defining the microservices boundaries and Kubernetes manifests.
- **Boilerplate Code**: `FastAPI` structures and `Pydantic` models were scaffolded using AI to save time.
- **Frontend UI**: Google Stitch generated HTML was used as a reference; Flutter widgets were implemented manually with AI assistance for state management (Provider pattern).
- **Core Logic**: Business logic (Cart calculations, Delivery simulation, JWT handling) was verified and refined manually.

## ☸️ Kubernetes (Production Simulation)

If you prefer to run on Kubernetes (e.g., Minikube or Docker Desktop K8s):

1.  **Build Images Locally** (Required because `imagePullPolicy` is `Never`):
    ```bash
    docker build -t user-service:latest ./services/user_service
    docker build -t product-service:latest ./services/product_service
    docker build -t order-service:latest ./services/order_service
    docker build -t delivery-service:latest ./services/delivery_service
    ```
2.  **Deploy**:
    ```bash
    kubectl apply -f k8s/
    ```
3.  **Access**: Services will be available on NodePorts `30001` (User), `30002` (Product), `30003` (Order), `30004` (Delivery).
