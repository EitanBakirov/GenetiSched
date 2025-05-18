# Technical Context

## Technology Stack

### Frontend
- **Framework**: Vue.js 3
- **Styling**: TailwindCSS
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **Package Manager**: npm/yarn
- **State Management**: Vue reactive system (no auth state needed)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Data Storage**: JSON (upgradable to SQLite/PostgreSQL)
- **API Documentation**: Swagger/OpenAPI
- **Authentication**: None (single manager system)

## Development Setup

### Prerequisites
1. Python 3.8+
2. Node.js 16+
3. npm or yarn
4. Git

### Environment Setup

#### Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload
```

#### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

## Dependencies

### Backend Dependencies
- FastAPI
- uvicorn
- pydantic
- python-dotenv
- typing-extensions
- No auth libraries needed

### Frontend Dependencies
- Vue.js
- TailwindCSS
- Axios
- No auth libraries needed

## Technical Constraints

### 1. Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- No IE11 support required

### 2. Performance Requirements
- Page load < 2 seconds
- API response < 500ms
- Smooth schedule updates

### 3. Security Considerations
- Input validation
- CORS configuration
- Environment variable management
- Data sanitization
- No authentication needed

### 4. Scalability
- JSON storage upgrade path
- Modular component design
- API versioning support
- Caching strategy

## Development Workflow

### 1. Code Organization
- Feature-based structure
- Clear separation of concerns
- Consistent naming conventions
- Documentation requirements

### 2. Testing Strategy
- Unit tests for core logic
- Integration tests for API
- Component tests for UI
- E2E tests for critical flows

### 3. Deployment Process
- Development environment
- Staging environment
- Production environment
- CI/CD pipeline

### 4. Monitoring
- Error tracking
- Performance monitoring
- Usage analytics
- Health checks 