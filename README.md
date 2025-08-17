# POS-PY: Point of Sale System for Animal Accessories & Food Shop

A modern, full-stack Point of Sale (POS) system built with Python 3.13.5, FastAPI, and Reflex. Designed specifically for managing animal accessories and food retail operations with comprehensive inventory tracking, sales processing, and user management.

## 🚀 Features

### Core POS Functionality
- **User Authentication & Authorization** - JWT-based authentication with role-based access control
- **Product Management** - Complete CRUD operations with categories, SKUs, and pricing
- **Inventory Management** - Real-time stock tracking with low-stock alerts
- **Sales Processing** - Transaction management with multiple payment methods
- **User Management** - Admin panel for user roles and permissions

### Advanced Features
- **Stock Entry State Management** - Save and resume incomplete stock entries
- **Search & Filtering** - Advanced product and inventory search capabilities
- **Reporting** - Stock summaries, sales analytics, and low-stock notifications
- **Google OAuth Integration** - Social authentication (ready for production)
- **Responsive Design** - Modern UI that works on desktop and mobile devices

## 🏗️ Architecture

```
pos-py/
├── backend/                 # FastAPI Backend (Port 8000)
│   ├── app/
│   │   ├── api/            # REST API endpoints
│   │   ├── core/           # Config, security, database
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── repositories/   # Data access layer
│   │   ├── schemas/        # Pydantic validation
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   └── tests/              # Backend tests
├── frontend/               # Reflex Frontend (Port 3000)
│   └── frontend/           # UI components
├── shared/                 # Shared models & utilities
└── docker/                 # PostgreSQL & Redis containers
```

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | FastAPI | Latest |
| **Frontend** | Reflex | 0.8.x |
| **Database** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | Async |
| **Authentication** | JWT + Google OAuth | - |
| **Validation** | Pydantic | V2 |
| **Testing** | Pytest + Testcontainers | - |
| **Linting** | Ruff | - |
| **Type Checking** | MyPy | - |
| **Package Manager** | Poetry | 2.x |

## 📋 Prerequisites

- **Python**: 3.13.5 or higher
- **Poetry**: 2.x for dependency management
- **Docker**: For PostgreSQL and Redis containers
- **Git**: For version control

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pos-py
```

### 2. Install Dependencies

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate the virtual environment
poetry env activate
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://pos_user:pos_password@localhost:5432/pos_db
DATABASE_URL_SYNC=postgresql://pos_user:pos_password@localhost:5432/pos_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth (for production)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Application Settings
DEBUG=true
ENVIRONMENT=development
```

### 4. Start Database Services

```bash
# Start PostgreSQL and Redis containers
docker-compose -f docker/docker-compose.yml up -d

# Verify containers are running
docker ps
```

### 5. Database Setup

```bash
# Navigate to backend directory
cd backend

# Run database migrations
alembic upgrade head

# (Optional) Seed initial data
python -m scripts.seed_data
```

### 6. Start Development Servers

#### Backend (Terminal 1)
```bash
cd backend
poetry env activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Terminal 2)
```bash
cd frontend
poetry shell
reflex run
```

## 🌐 Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on localhost:5432

## 🧪 Testing

### Running Tests

```bash
# Navigate to backend directory
cd backend

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_auth.py -v

# Run integration tests
poetry run pytest tests/test_integration.py -v
```

### Test Structure

- **Unit Tests**: `tests/test_*.py` - Individual component testing
- **Integration Tests**: `tests/test_integration.py` - End-to-end workflow testing
- **API Tests**: HTTP endpoint testing with TestClient
- **Database Tests**: Testcontainers for isolated database testing

## 🔧 Development Workflow

### 1. Code Quality Tools

```bash
# Format code with Ruff
poetry run ruff format .

# Lint code with Ruff
poetry run ruff check .

# Type checking with MyPy
poetry run mypy .

# Run all quality checks
poetry run pre-commit run --all-files
```

### 2. Database Migrations

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### 3. API Development

#### Adding New Endpoints

1. **Create Schema** (`app/schemas/`)
```python
from pydantic import BaseModel

class NewEntityCreate(BaseModel):
    name: str
    description: str
```

2. **Add Repository** (`app/repositories/`)
```python
class NewEntityRepository(BaseRepository[NewEntity]):
    async def get_by_name(self, name: str) -> Optional[NewEntity]:
        # Implementation
```

3. **Create Service** (`app/services/`)
```python
class NewEntityService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = NewEntityRepository(session)
    
    async def create_entity(self, data: NewEntityCreate) -> dict:
        # Business logic
```

4. **Add API Routes** (`app/api/`)
```python
@router.post("/", response_model=NewEntityResponse)
async def create_entity(
    data: NewEntityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = NewEntityService(db)
    return await service.create_entity(data)
```

### 4. Frontend Development

#### Adding New Pages

1. **Update State** (`frontend/frontend/frontend.py`)
```python
class State(rx.State):
    # Add new state variables
    new_data: List[Dict[str, Any]] = []
    
    def load_new_data(self):
        # Load data logic
```

2. **Create Page Component**
```python
def new_page() -> rx.Component:
    return rx.container(
        rx.heading("New Page"),
        # Component content
    )
```

3. **Add Navigation**
```python
def main_content() -> rx.Component:
    return rx.cond(
        State.current_page == "new_page",
        new_page(),
        # Other pages
    )
```

## 📁 Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── auth.py            # Authentication routes
│   │   ├── products.py        # Product management
│   │   ├── sales.py           # Sales transactions
│   │   └── stock.py           # Inventory management
│   ├── core/                  # Core configuration
│   │   ├── config.py          # Settings management
│   │   ├── database.py        # Database connection
│   │   └── security.py        # JWT authentication
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py            # User model
│   │   ├── product.py         # Product model
│   │   ├── stock.py           # Stock model
│   │   └── sale.py            # Sale model
│   ├── repositories/          # Data access layer
│   │   ├── base.py            # Base repository
│   │   ├── user.py            # User repository
│   │   ├── product.py         # Product repository
│   │   ├── stock.py           # Stock repository
│   │   └── sale.py            # Sale repository
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py            # Authentication schemas
│   │   ├── product.py         # Product schemas
│   │   ├── stock.py           # Stock schemas
│   │   └── sale.py            # Sale schemas
│   ├── services/              # Business logic
│   │   ├── auth.py            # Authentication service
│   │   ├── product.py         # Product service
│   │   ├── stock.py           # Stock service
│   │   └── sale.py            # Sale service
│   └── main.py                # FastAPI application
├── alembic/                   # Database migrations
├── tests/                     # Test suite
└── requirements.txt           # Dependencies
```

### Frontend Structure

```
frontend/
├── frontend/
│   ├── frontend.py            # Main application
│   └── api_client.py          # API communication
├── rxconfig.py                # Reflex configuration
└── requirements.txt           # Dependencies
```

## 🔐 Authentication & Security

### JWT Authentication

The application uses JWT tokens for authentication:

1. **Login**: POST `/auth/login` with email/password
2. **Token**: Returns JWT access token
3. **Authorization**: Include token in `Authorization: Bearer <token>` header

### Role-Based Access Control

- **CASHIER**: Basic sales and inventory operations
- **MANAGER**: Full access to all features
- **ADMIN**: User management and system configuration

### Google OAuth

Google OAuth integration is implemented and ready for production:

1. Configure Google OAuth credentials in `.env`
2. Update `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
3. Implement token verification in `AuthService.verify_google_token()`

## 🗄️ Database Schema

### Core Tables

- **users**: User accounts and authentication
- **products**: Product catalog with categories
- **stock**: Inventory tracking with locations
- **sales**: Transaction records
- **sale_items**: Individual items in sales

### Key Relationships

- Products have multiple stock entries
- Sales contain multiple sale items
- Users create stock entries and sales
- Stock entries track product quantities by location

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
```bash
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
SECRET_KEY=secure-secret-key
```

2. **Database Migration**
```bash
alembic upgrade head
```

3. **Static Files**
```bash
reflex export
```

4. **Docker Deployment**
```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

### Docker Configuration

The project includes Docker configurations for:
- PostgreSQL database
- Redis cache
- Production-ready deployment

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

2. **Database Connection Issues**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart containers
docker-compose -f docker/docker-compose.yml restart
```

3. **Migration Errors**
```bash
# Reset database
alembic downgrade base
alembic upgrade head
```

4. **Frontend Build Issues**
```bash
# Clear Reflex cache
rm -rf .web/
reflex run
```

### Debug Mode

Enable debug mode in `.env`:
```bash
DEBUG=true
```

This will provide detailed error messages and SQL query logging.

## 📚 API Documentation

### Authentication Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info
- `POST /auth/google` - Google OAuth authentication

### Product Endpoints

- `GET /products/` - List products (paginated)
- `POST /products/` - Create product
- `GET /products/{id}` - Get product by ID
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Stock Endpoints

- `GET /stock/` - List stock entries
- `POST /stock/` - Create stock entry
- `GET /stock/{id}` - Get stock entry by ID
- `PUT /stock/{id}` - Update stock entry
- `GET /stock/available/{product_id}` - Get available stock

### Sales Endpoints

- `GET /sales/` - List sales transactions
- `POST /sales/` - Create sale transaction
- `GET /sales/{id}` - Get sale by ID
- `GET /sales/total` - Get total sales statistics

## 🤝 Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 and use Ruff for formatting
2. **Type Hints**: Use type hints throughout the codebase
3. **Documentation**: Add docstrings to all functions and classes
4. **Testing**: Write tests for new features
5. **Commits**: Use conventional commit messages

### Pull Request Process

1. Create a feature branch from `main`
2. Implement changes with tests
3. Run all quality checks
4. Submit pull request with description
5. Code review and approval
6. Merge to main branch

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check existing issues in the repository
4. Create a new issue with detailed information

## 🎯 Roadmap

### Planned Features

- [ ] Real-time inventory updates
- [ ] Advanced reporting dashboard
- [ ] Barcode scanning integration
- [ ] Multi-location support
- [ ] Customer management
- [ ] Loyalty program
- [ ] Email notifications
- [ ] Mobile app

### Performance Optimizations

- [ ] Database query optimization
- [ ] Caching implementation
- [ ] API response compression
- [ ] Frontend bundle optimization

---

**Happy Coding! 🐾**

This POS system is designed to help you manage your animal accessories and food shop efficiently. The modular architecture makes it easy to extend and customize for your specific needs. 