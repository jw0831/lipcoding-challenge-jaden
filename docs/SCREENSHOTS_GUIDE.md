# 📷 Screenshots Guide

This guide will help you take comprehensive screenshots of the Mentor-Mentee Matching Application for documentation and demo purposes.

## 🚀 Application URLs

Before taking screenshots, make sure both servers are running:

- **Backend API**: http://localhost:8080
- **Frontend App**: http://localhost:3000
- **API Documentation**: http://localhost:8080/api/docs (Swagger UI)

## 📸 Required Screenshots

### 1. **Homepage/Landing Page**
   - URL: `http://localhost:3000`
   - Capture: Initial landing page with navigation

### 2. **User Registration (Signup)**
   - URL: `http://localhost:3000/signup`
   - Capture: 
     - Empty signup form
     - Filled signup form for mentor
     - Filled signup form for mentee
     - Success message after registration

### 3. **User Login**
   - URL: `http://localhost:3000/login`
   - Capture:
     - Empty login form
     - Filled login form
     - Success redirect after login

### 4. **Mentor Profile**
   - URL: `http://localhost:3000/profile` (as mentor)
   - Capture:
     - Profile view showing mentor information
     - Profile edit form
     - Profile with uploaded image

### 5. **Mentee Profile**
   - URL: `http://localhost:3000/profile` (as mentee)
   - Capture:
     - Profile view showing mentee information
     - Profile edit form

### 6. **Mentor Listing**
   - URL: `http://localhost:3000/mentors` (as mentee)
   - Capture:
     - List of available mentors
     - Mentor cards with skills and bio
     - Filtering by skills (if implemented)

### 7. **Match Requests**
   - URL: `http://localhost:3000/requests`
   - Capture:
     - As mentee: outgoing requests
     - As mentor: incoming requests
     - Request with different statuses (pending, accepted, rejected)

### 8. **API Documentation**
   - URL: `http://localhost:8080/api/docs`
   - Capture:
     - Swagger UI showing all endpoints
     - Example API request/response

### 9. **Backend Admin/Database**
   - Show backend running in terminal
   - Database tables (if accessible)

## 🎬 Demo Video Script

Create a 3-5 minute demo video showing:

1. **Introduction (30 seconds)**
   - Show project overview
   - Mention technologies used

2. **User Registration & Login (1 minute)**
   - Register as mentor
   - Register as mentee
   - Login process

3. **Mentor Workflow (1.5 minutes)**
   - Mentor profile setup
   - View incoming requests
   - Accept/reject requests

4. **Mentee Workflow (1.5 minutes)**
   - Mentee profile setup
   - Browse mentors
   - Send match requests

5. **Technical Demo (30 seconds)**
   - Show API documentation
   - Mention TDD and testing

## 📱 Screenshot Tips

1. **Use consistent browser size**: 1920x1080 or 1440x900
2. **Clear browser cache** before taking screenshots
3. **Use sample data** that looks professional
4. **Hide personal information** if any
5. **Take screenshots in good lighting**
6. **Use full-screen browser window**

## 🎥 Video Recording Tools

### For Mac:
- **QuickTime Player** (built-in screen recording)
- **OBS Studio** (free, professional)
- **ScreenFlow** (paid, advanced editing)

### For Windows:
- **OBS Studio** (free, professional)
- **Camtasia** (paid, easy to use)
- **Windows Game Bar** (built-in, Win+G)

## 📝 After Capturing

1. **Organize screenshots** in the `docs/screenshots/` folder
2. **Name files descriptively**:
   - `01-homepage.png`
   - `02-signup-mentor.png`
   - `03-login-form.png`
   - etc.

3. **Update README.md** with screenshot links
4. **Upload video to YouTube** (if creating)
5. **Commit and push to GitHub**

## 🔗 YouTube Upload Guidelines

1. **Title**: "Mentor-Mentee Matching Web App - Full Stack Demo"
2. **Description**: Include:
   - Technologies used
   - GitHub repository link
   - Key features demonstrated
3. **Tags**: "React", "Flask", "JavaScript", "Python", "Web Development", "Full Stack"
4. **Thumbnail**: Use a screenshot of the main application
