# POS Application Design Document

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Implementation Phases](#implementation-phases)
5. [Database Design](#database-design)
6. [API Design](#api-design)
7. [Authentication & Security](#authentication--security)
8. [Frontend Design](#frontend-design)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Strategy](#deployment-strategy)
11. [Performance Considerations](#performance-considerations)
12. [Security Considerations](#security-considerations)
13. [Tradeoffs & Decisions](#tradeoffs--decisions)
14. [Current Status](#current-status)
15. [TODOs & Next Steps](#todos--next-steps)
16. [Development Guidelines](#development-guidelines)

## Project Overview

### Purpose
A Point of Sale (POS) application designed for selling animal accessories and food in a retail environment. The system provides comprehensive inventory management, sales tracking, and user authentication capabilities.

### Key Features
- **Product Management**: CRUD operations for products with categories and pricing
- **Inventory Management**: Stock tracking with location-based inventory
- **Sales Processing**: Transaction management with multiple payment methods
- **User Authentication**: JWT-based authentication with Google OAuth support
- **Role-based Access**: Different user roles (admin, cashier, manager)
- **Reporting**: Sales analytics and inventory reports

### Target Users
- **Store Owners**: Full access to all features and reports
- **Cashiers**: Sales processing and basic inventory queries
- **Managers**: Inventory management and sales oversight

## Architecture Overview

### Modular Architecture
The application follows a modular architecture with clear separation of concerns:

```
pos-py/
├── backend/           # FastAPI backend application
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Core configuration and utilities
│   │   ├── models/    # SQLAlchemy database models
│   │   ├── repositories/ # Data access layer
│   │   ├── schemas/   # Pydantic validation schemas
│   │   └── services/  # Business logic layer
│   ├── tests/         # Backend tests
│   └── alembic/       # Database migrations
├── frontend/          # Reflex frontend application
│   ├── frontend/      # UI components and pages
│   └── tests/         # Frontend tests
├── shared/            # Shared code between frontend and backend
│   └── models/        # Shared enums and models
└── docker/            # Docker configuration
```

### Design Patterns
- **Repository Pattern**: Data access abstraction
- **Service Layer Pattern**: Business logic encapsulation
- **Dependency Injection**: FastAPI's dependency system
- **Model-View-Controller**: Frontend architecture with Reflex

## Technology Stack

### Backend
- **Python 3.13.5**: Latest Python version for performance and features
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy 2.0**: Modern ORM with async support
- **PostgreSQL**: Production-ready relational database
- **Alembic**: Database migration management
- **Pydantic**: Data validation and serialization
- **JWT**: Token-based authentication
- **Poetry**: Dependency management and packaging

### Frontend
- **Reflex 0.8.x**: Python-based web framework for full-stack development
- **Tailwind CSS**: Utility-first CSS framework
- **HTTpx**: Async HTTP client for API communication

### Development Tools
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pytest**: Testing framework with async support
- **Testcontainers**: Integration testing with real databases
- **Docker**: Containerization for development and deployment

### Database
- **PostgreSQL**: Primary database for production
- **SQLite**: In-memory database for testing
- **Redis**: Caching and session storage (planned)

## Implementation Phases

### Phase 1: Foundation & Setup ✅ COMPLETED
**Duration**: 1-2 weeks
**Status**: ✅ Complete

**Objectives**:
- Project structure setup
- Development environment configuration
- Basic database models
- Authentication foundation

**Deliverables**:
- [x] Project structure with modular architecture
- [x] Poetry dependency management
- [x] Docker development environment
- [x] Basic user authentication with JWT
- [x] Database models for core entities
- [x] Repository pattern implementation
- [x] Basic API endpoints

**Key Decisions**:
- Chose FastAPI over Django for better async support and automatic API docs
- Selected PostgreSQL for production and SQLite for testing
- Implemented repository pattern for data access abstraction
- Used Pydantic for schema validation and serialization

### Phase 2: Core Backend Development ✅ COMPLETED
**Duration**: 2-3 weeks
**Status**: ✅ Complete

**Objectives**:
- Complete backend API implementation
- Database migrations
- Comprehensive testing

**Deliverables**:
- [x] Complete CRUD operations for all entities
- [x] Database migrations with Alembic
- [x] Service layer implementation
- [x] Comprehensive unit and integration tests
- [x] API documentation with OpenAPI/Swagger
- [x] Error handling and validation

**Key Decisions**:
- Used async/await throughout for better performance
- Implemented comprehensive test coverage with Testcontainers
- Chose UUID primary keys for better scalability
- Used Decimal for monetary values to avoid floating-point precision issues

### Phase 3: API Implementation ✅ COMPLETED
**Duration**: 1-2 weeks
**Status**: ✅ Complete

**Objectives**:
- Product management API
- Stock management API
- Sales API
- Google OAuth integration

**Deliverables**:
- [x] Product CRUD with pagination and search
- [x] Stock management with location tracking
- [x] Sales processing with itemized transactions
- [x] Google OAuth authentication (mock implementation)
- [x] Protected endpoints with role-based access
- [x] Comprehensive API testing

**Key Decisions**:
- Implemented pagination for large datasets
- Used enum-based categories for products
- Designed flexible stock location system
- Created comprehensive sales transaction model

### Phase 4: Frontend Development 🔄 IN PROGRESS
**Duration**: 2-3 weeks
**Status**: 🔄 Partially Complete

**Objectives**:
- Modern web interface
- Authentication UI
- Product and inventory management
- Sales interface

**Deliverables**:
- [x] Basic Reflex application setup
- [x] Authentication UI components
- [x] Product management interface (basic)
- [ ] Complete stock management UI
- [ ] Sales processing interface
- [ ] Dashboard and reporting views
- [ ] Responsive design implementation

**Key Decisions**:
- Chose Reflex for Python-based full-stack development
- Implemented component-based architecture
- Used Tailwind CSS for styling
- Designed mobile-first responsive layout

### Phase 5: Integration & Testing 🔄 IN PROGRESS
**Duration**: 1-2 weeks
**Status**: 🔄 Partially Complete

**Objectives**:
- End-to-end testing
- Performance optimization
- Security hardening
- Documentation

**Deliverables**:
- [x] Backend integration tests
- [ ] Frontend integration tests
- [ ] End-to-end workflow testing
- [ ] Performance benchmarking
- [ ] Security audit and fixes
- [ ] Complete API documentation
- [ ] User guides and deployment instructions

## Database Design

### Entity Relationship Diagram

```
User (1) ----< Sale (N)
User (1) ----< StockEntry (N)
Product (1) ----< Stock (N)
Product (1) ----< SaleItem (N)
Sale (1) ----< SaleItem (N)
```

### Core Tables

#### Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role UserRole NOT NULL DEFAULT 'cashier',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Products
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category ProductCategory NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Stock
```sql
CREATE TABLE stock (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 0,
    location VARCHAR(100) NOT NULL,
    status StockStatus DEFAULT 'available',
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Sales
```sql
CREATE TABLE sales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reference VARCHAR(100) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    final_amount DECIMAL(10,2) NOT NULL,
    status SaleStatus DEFAULT 'pending',
    payment_method VARCHAR(50),
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

#### Sale Items
```sql
CREATE TABLE sale_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sale_id UUID REFERENCES sales(id),
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Indexes
- Email index on users table
- SKU index on products table
- Product_id index on stock table
- Sale_id index on sale_items table
- Created_at indexes for reporting queries

## API Design

### RESTful Endpoints

#### Authentication
```
POST /auth/register     # User registration
POST /auth/login        # User login
POST /auth/google       # Google OAuth
GET  /auth/me           # Get current user
```

#### Products
```
GET    /products/           # List products (paginated)
POST   /products/           # Create product
GET    /products/{id}       # Get product
PUT    /products/{id}       # Update product
DELETE /products/{id}       # Delete product
GET    /products/search     # Search products
```

#### Stock
```
GET    /stock/              # List stock items
POST   /stock/              # Create stock entry
GET    /stock/{id}          # Get stock item
PUT    /stock/{id}          # Update stock
GET    /stock/low-stock     # Get low stock items
GET    /stock/product/{id}  # Get stock by product
```

#### Sales
```
GET    /sales/              # List sales
POST   /sales/              # Create sale
GET    /sales/{id}          # Get sale
PUT    /sales/{id}          # Update sale
GET    /sales/stats/total   # Sales statistics
```

### Response Formats

#### Standard Response
```json
{
    "id": "uuid",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Error Response

```json
{
    "detail": "Error message",
    "status_code": 400
}
```

#### Paginated Response

```json
{
    "items": [...],
    "total": 100,
    "page": 1,
    "size": 20,
    "pages": 5
}
```

## Authentication & Security

### JWT Implementation
- **Algorithm**: HS256
- **Expiration**: 30 minutes (access token)
- **Refresh Token**: 7 days (planned)
- **Secret**: Environment variable

### Google OAuth
- **Status**: Mock implementation ready
- **Integration**: Google OAuth 2.0
- **Scopes**: email, profile
- **User Creation**: Automatic on first login

### Role-based Access Control
```python
class UserRole(str, Enum):
    ADMIN = "admin"      # Full access
    MANAGER = "manager"  # Inventory and sales management
    CASHIER = "cashier"  # Sales processing only
```

### Security Measures
- Password hashing with bcrypt
- JWT token validation
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Rate limiting (planned)

## Frontend Design

### Component Architecture
```
App/
├── Layout/
│   ├── Header
│   ├── Sidebar
│   └── Footer
├── Pages/
│   ├── Login
│   ├── Dashboard
│   ├── Products
│   ├── Stock
│   └── Sales
├── Components/
│   ├── Forms/
│   ├── Tables/
│   ├── Modals/
│   └── Charts/
└── State/
    ├── Auth
    ├── Products
    ├── Stock
    └── Sales
```

### State Management
- Reflex built-in state management
- API client for backend communication
- Local storage for user preferences
- Real-time updates (planned)

### UI/UX Design
- **Design System**: Custom component library
- **Responsive**: Mobile-first approach
- **Accessibility**: WCAG 2.1 compliance
- **Performance**: Lazy loading and optimization

## Testing Strategy

### Test Pyramid
```
    /\
   /  \     E2E Tests (Few)
  /____\    
 /      \   Integration Tests (Some)
/________\  Unit Tests (Many)
```

### Test Types

#### Unit Tests ✅
- **Coverage**: 90%+ target
- **Framework**: Pytest
- **Scope**: Individual functions and classes
- **Mocking**: External dependencies

#### Integration Tests ✅
- **Framework**: Pytest with Testcontainers
- **Database**: Real PostgreSQL in containers
- **Scope**: API endpoints and database operations
- **Coverage**: All CRUD operations

#### End-to-End Tests 🔄
- **Framework**: Playwright (planned)
- **Scope**: Complete user workflows
- **Coverage**: Critical business paths

### Test Data Management
- **Factories**: Pytest-factoryboy for test data
- **Fixtures**: Reusable test setup
- **Cleanup**: Automatic database cleanup
- **Isolation**: Each test runs in isolation

## Deployment Strategy

### Development Environment
- **Docker Compose**: Local development
- **Hot Reload**: FastAPI and Reflex development servers
- **Database**: PostgreSQL with persistent volumes
- **Redis**: Caching and session storage

### Production Environment
- **Containerization**: Docker containers
- **Orchestration**: Kubernetes (planned)
- **Database**: Managed PostgreSQL service
- **Caching**: Redis cluster
- **Load Balancing**: Nginx reverse proxy
- **SSL**: Let's Encrypt certificates

### CI/CD Pipeline
- **Version Control**: Git with feature branches
- **Testing**: Automated test suite
- **Code Quality**: Ruff and MyPy checks
- **Deployment**: Automated deployment on merge
- **Monitoring**: Application and infrastructure monitoring

## Performance Considerations

### Database Optimization
- **Indexing**: Strategic indexes for common queries
- **Connection Pooling**: SQLAlchemy connection pooling
- **Query Optimization**: Efficient queries with proper joins
- **Caching**: Redis caching for frequently accessed data

### API Performance
- **Async Operations**: Full async/await implementation
- **Pagination**: Efficient pagination for large datasets
- **Compression**: Gzip compression for responses
- **Caching**: HTTP caching headers

### Frontend Performance
- **Code Splitting**: Lazy loading of components
- **Bundle Optimization**: Tree shaking and minification
- **Image Optimization**: Compressed images and lazy loading
- **CDN**: Static asset delivery

## Security Considerations

### Data Protection
- **Encryption**: Data encryption at rest and in transit
- **Backup**: Regular encrypted backups
- **Access Control**: Role-based access control
- **Audit Logging**: Comprehensive audit trails

### Application Security
- **Input Validation**: Comprehensive input validation
- **SQL Injection**: Prevention through ORM
- **XSS Protection**: Content Security Policy
- **CSRF Protection**: Token-based CSRF protection

### Infrastructure Security
- **Network Security**: VPC and firewall rules
- **Secrets Management**: Environment-based secrets
- **Updates**: Regular security updates
- **Monitoring**: Security event monitoring

## Tradeoffs & Decisions

### Technology Choices

#### FastAPI vs Django
**Decision**: FastAPI
**Pros**:
- Better async support
- Automatic API documentation
- Modern Python features
- Better performance

**Cons**:
- Smaller ecosystem
- Less built-in features
- Steeper learning curve

#### PostgreSQL vs MySQL
**Decision**: PostgreSQL
**Pros**:
- Better JSON support
- Advanced features (UUID, JSONB)
- Better performance for complex queries
- ACID compliance

**Cons**:
- Higher resource usage
- More complex setup

#### Reflex vs React/Vue
**Decision**: Reflex
**Pros**:
- Python-based full-stack development
- Shared code between frontend and backend
- Faster development for Python developers
- Built-in state management

**Cons**:
- Smaller ecosystem
- Less mature than React/Vue
- Limited third-party components

### Architecture Decisions

#### Repository Pattern
**Decision**: Implemented
**Pros**:
- Data access abstraction
- Easier testing
- Better separation of concerns
- Database agnostic

**Cons**:
- Additional complexity
- More boilerplate code

#### Async/Await
**Decision**: Full async implementation
**Pros**:
- Better performance
- Scalability
- Modern Python approach

**Cons**:
- More complex code
- Debugging challenges

#### UUID Primary Keys
**Decision**: Used throughout
**Pros**:
- Better scalability
- No sequential guessing
- Distributed system friendly

**Cons**:
- Larger storage requirements
- Slightly slower joins

## Current Status

### Completed Features ✅
- [x] Project foundation and architecture
- [x] User authentication with JWT
- [x] Product management (CRUD)
- [x] Stock management (CRUD)
- [x] Sales processing (CRUD)
- [x] Database migrations
- [x] Comprehensive backend testing
- [x] API documentation
- [x] Basic frontend setup
- [x] Code quality tools (Ruff, MyPy)

### In Progress 🔄
- [ ] Complete frontend implementation
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security hardening

### Not Started ⏳
- [ ] Google OAuth integration
- [ ] Advanced reporting
- [ ] Real-time features
- [ ] Mobile app
- [ ] Production deployment

## TODOs & Next Steps

### Immediate Priorities (Next 2-4 weeks)

#### 1. Complete Frontend Implementation
**Priority**: High
**Effort**: 2-3 weeks
**Tasks**:
- [ ] Complete product management UI
- [ ] Implement stock management interface
- [ ] Build sales processing interface
- [ ] Create dashboard with analytics
- [ ] Add responsive design
- [ ] Implement error handling and loading states

#### 2. End-to-End Testing
**Priority**: High
**Effort**: 1-2 weeks
**Tasks**:
- [ ] Set up Playwright for E2E testing
- [ ] Create test scenarios for critical workflows
- [ ] Implement visual regression testing
- [ ] Add performance testing
- [ ] Create test data management strategy

#### 3. Google OAuth Integration
**Priority**: Medium
**Effort**: 1 week
**Tasks**:
- [ ] Set up Google OAuth credentials
- [ ] Implement OAuth flow in backend
- [ ] Create OAuth UI components
- [ ] Add user profile management
- [ ] Test OAuth integration

### Medium-term Goals (Next 1-3 months)

#### 4. Advanced Features
**Priority**: Medium
**Effort**: 2-4 weeks
**Tasks**:
- [ ] Real-time inventory updates
- [ ] Advanced reporting and analytics
- [ ] Barcode scanning integration
- [ ] Receipt printing
- [ ] Customer management
- [ ] Discount and promotion system

#### 5. Performance Optimization
**Priority**: Medium
**Effort**: 1-2 weeks
**Tasks**:
- [ ] Database query optimization
- [ ] Redis caching implementation
- [ ] Frontend bundle optimization
- [ ] API response optimization
- [ ] Load testing and benchmarking

#### 6. Security Hardening
**Priority**: High
**Effort**: 1-2 weeks
**Tasks**:
- [ ] Security audit and penetration testing
- [ ] Implement rate limiting
- [ ] Add audit logging
- [ ] Enhance input validation
- [ ] Security headers implementation

### Long-term Goals (Next 3-6 months)

#### 7. Production Deployment
**Priority**: High
**Effort**: 2-4 weeks
**Tasks**:
- [ ] Set up production infrastructure
- [ ] Implement CI/CD pipeline
- [ ] Configure monitoring and logging
- [ ] Set up backup and disaster recovery
- [ ] Performance monitoring

#### 8. Mobile Application
**Priority**: Low
**Effort**: 8-12 weeks
**Tasks**:
- [ ] Design mobile UI/UX
- [ ] Implement React Native app
- [ ] API integration
- [ ] Offline functionality
- [ ] Push notifications

#### 9. Advanced Analytics
**Priority**: Low
**Effort**: 4-6 weeks
**Tasks**:
- [ ] Business intelligence dashboard
- [ ] Sales forecasting
- [ ] Inventory optimization
- [ ] Customer analytics
- [ ] Financial reporting

### Technical Debt & Improvements

#### Code Quality
- [ ] Improve type annotations coverage
- [ ] Add more comprehensive error handling
- [ ] Implement logging strategy
- [ ] Add API versioning
- [ ] Improve documentation

#### Architecture Improvements
- [ ] Implement event-driven architecture
- [ ] Add message queue for background tasks
- [ ] Implement microservices architecture (if needed)
- [ ] Add API gateway
- [ ] Implement circuit breaker pattern

## Development Guidelines

### Code Standards
- **Python**: PEP 8 with Black formatting
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Docstrings for all functions
- **Testing**: Minimum 90% code coverage
- **Linting**: Ruff for linting and formatting

### Git Workflow
- **Branching**: Feature branch workflow
- **Commits**: Conventional commit messages
- **Pull Requests**: Required for all changes
- **Code Review**: Mandatory for all PRs
- **CI/CD**: Automated testing and deployment

### Development Process
- **Planning**: Feature planning and estimation
- **Development**: TDD approach with comprehensive testing
- **Review**: Code review and testing
- **Deployment**: Staging and production deployment
- **Monitoring**: Performance and error monitoring

### Documentation
- **API Documentation**: OpenAPI/Swagger
- **Code Documentation**: Inline comments and docstrings
- **User Documentation**: User guides and tutorials
- **Technical Documentation**: Architecture and deployment guides

---

## Conclusion

This POS application provides a solid foundation for a modern retail management system. The modular architecture, comprehensive testing, and modern technology stack ensure scalability, maintainability, and reliability. The phased implementation approach allows for iterative development and continuous improvement.

The next phase focuses on completing the frontend implementation and end-to-end testing, followed by production deployment and advanced feature development. The project is well-positioned for long-term success with clear development guidelines and a comprehensive roadmap.
