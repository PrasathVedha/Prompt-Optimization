# PromptX System Architecture Documentation

## System Overview
PromptX is an advanced AI image generation platform that combines prompt enhancement with style-based generation capabilities. The system utilizes a multi-stage pipeline for processing user inputs and generating high-quality images.

## Core Components

### 1. Authentication System
- **Implementation**: Flask session-based authentication
- **Key Files**: `app.py`, `routes/user_routes.py`
- **Features**:
  - User registration with password hashing
  - Session management
  - Login/logout functionality
  - Admin/user role separation

### 2. Prompt Enhancement Pipeline
- **Implementation**: `enhance_prompt.py`
- **Stages**:
  1. **Initial Enhancement**
     - Processes raw user input
     - Adds factual context using Google's Generative AI
     - Ensures prompt clarity and specificity
  2. **Style Integration**
     - Applies selected artistic style
     - Maintains coherent visual description
     - Supports multiple predefined styles
  3. **Final Optimization**
     - Generates concise, descriptive output
     - Optimizes for image generation
     - Maintains natural language flow

### 3. Image Generation System
- **Implementation**: `generate_images.py`
- **Features**:
  - Style-based image generation
  - Quality optimization
  - Error handling and validation

### 4. Database Management
- **Implementation**: `database/database.py`
- **Schema**:
  ```sql
  -- Users Table
  CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      username TEXT UNIQUE,
      password TEXT,
      credits INTEGER DEFAULT 20,
      is_admin BOOLEAN DEFAULT 0
  )

  -- Prompts Table
  CREATE TABLE prompts (
      id INTEGER PRIMARY KEY,
      user_id INTEGER,
      input1 TEXT,
      input2 TEXT,
      image BLOB,
      FOREIGN KEY(user_id) REFERENCES users(id)
  )

  -- Credit Requests Table
  CREATE TABLE credit_requests (
      id INTEGER PRIMARY KEY,
      user_id INTEGER,
      requested_amount INTEGER,
      status TEXT DEFAULT 'pending',
      request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES users(id)
  )
  ```

### 5. Credit System
- **Implementation**: Integrated in `database.py`
- **Features**:
  - Default 20 credits for new users
  - Credit consumption per generation
  - Credit request system
  - Admin approval workflow

## API Endpoints

### Authentication Endpoints
```
POST /login
- Purpose: User authentication
- Parameters: username, password
- Returns: Session cookie

POST /register
- Purpose: New user registration
- Parameters: username, password
- Returns: Success/failure message

GET /logout
- Purpose: User logout
- Returns: Redirect to login
```

### Image Generation Endpoints
```
POST /generate
- Purpose: Generate new image
- Parameters: prompt, style
- Returns: prompt_id

GET /output/<prompt_id>
- Purpose: Retrieve generated image
- Parameters: prompt_id
- Returns: JPEG image
```

### Credit Management Endpoints
```
POST /request-credits
- Purpose: Request additional credits
- Parameters: amount
- Returns: Success/failure message
```

## Frontend Structure

### Templates
- `login.html`: Authentication interface
- `register.html`: User registration form
- `user_dashboard.html`: Main user interface
- `admin_dashboard.html`: Admin control panel

### Static Assets
- `styles.css`: Global styling
- `script.js`: Frontend functionality
- `workflow.svg`: System diagram

## Security Implementation

### Password Security
- Werkzeug password hashing
- Secure session management
- CSRF protection

### Access Control
- Role-based authorization
- Session validation
- Route protection

## Error Handling

### Global Error Handlers
- Authentication errors
- Credit insufficiency
- Generation failures
- Database errors

### Response Format
```json
{
    "error": "Error description",
    "status": 400
}
```

## Performance Considerations

### Database Optimization
- SQLite indexes
- Connection pooling
- Query optimization

### Image Processing
- Asynchronous generation
- Result caching
- Memory management

## Deployment Configuration

### Production Server
```python
from waitress import serve
serve(app, host='0.0.0.0', port=5000)
```

### Environment Variables
```python
os.environ["HF_HOME"] = "E:/cap/Stable-Diffusion-Project/TEXT-TO-IMAGE-GENERATION/huggingface"
app.secret_key = os.urandom(24)
```

## Maintenance Procedures

### Database Maintenance
- Regular backups
- Index optimization
- Data cleanup

### System Updates
- Dependency updates
- Security patches
- Feature deployments

## Monitoring and Logging

### System Logs
- Generation requests
- Error tracking
- User activities

### Performance Metrics
- Response times
- Success rates
- Resource usage

## Future Considerations

### Scalability
- Load balancing
- Distributed processing
- Cache optimization

### Feature Expansion
- Additional styles
- Batch processing
- API integrations