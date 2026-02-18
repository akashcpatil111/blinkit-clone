@echo off
echo Starting Services...

:: Start User Service
start "User Service" uvicorn services.user_service.main:app --port 8001
echo Started User Service on port 8001 (Swagger: localhost:8001/docs)

:: Start Product Service
start "Product Service" uvicorn services.product_service.main:app --port 8002
echo Started Product Service on port 8002 (Swagger: localhost:8002/docs)

:: Start Order Service
start "Order Service" uvicorn services.order_service.main:app --port 8003
echo Started Order Service on port 8003 (Swagger: localhost:8003/docs)

:: Start Delivery Service
start "Delivery Service" uvicorn services.delivery_service.main:app --port 8004
echo Started Delivery Service on port 8004 (Swagger: localhost:8004/docs)

echo.
echo All services started! You can check their API documentation in your browser.
echo.
echo Launching the Scraper now...
python services/product_service/seed_from_blinkit.py

pause
