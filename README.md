# Blinkit Clone - B2C Quick Commerce Application

This is a minimal, fully functional B2C quick-commerce application built to demonstrate a microservices architecture, cross-platform frontend development, and containerized deployment.

## 🏗️ Overall Architecture
The system follows a strict **Microservices Architecture** with a clear separation of concerns. 
- The backend is divided into exactly **4 independent microservices**.
- Each service runs in its own Docker container, communicates via REST APIs (JSON), and maintains its own isolated MongoDB collection.
- The frontend is built with **Flutter**, designed to connect with these four independent services as a unified mobile app experience.

### Service Responsibilities
1. **User Service (Port 8001)**
   *   **Responsibility:** Handles user registration, login, profile management, and maintains user address books.
   *   **Authentication:** Issues simple Bearer tokens (JWT) upon successful login.

2. **Product Catalog Service (Port 8002)**
   *   **Responsibility:** Manages all product listings and categories.
   *   **Seeding:** Includes an automated scraper script (`seed_from_blinkit.py`) that populates the MongoDB product collection with real-world data directly from Blinkit.com.

3. **Cart and Order Service (Port 8003)**
   *   **Responsibility:** Manages cart items, converts items into historical orders, calculates totals, and assigns unique order reference IDs.

4. **Delivery Service (Port 8004)**
   *   **Responsibility:** Manages and tracks the lifecycle of an order’s delivery progression.
   *   **Simulation:** Contains an asynchronous background process that automatically progresses active orders through the status pipeline every 30 seconds.

## 🔌 API List

### 1. User Service (`http://127.0.0.1:8001`)
*   **`POST /register`** - Create a new user account.
*   **`POST /login`** - Authenticate and receive a JWT token.
*   **`GET /profile`** - Fetch the authenticated user's profile data.
*   **`GET /users/me/addresses`** - Get saved delivery addresses.
*   **`POST /users/me/addresses`** - Add a new delivery address.

### 2. Product Catalog Service (`http://127.0.0.1:8002`)
*   **`GET /products`** - Fetch all products (supports `category` and `q` search queries).
*   **`GET /products/{product_id}`** - Fetch a specific product by ID.
*   **`GET /categories`** - Fetch all unique product categories.

### 3. Cart and Order Service (`http://127.0.0.1:8003`)
*   **`POST /cart/add`** - Add an item to the user's cart.
*   **`POST /cart/remove`** - Remove an item from the user's cart.
*   **`GET /cart/{user_id}`** - Fetch the user's current cart.
*   **`POST /order/create`** - Convert cart payload into an official order.
*   **`GET /orders?user_id={user_id}`** - Fetch order history for a specific user.
*   **`GET /order/{order_id}`** - Fetch details of a specific order.

### 4. Delivery Service (`http://127.0.0.1:8004`)
*   **`GET /order/{order_id}/status`** - Get the delivery object for a specific order.
*   **`POST /order/{order_id}/update-status`** - Manually update the status of an active delivery.
*(Expected Statuses: `PLACED`, `PACKED`, `OUT_FOR_DELIVERY`, `DELIVERED`)*

## 🚀 How to Run the System Locally

### Option 1: Quick Start (Windows Batch Script)
The easiest way to start the entire backend stack locally is to use the provided batch script. You must have Python installed.

1. Ensure your MongoDB instance is running (locally or via Docker).
2. Double-click the `run_demo.bat` file in the root `blinkit_commerce` directory.
3. This script will automatically:
    * Install all required Python dependencies (`requirements.txt`).
    * Boot up all 4 microservice APIs (ports 8001 through 8004) in background terminal windows.
    * Trigger the Selenium web scraper to dynamically seed the Product Database with real data.
4. Navigate to `http://localhost:<PORT>/docs` in your browser to view the interactive Swagger API documentation for any of the 4 services.

### Option 2: Docker Containers
Each service contains its own `Dockerfile` allowing for independent containerized deployment.
1. Build the images from the root directory:
   * `docker build -t user-service -f services/user_service/Dockerfile .`
   * `docker build -t product-service -f services/product_service/Dockerfile .`
   * `docker build -t order-service -f services/order_service/Dockerfile .`
   * `docker build -t delivery-service -f services/delivery_service/Dockerfile .`
2. Run each container, exposing their respective ports (8001, 8002, 8003, 8004), and passing your `MONGO_URI` environment variable so they can connect to the shared database cluster.

### Running the Frontend (Flutter)
1. Ensure the Flutter SDK is installed.
2. Open a terminal and navigate to `frontend/blinkit_mobile`.
3. If running on a Desktop or Web browser, ensure the `baseUrl` in `lib/services/api_service.dart` points to your IP address (e.g., `http://127.0.0.1` or `http://localhost`). It defaults to `http://10.0.2.2` for Android Emulator loopbacks.
4. Run `flutter run`.

## 🤔 Assumptions Made
* **Trusted Network:** As per the assignment guidelines, authentication is only explicitly enforced on frontend-facing APIs (like Login/Profile). Communication between internal services (like the Order service sending a signal to the Delivery service) assumes a secure, trusted internal network and skips heavy token validation for simplicity.
* **Prepaid Orders:** There is no payment gateway integration. It is assumed that hitting the `/order/create` endpoint implies a prepaid, completely legitimate order.
* **Shared Database Host:** Rather than spinning up 4 entirely separate heavy MongoDB instances, the architecture assumes 1 common MongoDB server host (e.g. `localhost:27017`), but utilizes completely independent collections (`users`, `products`, `orders`, `deliveries`) within it for strict data segregation.

## ⚠️ Known Limitations
* **OTP Implementation:** The authentication system uses a basic JWT email/password system. Complex phone-based SMS OTPs were skipped per the assignment guidelines to prioritize architectural focus over third-party integration overhead.
* **Delivery Simulation:** The delivery tracking is purely a background scheduled simulation. There is no actual logistics mapping or driver assignment logic.

## 🤖 Transparency Requirement (AI Usage)
* **Frontend UI (Flutter):** I utilized Google Stitch generated UI layouts from the provided reference URL and adapted them into the Flutter Widget tree.
* **Microservices Base:** The initial boilerplate for the FastAPI Python services, the Pydantic data models, and the database connection strings were scaffolded using AI code generation (Cursor/Antigravity).
* **Manual Customizations & Fixes:** I heavily customized the generated backend to enforce strict conformance with the assignment requirements. This included rewriting API endpoints, standardizing the `DeliveryStatus` enum flows to match the prompt (`PLACED` -> `DELIVERED`), modifying Pydantic models to auto-generate `reference_id`s, and rectifying application startup crashes across the `order` and `delivery` services manually using terminal debugging.
