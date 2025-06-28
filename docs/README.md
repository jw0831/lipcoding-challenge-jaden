# 📸 Screenshot & Demo Preparation Guide

## 🎯 Current Status
✅ Backend running on: http://localhost:8080
✅ Frontend running on: http://localhost:3001
✅ API Documentation: http://localhost:8080/api/docs

## 📷 Step-by-Step Screenshot Process

### 1. Open Your Browser
- Use Chrome or Safari for best results
- Set window to full screen (1920x1080 recommended)
- Clear cache: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### 2. Take Screenshots in This Order:

#### **Screenshot 1: Homepage** 
- Navigate to: `http://localhost:3001`
- Show the landing page with navigation
- Save as: `01-homepage.png`

#### **Screenshot 2: Signup Page**
- Click "Sign Up" or navigate to signup
- Show empty form first
- Save as: `02-signup-empty.png`

#### **Screenshot 3: Mentor Registration**
- Fill form with mentor details:
  - Name: "Dr. Sarah Johnson"
  - Email: "sarah.mentor@example.com"
  - Password: "password123"
  - Role: "Mentor"
- Save as: `03-signup-mentor.png`

#### **Screenshot 4: Mentee Registration**
- Clear form and fill with mentee details:
  - Name: "Alex Smith"
  - Email: "alex.student@example.com"
  - Password: "password123"
  - Role: "Mentee"
- Save as: `04-signup-mentee.png`

#### **Screenshot 5: Login Page**
- Navigate to login page
- Show filled login form
- Save as: `05-login.png`

#### **Screenshot 6: Mentor Dashboard**
- Login as mentor
- Show mentor's main view
- Save as: `06-mentor-dashboard.png`

#### **Screenshot 7: Mentor Profile**
- Navigate to profile page
- Show mentor profile view
- Save as: `07-mentor-profile.png`

#### **Screenshot 8: Profile Edit**
- Click edit profile
- Show edit form with fields
- Save as: `08-profile-edit.png`

#### **Screenshot 9: Mentee View - Mentor List**
- Logout and login as mentee
- Navigate to mentors page
- Show list of available mentors
- Save as: `09-mentor-list.png`

#### **Screenshot 10: Match Requests**
- Show requests page (mentee view)
- Save as: `10-mentee-requests.png`

#### **Screenshot 11: API Documentation**
- Open: `http://localhost:8080/api/docs`
- Show Swagger UI
- Save as: `11-api-docs.png`

#### **Screenshot 12: Terminal/Backend**
- Show terminal with backend running
- Save as: `12-backend-terminal.png`

## 🎬 Recording Your Demo Video

### Option 1: QuickTime Player (Mac)
1. Open QuickTime Player
2. File → New Screen Recording
3. Click record and select your browser window
4. Follow the demo script in `DEMO_VIDEO_SCRIPT.md`

### Option 2: OBS Studio (Free, All Platforms)
1. Download OBS Studio
2. Add browser window as source
3. Record in 1080p
4. Follow the demo script

### Video Recording Tips:
- **Duration**: Keep it 3-5 minutes
- **Audio**: Speak clearly, no background noise
- **Pace**: Not too fast, pause between actions
- **Content**: Follow the script but be natural

## 📤 YouTube Upload Process

### 1. Create YouTube Account (if needed)
- Use professional email
- Create channel name related to your project

### 2. Upload Video
- **Title**: "Mentor-Mentee Matching Web App - Full Stack Demo | React + Flask"
- **Description**: Use the template in `DEMO_VIDEO_SCRIPT.md`
- **Thumbnail**: Use screenshot of your app
- **Tags**: React, Flask, JavaScript, Python, WebDev, FullStack

### 3. Video Settings
- **Visibility**: Public or Unlisted
- **Category**: Science & Technology
- **Language**: English (or your preference)

## 📁 Organizing Files for GitHub

Create this structure:
```
docs/
├── screenshots/
│   ├── 01-homepage.png
│   ├── 02-signup-empty.png
│   ├── 03-signup-mentor.png
│   └── ... (all screenshots)
├── SCREENSHOTS_GUIDE.md
├── DEMO_VIDEO_SCRIPT.md
└── README.md (this file)
```

## 📝 Update Main README.md

Add this section to your main README.md:

```markdown
## 📷 Screenshots

![Homepage](docs/screenshots/01-homepage.png)
*Application homepage with navigation*

![Mentor Registration](docs/screenshots/03-signup-mentor.png)
*Mentor registration form*

![Mentor Dashboard](docs/screenshots/06-mentor-dashboard.png)
*Mentor dashboard and profile*

![Mentor Listing](docs/screenshots/09-mentor-list.png)
*Mentee view of available mentors*

## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

Watch the full application demo on YouTube: [Your YouTube Link]
```

## 🚀 Final Submission Checklist

- [ ] All screenshots taken and saved
- [ ] Demo video recorded and uploaded to YouTube
- [ ] README.md updated with screenshots and video link
- [ ] All files committed to GitHub
- [ ] Repository is public and accessible
- [ ] Application runs correctly (test once more)

## 💡 Pro Tips

1. **Test Everything First**: Make sure all features work before recording
2. **Use Sample Data**: Create realistic but fake user data
3. **Clean Browser**: Use incognito mode for clean screenshots
4. **Consistent Sizing**: Keep browser window same size for all screenshots
5. **Good Lighting**: Take screenshots in good lighting conditions
6. **Professional Look**: Use professional-looking sample data

## 🔗 Quick Links

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8080
- **API Docs**: http://localhost:8080/api/docs
- **GitHub**: [Your Repository URL]
- **YouTube**: [Your Video URL] (after upload)

---

**Need Help?** 
- Check that both servers are running
- Refresh browser if pages don't load
- Use developer tools (F12) to debug issues
- Make sure you're using the correct ports
