# Blinkit Clone - Microservices & Flutter Architecture

> **Project Description**: A B2C Quick Commerce app (Blinkit-like) built on a Microservices architecture. Features 4 isolated backend services (FastAPI + MongoDB), a premium Flutter mobile app (Provider), and full Docker/Kubernetes orchestration. Includes auth, product search, cart management, and real-time delivery tracking simulation.

> **Transparency Statement**: 
> - **Scaffolding and Isolation**: Managed via Google Antigravity.
> - **UI Design**: Derived from Google Stitch requirements.
> - **AI Assistance**: "Gemini" was used for architectural logic optimization and generating K8s configuration. 
> - **Manual Implementation**: Core logic in services, state management in Flutter, and Dockerfile optimization were verified manually.
> - **Architecture Decision**: The Cart logic is implemented via Client-Side State (Provider) for minimal latency ("Optimistic UI"), with the final transaction being sent to the Order Service. This reduces inter-service chatter for a smoother user experience in this demonstration scope.

## 🏗️ Architecture
(See ASCII diagram in previous steps or implementation plan)

## 🚀 Tech Stack
-   **Backend**: FastAPI (Python) - 4 Isolated Microservices
-   **Frontend**: Flutter (Dart) - Provider State Management
-   **Database**: MongoDB
-   **Infrastructure**: Docker, Kubernetes (Manifests included)

## 🛠️ Local Setup

### Option 1: Docker Compose (Development)
1.  **Start Services**: `docker compose up -d --build`
2.  **Run Flutter App**: No install - use Codespaces!

### Option 2: GitHub Codespaces (No Install)
Run without installing anything:
1.  Push to GitHub.
2.  Click **Code** -> **Codespaces** -> **Create codespace on main**.
3.  Run:
    ```bash
    docker compose up -d
    cd frontend/blinkit_mobile
    flutter run -d web-server --web-hostname 0.0.0.0 --web-port 8080
    ```

### Option 3: Kubernetes (Production Simulation)
1.  Build Images.
2.  `kubectl apply -f k8s/`
3.  Access services on NodePorts 30001-30004.

## ✨ Features
-   **Microservices**: User, Product, Order, Delivery.
-   **Real-time**: Delivery tracking simulation.
-   **Premium UI**: Google Stitch design.

## 📦 Seeding Data

To simulate real-world data, you can seed the `product_service` with data extracted from Blinkit.

1.  Navigate to the service directory:
    ```bash
    cd blinkit_commerce/services/product_service
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the seeder script:
    ```bash
    python seed_from_blinkit.py
    ```
    *Note: This script uses Selenium (headless) to scrape live data. Ensure you have Chrome installed.*
