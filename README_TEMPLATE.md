# 🎯 Mentor-Mentee Matching Web Application

A full-stack web application that connects mentees with mentors based on skills and interests, featuring a comprehensive match request system.

## 🛠️ Technology Stack

- **Frontend**: React.js, JavaScript, CSS3
- **Backend**: Flask, Python, SQLAlchemy
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest (Test-Driven Development)
- **Documentation**: OpenAPI/Swagger

## ✨ Key Features

- 🔐 **User Authentication**: Secure signup and login system
- 👤 **User Profiles**: Complete profile management with image upload
- 🔍 **Mentor Discovery**: Browse and filter mentors by skills
- 💌 **Match Requests**: Send, accept, reject, and track mentoring requests
- 🛡️ **Role-Based Access**: Different interfaces for mentors and mentees
- 📚 **API Documentation**: Interactive Swagger UI
- 🧪 **Test Coverage**: Comprehensive TDD test suite

## 🎥 Demo Video

[![Demo Video](https://img.youtube.com/vi/[REPLACE_WITH_VIDEO_ID]/maxresdefault.jpg)](https://youtu.be/[REPLACE_WITH_VIDEO_ID])

[▶️ **Watch Full Demo on YouTube**](https://youtu.be/[REPLACE_WITH_VIDEO_ID])

---

## 📷 Application Screenshots

### 🔐 Authentication & User Management
![Login Page](docs/screenshots/01-login-page.png)
*Secure login interface with form validation*

![Signup Page](docs/screenshots/02-signup-page.png)
*User registration with role selection (mentor/mentee)*

### 👤 Profile Management
![Profile Page](docs/screenshots/03-profile-page.png)
*Comprehensive profile management with image upload*

### 🔍 Mentor Discovery
![Mentor List](docs/screenshots/04-mentor-list.png)
*Advanced mentor search with filtering and sorting options*

### 💌 Match Request System
![Match Requests](docs/screenshots/05-match-requests.png)
*Complete match request management dashboard*

### 📚 API Documentation
![API Documentation](docs/screenshots/06-api-docs.png)
*Interactive Swagger UI for API testing and documentation*
*Simple registration process for both mentors and mentees*

### Mentor Experience
![Mentor Profile](docs/screenshots/07-mentor-profile.png)
*Comprehensive mentor profiles with skills and availability*

![Mentor Dashboard](docs/screenshots/06-mentor-dashboard.png)
*Mentor dashboard for managing incoming requests*

### Mentee Experience
![Mentor Discovery](docs/screenshots/09-mentor-list.png)
*Easy-to-browse mentor listing with filtering capabilities*

![Match Requests](docs/screenshots/10-mentee-requests.png)
*Track and manage outgoing match requests*

### Technical Documentation
![API Documentation](docs/screenshots/11-api-docs.png)
*Complete API documentation with Swagger UI*

## 🎬 Demo Video

[![Watch Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)

**[📺 Watch Full Demo on YouTube](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)**

*4-minute comprehensive demo showing all features and user workflows*

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mentor-mentee-app.git
   cd mentor-mentee-app
   ```

2. **Run the application**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8080
   - API Documentation: http://localhost:8080/api/docs

## 🧪 Testing

The application includes comprehensive test coverage using pytest:

```bash
cd backend
source venv/bin/activate
python -m pytest -v
```

### Test Coverage Includes:
- ✅ Authentication and authorization
- ✅ Profile management
- ✅ Mentor listing and filtering
- ✅ Match request workflows
- ✅ Security and validation
- ✅ API specification compliance

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/signup` | User registration |
| POST | `/api/login` | User authentication |
| GET | `/api/profile` | Get user profile |
| PUT | `/api/profile` | Update user profile |
| GET | `/api/mentors` | List available mentors |
| POST | `/api/match-requests` | Send match request |
| GET | `/api/match-requests/incoming` | Get incoming requests (mentors) |
| GET | `/api/match-requests/outgoing` | Get outgoing requests (mentees) |
| PUT | `/api/match-requests/:id/accept` | Accept request |
| PUT | `/api/match-requests/:id/reject` | Reject request |
| DELETE | `/api/match-requests/:id` | Cancel request |

## 🏗️ Architecture

### Frontend Structure
```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Main application pages
│   ├── context/       # React Context for state management
│   └── index.js       # Application entry point
```

### Backend Structure
```
backend/
├── app.py            # Main Flask application
├── requirements.txt  # Python dependencies
├── test_*.py        # Test files
└── uploads/         # User uploaded files
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password encryption
- **Input Validation**: Comprehensive request validation
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Proper cross-origin setup
- **Role-Based Access**: Endpoint-level authorization

## 📈 Development Approach

This project was built using **Test-Driven Development (TDD)**:

1. ✅ **Requirements Analysis**: Thorough API specification review
2. ✅ **Test Creation**: Comprehensive test suite covering all endpoints
3. ✅ **Implementation**: Backend and frontend development
4. ✅ **Validation**: All tests passing and specification compliance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built as part of a coding challenge assessment
- Implements modern full-stack development practices
- Demonstrates Test-Driven Development methodology

---

**⭐ If you found this project helpful, please give it a star!**

**🔗 Links:**
- [Live Demo](YOUR_DEMO_URL_IF_DEPLOYED)
- [YouTube Demo](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)
- [API Documentation](http://localhost:8080/api/docs)

**👨‍💻 Developer:** [Your Name](https://github.com/yourusername)
