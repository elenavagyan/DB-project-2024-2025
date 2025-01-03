# Database Interface with FastAPI

This project is a **database interface application** built using **FastAPI**. It provides RESTful API endpoints for managing products, customers, and purchases. The application is containerized using **Docker**, with the Docker configuration located in the `docker` directory and all application logic in the `app` directory.

---

## 📁 Project Structure

```
├── app
│   ├── api.py
│   ├── data.py
│   ├── main.py
│   ├── models.py
│   └── session.py
└── docker
    └── docker-compose.yaml
```

- **`app`**: Contains all the Python files for the FastAPI application.
- **`docker`**: Contains the Docker configuration files for containerizing the application.

---

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
- **Docker**
- **Docker Compose**
- **Python 3.8+**

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 3️⃣ Start the Docker Containers
Navigate to the `docker` directory and run the following command to start the PostgreSQL database container:

```bash
docker-compose up -d
```

This will:
- Start a **PostgreSQL** database on port **5432**.
- Create a database named **`sales_office`**.

---

## 🚀 Running the FastAPI Application

After setting up the database, navigate to the `app` directory and run the following command to start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at **`http://localhost:8000`**.

---

## 📚 API Endpoints

### Products
- **POST** `/products/` - Create a new product.
- **GET** `/products/{product_id}` - Retrieve a product by its ID.
- **GET** `/products/` - List all products.

### Customers
- **POST** `/customers/` - Create a new customer.
- **GET** `/customers/{customer_id}` - Retrieve a customer by their ID.
- **GET** `/customers/` - List all customers.

### Purchases
- **POST** `/purchases/` - Create a new purchase.
- **GET** `/purchases/{purchase_id}` - Retrieve a purchase by its ID.
- **GET** `/purchases/` - List all purchases.

### Analytics
- **GET** `/analytics/customer-purchases/{customer_id}` - Get all purchases made by a specific customer.
- **GET** `/analytics/product-sales/{product_id}` - Get sales statistics for a specific product.

---

## ⚙️ Database Configuration

The database connection is configured in **`session.py`**:
```python
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="1453",
    host="localhost",
    database="sales_office",
    port=5432
)
```

---

## 📂 Docker Configuration

The **`docker-compose.yaml`** file sets up a **PostgreSQL** container:
```yaml
services:
  db:
    container_name: postgres
    image: postgres
    restart: always
    environment:
      POSTGRES_DB: sales_office
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 1453
    ports:
      - "5432:5432"
volumes:
  db-data:
```

---

## 🧪 Sample Data Generation

The **`data.py`** file includes helper functions for generating sample data, such as random company names, product names, and addresses.

---

## 🛠️ Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your branch.
5. Submit a pull request.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 💻 Author

Developed by **Elen Avagyan**.
