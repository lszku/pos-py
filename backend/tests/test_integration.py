"""Integration tests for the POS API."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_user(client: TestClient):
    """Create a test user and return auth token."""
    import uuid

    # Create unique email to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_{unique_id}@example.com"

    # Register a test user
    user_data = {
        "email": email,
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "cashier"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Login to get token
    login_data = {
        "username": email,
        "password": "testpassword123"
    }

    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200

    token_data = response.json()
    return token_data["access_token"]


@pytest.fixture
def auth_headers(test_user):
    """Return headers with authentication token."""
    return {"Authorization": f"Bearer {test_user}"}


class TestProductIntegration:
    """Integration tests for product endpoints."""

    def test_create_and_get_product(self, client: TestClient, auth_headers):
        """Test creating and retrieving a product."""
        # Create product
        product_data = {
            "name": "Test Product",
            "sku": "TP001",
            "description": "A test product",
            "price": "19.99",
            "category": "dog_accessories"
        }

        response = client.post(
            "/products/",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        created_product = response.json()
        assert created_product["name"] == product_data["name"]
        assert created_product["sku"] == product_data["sku"]
        assert created_product["price"] == product_data["price"]

        # Get product by ID
        product_id = created_product["id"]
        response = client.get(
            f"/products/{product_id}",
            headers=auth_headers
        )
        assert response.status_code == 200

        retrieved_product = response.json()
        assert retrieved_product["id"] == product_id
        assert retrieved_product["name"] == product_data["name"]

    def test_get_products_list(self, client: TestClient, auth_headers):
        """Test getting paginated list of products."""
        # Create multiple products
        products_data = [
            {
                "name": "Product 1",
                "sku": "P001",
                "description": "First test product",
                "price": "10.99",
                "category": "dog_accessories"
            },
            {
                "name": "Product 2",
                "sku": "P002",
                "description": "Second test product",
                "price": "15.99",
                "category": "cat_food"
            }
        ]

        for product_data in products_data:
            response = client.post(
                "/products/",
                json=product_data,
                headers=auth_headers
            )
            assert response.status_code == 200

        # Get products list
        response = client.get("/products/", headers=auth_headers)
        assert response.status_code == 200

        products = response.json()
        assert len(products) >= 2

        # Verify products exist
        product_names = [p["name"] for p in products]
        assert "Product 1" in product_names
        assert "Product 2" in product_names

    def test_update_product(self, client: TestClient, auth_headers):
        """Test updating a product."""
        # Create a product first
        product_data = {
            "name": "Original Product",
            "sku": "OP001",
            "description": "Original description",
            "price": "25.99",
            "category": "dog_accessories"
        }

        response = client.post(
            "/products/",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        created_product = response.json()
        product_id = created_product["id"]

        # Update the product
        update_data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": "29.99"
        }

        response = client.put(
            f"/products/{product_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        updated_product = response.json()
        assert updated_product["name"] == update_data["name"]
        assert updated_product["description"] == update_data["description"]
        assert updated_product["price"] == update_data["price"]
        assert updated_product["sku"] == product_data["sku"]  # Should remain unchanged


class TestStockIntegration:
    """Integration tests for stock endpoints."""

    def test_create_and_get_stock(self, client: TestClient, auth_headers):
        """Test creating and retrieving stock entries."""
        # First create a product
        product_data = {
            "name": "Stock Test Product",
            "sku": "STP001",
            "description": "Product for stock testing",
            "price": "12.99",
            "category": "dog_accessories"
        }

        response = client.post(
            "/products/",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        product = response.json()
        product_id = product["id"]

        # Create stock entry
        stock_data = {
            "product_id": product_id,
            "quantity": 50,
            "location": "warehouse",
            "expiry_date": "2024-12-31"
        }

        response = client.post(
            "/stock/",
            json=stock_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        created_stock = response.json()
        assert created_stock["product_id"] == product_id
        assert created_stock["quantity"] == stock_data["quantity"]
        assert created_stock["location"] == stock_data["location"]

        # Get stock by ID
        stock_id = created_stock["id"]
        response = client.get(
            f"/stock/{stock_id}",
            headers=auth_headers
        )
        assert response.status_code == 200

        retrieved_stock = response.json()
        assert retrieved_stock["id"] == stock_id
        assert retrieved_stock["product_id"] == product_id

    def test_get_stock_list(self, client: TestClient, auth_headers):
        """Test getting list of stock entries."""
        # Create a product first
        product_data = {
            "name": "Stock List Product",
            "sku": "SLP001",
            "description": "Product for stock list testing",
            "price": "8.99",
            "category": "cat_food"
        }

        response = client.post(
            "/products/",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        product = response.json()
        product_id = product["id"]

        # Create multiple stock entries
        stock_entries = [
            {
                "product_id": product_id,
                "quantity": 30,
                "location": "warehouse",
                "expiry_date": "2024-12-31"
            },
            {
                "product_id": product_id,
                "quantity": 20,
                "location": "store",
                "expiry_date": "2024-11-30"
            }
        ]

        for stock_data in stock_entries:
            response = client.post(
                "/stock/",
                json=stock_data,
                headers=auth_headers
            )
            assert response.status_code == 200

        # Get stock list
        response = client.get("/stock/", headers=auth_headers)
        assert response.status_code == 200

        stock_list = response.json()
        assert len(stock_list) >= 2

        # Verify stock entries exist
        locations = [s["location"] for s in stock_list]
        assert "warehouse" in locations
        assert "store" in locations


class TestSalesIntegration:
    """Integration tests for sales endpoints."""

    def test_create_sale(self, client: TestClient, auth_headers):
        """Test creating a sale transaction."""
        # First create a product
        product_data = {
            "name": "Sale Test Product",
            "sku": "SATP001",
            "description": "Product for sale testing",
            "price": "15.99",
            "category": "dog_accessories"
        }

        response = client.post(
            "/products/",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        product = response.json()
        product_id = product["id"]

        # Create stock for the product
        stock_data = {
            "product_id": product_id,
            "quantity": 100,
            "location": "store",
            "expiry_date": "2024-12-31"
        }

        response = client.post(
            "/stock/",
            json=stock_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        # Create a sale
        sale_data = {
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                    "unit_price": "15.99"
                }
            ],
            "payment_method": "cash",
            "total_amount": "47.97"
        }

        response = client.post(
            "/sales/",
            json=sale_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        created_sale = response.json()
        assert created_sale["total_amount"] == sale_data["total_amount"]
        assert created_sale["payment_method"] == sale_data["payment_method"]
        assert len(created_sale["items"]) == 1

        sale_item = created_sale["items"][0]
        assert sale_item["product_id"] == product_id
        assert sale_item["quantity"] == 3
        assert sale_item["unit_price"] == "15.99"

    def test_get_sales_list(self, client: TestClient, auth_headers):
        """Test getting list of sales transactions."""
        # Create a product first
        product_data = {
            "name": "Sales List Product",
            "sku": "SLSP001",
            "description": "Product for sales list testing",
            "price": "9.99",
            "category": "cat_food"
        }

        response = client.post(
            "/products/",
            json=product_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        product = response.json()
        product_id = product["id"]

        # Create stock for the product
        stock_data = {
            "product_id": product_id,
            "quantity": 50,
            "location": "store",
            "expiry_date": "2024-12-31"
        }

        response = client.post(
            "/stock/",
            json=stock_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        # Create multiple sales
        sales_data = [
            {
                "items": [
                    {
                        "product_id": product_id,
                        "quantity": 2,
                        "unit_price": "9.99"
                    }
                ],
                "payment_method": "cash",
                "total_amount": "19.98"
            },
            {
                "items": [
                    {
                        "product_id": product_id,
                        "quantity": 1,
                        "unit_price": "9.99"
                    }
                ],
                "payment_method": "card",
                "total_amount": "9.99"
            }
        ]

        for sale_data in sales_data:
            response = client.post(
                "/sales/",
                json=sale_data,
                headers=auth_headers
            )
            assert response.status_code == 200

        # Get sales list
        response = client.get("/sales/", headers=auth_headers)
        assert response.status_code == 200

        sales_list = response.json()
        assert len(sales_list) >= 2

        # Verify sales exist
        payment_methods = [s["payment_method"] for s in sales_list]
        assert "cash" in payment_methods
        assert "card" in payment_methods


class TestAuthenticationIntegration:
    """Integration tests for authentication endpoints."""

    def test_register_and_login(self, client: TestClient):
        """Test user registration and login flow."""
        # Register new user
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "full_name": "New User",
            "role": "cashier"
        }

        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200

        created_user = response.json()
        assert created_user["email"] == user_data["email"]
        assert created_user["full_name"] == user_data["full_name"]
        assert created_user["role"] == user_data["role"]

        # Login with the new user
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }

        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200

        login_response = response.json()
        assert "access_token" in login_response
        assert login_response["token_type"] == "bearer"

    def test_duplicate_registration(self, client: TestClient):
        """Test that duplicate email registration fails."""
        import uuid

        # Create unique email
        unique_id = str(uuid.uuid4())[:8]
        email = f"duplicate_{unique_id}@example.com"

        user_data = {
            "email": email,
            "password": "password123",
            "full_name": "Duplicate User",
            "role": "cashier"
        }

        # First registration should succeed
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200

        # Second registration should fail
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_invalid_login(self, client: TestClient):
        """Test login with invalid credentials."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_protected_endpoints(self, client: TestClient):
        """Test that protected endpoints require authentication."""
        # Try to access protected endpoint without token
        response = client.get("/products/")
        assert response.status_code == 403

        # Try with invalid token
        response = client.get(
            "/products/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
