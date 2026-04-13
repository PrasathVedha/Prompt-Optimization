# PromptX Documentation

## Overview
Prompt Opti is an advanced AI image generation platform that combines prompt enhancement with style-based generation capabilities. The system provides a robust pipeline for creating high-quality AI-generated images through an intuitive user interface.

## System Architecture

### Core Components
1. **Prompt Enhancement System** (`enhance_prompt.py`)
   - Analyzes user inputs
   - Enriches prompts with additional context
   - Optimizes prompt structure for better image generation

2. **Image Generation Pipeline** (`generate_images.py`)
   - Handles image generation requests
   - Manages style integration
   - Processes generation parameters

3. **Database Management** (`database/database.py`)
   - SQLite database implementation
   - Stores user data and generation history
   - Manages prompt templates and styles

### Route Structure
- **User Routes** (`routes/user_routes.py`)
  - Authentication endpoints
  - Image generation interface
  - User dashboard functionality

- **Admin Routes** (`routes/admin_routes.py`)
  - System monitoring
  - User management
  - Configuration controls

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Prompts Table
```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    original_prompt TEXT NOT NULL,
    enhanced_prompt TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Image Generation
- `POST /generate` - Generate new image
- `GET /images/history` - View generation history
- `GET /images/{id}` - Retrieve specific image

### Admin Operations
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `POST /admin/config` - System configuration

## Frontend Structure

### Templates
- `templates/index.html` - Landing page
- `templates/login.html` - User login interface
- `templates/register.html` - Registration page
- `templates/user_dashboard.html` - User dashboard
- `templates/admin_dashboard.html` - Admin interface

### Static Assets
- `static/styles.css` - Global styles
- `static/script.js` - Frontend functionality
- `static/workflow.svg` - System workflow diagram

## Dependencies
Key project dependencies are listed in `requirements.txt`:
- Flask - Web framework
- SQLite3 - Database management
- Image generation libraries
- Authentication modules

## Deployment Guidelines

### Environment Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize database:
   ```bash
   python -c "from database.database import init_db; init_db()"
   ```

### Running the Application
1. Development mode:
   ```bash
   flask run --debug
   ```

2. Production mode:
   ```bash
   waitress-serve --port=8000 app:app
   ```

## Security Considerations
- Password hashing implementation
- Rate limiting on API endpoints
- Input validation and sanitization
- Secure session management

## Performance Optimization
- Image caching strategy
- Database query optimization
- Asynchronous processing for long-running tasks

## Maintenance and Updates
- Regular dependency updates
- Database backups
- Log rotation and monitoring
- Performance metrics tracking

## Contributing Guidelines
1. Fork the repository
2. Create feature branch
3. Submit pull request with detailed description
4. Follow code style guidelines
5. Include tests for new features

## License
This project is proprietary and confidential. All rights reserved.

## Support
For technical support or feature requests, please contact the development team.
