import reflex as rx

config = rx.Config(
    app_name="pos_ui",
    backend_port=8001,  # Use different port to avoid conflict with FastAPI backend
    frontend_port=3000,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)