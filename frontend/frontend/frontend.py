"""POS Application - Point of Sale system for animal accessories and food shop."""

import reflex as rx
from typing import Optional, List, Dict, Any

from rxconfig import config


class State(rx.State):
    """The app state."""
    
    # Authentication
    is_authenticated: bool = False
    current_user: Optional[Dict[str, Any]] = None
    
    # Products
    products: List[Dict[str, Any]] = []
    product_loading: bool = False
    
    # Stock
    stock_items: List[Dict[str, Any]] = []
    stock_loading: bool = False
    
    # UI State
    current_page: str = "login"
    login_error: str = ""
    
    # Form data
    login_email: str = ""
    login_password: str = ""
    
    def handle_email_change(self, value: str):
        """Handle email input change."""
        self.login_email = value
    
    def handle_password_change(self, value: str):
        """Handle password input change."""
        self.login_password = value
    
    def handle_login(self):
        """Handle login form submission."""
        if not self.login_email or not self.login_password:
            self.login_error = "Please enter both email and password"
            return
        
        # For demo purposes, accept any login
        # In production, this would call the real API
        self.login_error = ""
        self.is_authenticated = True
        self.current_page = "dashboard"
        self.current_user = {
            "full_name": "Demo User",
            "email": self.login_email,
            "role": "cashier"
        }
    
    def logout(self):
        """Logout user."""
        self.is_authenticated = False
        self.current_user = None
        self.current_page = "login"
        self.login_email = ""
        self.login_password = ""
        self.login_error = ""
    
    def load_products(self):
        """Load products from API."""
        # Demo data for now - in production this would call the real API
        self.product_loading = True
        self.products = [
            {
                "id": "1",
                "name": "Dog Collar",
                "sku": "DC001",
                "category": "accessories",
                "price": 15.99
            },
            {
                "id": "2", 
                "name": "Cat Food Premium",
                "sku": "CF001",
                "category": "food",
                "price": 25.50
            },
            {
                "id": "3",
                "name": "Bird Cage",
                "sku": "BC001", 
                "category": "accessories",
                "price": 89.99
            }
        ]
        self.product_loading = False
    
    def load_stock(self):
        """Load stock items from API."""
        # Demo data for now - in production this would call the real API
        self.stock_loading = True
        self.stock_items = [
            {
                "id": "1",
                "product_name": "Dog Collar",
                "quantity": 50,
                "location": "Warehouse A"
            },
            {
                "id": "2",
                "product_name": "Cat Food Premium", 
                "quantity": 25,
                "location": "Warehouse B"
            },
            {
                "id": "3",
                "product_name": "Bird Cage",
                "quantity": 10,
                "location": "Warehouse A"
            }
        ]
        self.stock_loading = False
    
    def navigate_to(self, page: str):
        """Navigate to a specific page."""
        self.current_page = page
        
        # Load data for specific pages
        if page == "products":
            self.load_products()
        elif page == "stock":
            self.load_stock()


def login_page() -> rx.Component:
    """Login page component."""
    return rx.container(
        rx.vstack(
            rx.heading("POS System Login", size="6"),
            rx.cond(
                State.login_error != "",
                rx.text(State.login_error, color="red"),
                rx.text(""),
            ),
            rx.vstack(
                rx.input(
                    placeholder="Email",
                    value=State.login_email,
                    on_change=State.handle_email_change,
                    type_="email",
                ),
                rx.input(
                    placeholder="Password",
                    value=State.login_password,
                    on_change=State.handle_password_change,
                    type_="password",
                ),
                rx.button("Login", on_click=State.handle_login),
                spacing="4",
            ),
            rx.text("Demo: Use any email/password to test"),
            spacing="6",
            justify="center",
            min_height="100vh",
        ),
        max_width="400px",
    )


def dashboard() -> rx.Component:
    """Dashboard page component."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("POS Dashboard", size="6"),
                rx.spacer(),
                rx.button("Logout", on_click=State.logout),
                width="100%",
            ),
            rx.cond(
                State.current_user,
                rx.text(f"Welcome, {State.current_user.get('full_name', 'User')}!"),
                rx.text("Welcome to POS System!"),
            ),
            rx.hstack(
                rx.button(
                    "Products",
                    on_click=lambda: State.navigate_to("products"),
                ),
                rx.button(
                    "Stock",
                    on_click=lambda: State.navigate_to("stock"),
                ),
                rx.button(
                    "Sales",
                    on_click=lambda: State.navigate_to("sales"),
                ),
                spacing="4",
            ),
            spacing="6",
            width="100%",
        ),
        max_width="800px",
        padding="6",
    )


def products_page() -> rx.Component:
    """Products page component."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Products", size="6"),
                rx.spacer(),
                rx.button("Add Product"),
                rx.button("Back", on_click=lambda: State.navigate_to("dashboard")),
                width="100%",
            ),
            rx.cond(
                State.product_loading,
                rx.spinner(),
                rx.cond(
                    len(State.products) > 0,
                    rx.vstack(
                        rx.foreach(
                            State.products,
                            lambda product: rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(product["name"], font_weight="bold"),
                                        rx.text(f"SKU: {product['sku']}"),
                                        rx.text(f"Category: {product['category']}"),
                                        rx.text(f"Price: ${product['price']:.2f}"),
                                        align_items="start",
                                    ),
                                    rx.spacer(),
                                    rx.button("Edit", size="sm"),
                                    width="100%",
                                ),
                                padding="4",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                            )
                        ),
                        spacing="4",
                    ),
                    rx.text("No products found. Add some products to get started."),
                ),
            ),
            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="6",
    )


def stock_page() -> rx.Component:
    """Stock page component."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Stock Management", size="6"),
                rx.spacer(),
                rx.button("Add Stock Entry"),
                rx.button("Back", on_click=lambda: State.navigate_to("dashboard")),
                width="100%",
            ),
            rx.cond(
                State.stock_loading,
                rx.spinner(),
                rx.cond(
                    len(State.stock_items) > 0,
                    rx.vstack(
                        rx.foreach(
                            State.stock_items,
                            lambda stock: rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(stock.get("product_name", "Unknown"), font_weight="bold"),
                                        rx.text(f"Quantity: {stock['quantity']}"),
                                        rx.text(f"Location: {stock.get('location', 'N/A')}"),
                                        align_items="start",
                                    ),
                                    rx.spacer(),
                                    rx.button("Edit", size="sm"),
                                    width="100%",
                                ),
                                padding="4",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                            )
                        ),
                        spacing="4",
                    ),
                    rx.text("No stock items found. Add some stock to get started."),
                ),
            ),
            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="6",
    )


def sales_page() -> rx.Component:
    """Sales page component."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("Sales", size="6"),
                rx.spacer(),
                rx.button("New Sale"),
                rx.button("Back", on_click=lambda: State.navigate_to("dashboard")),
                width="100%",
            ),
            rx.text("Sales transactions will be displayed here"),
            rx.text("Features: Create sales, view history"),
            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="6",
    )


def main_content() -> rx.Component:
    """Main content based on current page."""
    return rx.cond(
        State.current_page == "login",
        login_page(),
        rx.cond(
            State.current_page == "dashboard",
            dashboard(),
            rx.cond(
                State.current_page == "products",
                products_page(),
                rx.cond(
                    State.current_page == "stock",
                    stock_page(),
                    rx.cond(
                        State.current_page == "sales",
                        sales_page(),
                        dashboard(),  # Default fallback
                    ),
                ),
            ),
        ),
    )


def index() -> rx.Component:
    """Main page component."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        main_content(),
        width="100%",
        max_width="100%",
    )


app = rx.App()
app.add_page(index)
