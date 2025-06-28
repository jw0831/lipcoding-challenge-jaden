# Manual Browser Testing Checklist

## Pre-Test Setup
- [x] Backend server running on http://localhost:8080
- [x] Frontend server running on http://localhost:3000
- [x] Test users created: user@test.com (mentee), mentor@test.com (mentor)
- [ ] Browser opened to http://localhost:3000

## 1. Initial Page Load & Navigation
- [ ] Homepage loads correctly
- [ ] Navigation menu is visible and functional
- [ ] Responsive design works on different screen sizes

## 2. User Registration Flow
- [ ] Navigate to registration page
- [ ] Register new mentee user
- [ ] Register new mentor user
- [ ] Verify validation messages work correctly
- [ ] Verify success messages appear

## 3. User Login Flow
- [ ] Navigate to login page
- [ ] Login with test mentee (user@test.com/user)
- [ ] Verify JWT token is stored correctly
- [ ] Login with test mentor (mentor@test.com/user)
- [ ] Verify proper redirect after login

## 4. Profile Management
- [ ] View profile page
- [ ] Edit profile information
- [ ] Upload profile picture (if implemented)
- [ ] Update skills/expertise
- [ ] Save changes and verify persistence

## 5. Mentor Discovery (Mentee View)
- [ ] Navigate to mentor list page
- [ ] View available mentors
- [ ] Search/filter mentors
- [ ] View mentor profiles
- [ ] Send match request to mentor

## 6. Match Request Management
- [ ] View outgoing requests (mentee)
- [ ] View incoming requests (mentor)
- [ ] Accept match request (mentor)
- [ ] Reject match request (mentor)
- [ ] Delete match request (mentee)

## 7. Dashboard/Match Status
- [ ] View active matches
- [ ] View match history
- [ ] Navigate between different sections

## 8. Error Handling
- [ ] Test invalid login credentials
- [ ] Test network error scenarios
- [ ] Test unauthorized access attempts
- [ ] Verify error messages are user-friendly

## 9. UI/UX Verification
- [ ] All buttons and links work correctly
- [ ] Forms submit properly
- [ ] Loading states are shown
- [ ] Success/error messages display properly
- [ ] Design matches requirements

## 10. Data Persistence
- [ ] Logout and login again
- [ ] Verify data persistence across sessions
- [ ] Test browser refresh scenarios

## Test Results
(To be filled during testing)

### Issues Found:
- [ ] Issue 1: Description
- [ ] Issue 2: Description
- [ ] Issue 3: Description

### Screenshots Taken:
- [ ] Homepage
- [ ] Registration page
- [ ] Login page
- [ ] Profile page
- [ ] Mentor list
- [ ] Match requests page
- [ ] Dashboard

### Demo Video:
- [ ] Full user flow recorded
- [ ] All key features demonstrated
- [ ] Voice-over explaining features
