# Smart Inventory & Order Management System


![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-336791.svg?style=flat&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg?style=flat)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange.svg?style=flat)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker)
![License](https://img.shields.io/badge/license-MIT-blue.svg)


A robust backend system built with FastAPI and PostgreSQL to manage real-time inventory, purchase orders, supplier details, and stock movements. This project serves as a strong demonstration of modern backend development practices and advanced RDBMS features.


## ✅ Key Features

-   **Clean & Scalable Architecture**: Follows a structured, feature-based layout with clear separation of concerns (API, CRUD, Models, Schemas).
-   **Full CRUD Operations**: Endpoints for managing Products, Suppliers, and Orders.
-   **Relational Data Modeling**: Utilizes SQLAlchemy 2.0 to define relationships between Products, Suppliers, and Orders.
-   **Database Migrations**: Employs **Alembic** to manage database schema changes in a version-controlled, reproducible manner.
-   **Configuration Management**: Centralized configuration using Pydantic's `BaseSettings` and a `.env` file.
-   **Containerized Services**: Uses **Docker** and `docker-compose` to run a PostgreSQL database, ensuring a consistent development environment.
-   **Programmatic DB Administration**: Includes an API endpoint to dynamically create new database partitions for time-series data.


### 🚀 Advanced RDBMS Showcase

This project goes beyond simple CRUD to demonstrate advanced database optimization techniques:

-   **Indexing**: Strategic use of indexes on foreign keys and frequently queried columns to accelerate data retrieval.
-   **Table Partitioning**: The `inventory_movement` table is partitioned by date range (yearly) to showcase significant performance gains on large time-series datasets through **partition pruning**.
-   **SQL Views**: The schema includes a SQL `VIEW` (`vw_stock_valuation`) created via an Alembic migration for generating analytical summaries.

## 🛠️ Tech Stack

| Layer                | Technology                                     |
| -------------------- | ---------------------------------------------- |
| **Backend**          | FastAPI                                        |
| **Database**         | PostgreSQL 14                                  |
| **ORM**              | SQLAlchemy 2.0 (with modern `Mapped` syntax)   |
| **Migrations**       | Alembic                                        |
| **Data Validation**  | Pydantic V2                                    |
| **Containerization** | Docker & Docker Compose                        |

## 🏛️ Project Architecture

The project is structured to enforce separation of concerns, making it easy to maintain and scale.


```
├── smart_inventory
│   ├── alembic
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 271b6be71260_create_initial_product_and_supplier_.py
│   │       ├── 67d297b7c006_add_supplier_table.py
│   │       ├── c3c05607b95b_add_supplier_id_to_product_table.py
│   │       ├── c5650216bf89_add_order_and_order_item_tables.py
│   │       ├── d8fed3de84eb_create_stock_valuation_view.py
│   │       ├── e1791914e43a_create_partitioned_inventory_movement_.py
│   ├── alembic.ini
│   ├── app
│   │   ├── api
│   │   │   ├── deps.py
│   │   │   ├── endpoints
│   │   ├── core
│   │   │   ├── config.py
│   │   ├── crud
│   │   │   ├── crud_maintenance.py
│   │   │   ├── crud_product.py
│   │   │   ├── crud_report.py
│   │   │   ├── crud_supplier.py
│   │   │   ├── __init__.py
│   │   ├── db
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── inventory_movement.py
│   │   │   ├── order.py
│   │   │   ├── product.py
│   │   │   └── supplier.py
│   │   └── schemas
│   │       ├── __init__.py
│   │       ├── maintenance.py
│   │       ├── order.py
│   │       ├── product.py
│   │       └── supplier.py
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   ├── README.md
│   └── requirements.txt


```



## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   Python 3.8+
-   Docker and Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/harshad208/smart_inventory.git
cd smart_inventory
```

### 2. Configure Environment Variables

- Create a .env file in the project root by copying the example file.

```bash
cp example.env .env
```

### 3. Start the Database

- Launch the PostgreSQL database service using Docker Compose.

``` bash
docker-compose up -d
```

### 4. Set Up the Python Environment

- Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate

# On Windows: venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

- Run Alembic to apply all migrations and create the necessary tables, views, and partitions in the database.

```bash
alembic upgrade head
```

### 6. Run the Application

```bash
python -m app.main
```


The server will now be running at http://0.0.0.0:8000.

## 📖 API Usage

- The API includes interactive documentation generated by Swagger UI and ReDoc.
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc


## Example: Create a Product

```bash

curl -X 'POST' \
  'http://127.0.0.1:8000/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sku": "LAPTOP-001",
  "name": "High-Performance Laptop",
  "description": "16GB RAM, 512GB SSD",
  "price": 1299.99,
  "quantity_in_stock": 50
}'

```


## 🔬 Advanced Features Demonstration
### Indexing Performance

- Indexes are used on foreign keys and frequently searched columns (e.g., product.sku). You can see the performance difference using EXPLAIN ANALYZE.
- Without an index, a search would result in a slow Seq Scan:

```bash

EXPLAIN ANALYZE SELECT * FROM product WHERE sku = 'LAPTOP-001';
-- QUERY PLAN -----------------------------------------------------------------
-- Seq Scan on product  (cost=0.00..35.50 rows=1 width=...)
--   Filter: ((sku)::text = 'LAPTOP-001'::text)

```

- With an index, the database performs a highly efficient Index Scan:

```bash
EXPLAIN ANALYZE SELECT * FROM product WHERE sku = 'LAPTOP-001';
-- QUERY PLAN -----------------------------------------------------------------
-- Index Scan using ix_product_sku on product  (cost=0.28..8.29 rows=1 width=...)
--   Index Cond: ((sku)::text = 'LAPTOP-001'::text)
```

## Table Partitioning and Pruning

- The inventory_movement table is partitioned by year. When querying with a date range, PostgreSQL's query planner automatically prunes (ignores) irrelevant partitions.

### Querying for a specific month:

``` bash
EXPLAIN ANALYZE SELECT * FROM inventory_movement WHERE timestamp >= '2024-05-01' AND timestamp < '2024-06-01';
```

Query Plan demonstrating Partition Pruning:
The plan shows that only the inventory_movement_y2024 partition is scanned, while all other yearly partitions are completely ignored.

```bash
-- QUERY PLAN -----------------------------------------------------------------
-- Append  (cost=0.00..59.08 rows=2 width=...)
--   ->  Seq Scan on inventory_movement_y2024  (cost=0.00..59.08 rows=2 width=...)
--         Filter: ((timestamp >= ...))
```

This dramatically improves query speed on very large datasets.

### 📝 Future Enhancements

- Authentication & Authorization: Implement JWT-based security to protect endpoints and define user roles (e.g., admin, manager).
- Unit & Integration Testing: Add a comprehensive test suite using pytest.
- CI/CD Pipeline: Set up a GitHub Actions workflow to automatically run tests and linters on push.
- Background Tasks: Use Celery and Redis for long-running tasks like sending low-stock email alerts.
- Simple Frontend: Build a simple React/Vue dashboard to visualize the inventory data.

### 📄 License

-Distributed under the MIT License. See LICENSE for more information.
# smart_inventory
