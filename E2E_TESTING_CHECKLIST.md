# 🧪 End-to-End Testing Checklist - Enrollment System

**Date:** October 3, 2025  
**Status:** ⏳ Ready to Execute  
**Prerequisites:** ✅ All fixes applied, npm install completed

---

## 🎯 Testing Overview

This checklist covers comprehensive end-to-end testing of the enrollment system across student, instructor, and admin roles.

**Testing Scope:**
- 9 API endpoints
- 3 frontend pages
- 1 shared component
- Role-based access control
- Edge cases and error handling

---

## 📋 Pre-Testing Setup

### Step 1: Start Backend Server
```bash
cd BEDB
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify:**
- [ ] Backend running at http://localhost:8000
- [ ] Swagger docs accessible at http://localhost:8000/docs
- [ ] MongoDB connection successful
- [ ] No startup errors in console

---

### Step 2: Start Frontend Server
```bash
cd learning-app-fe
npm install  # If not already done
npm run dev
```

**Expected Output:**
```
VITE ready in XXX ms
➜  Local:   http://localhost:3000/
```

**Verify:**
- [ ] Frontend running at http://localhost:3000
- [ ] No build errors
- [ ] Hot reload working

---

### Step 3: Prepare Test Accounts

**Create/Verify Test Users:**
1. **Student Account**
   - Email: `student@test.com`
   - Password: `password123`
   - Role: `student`

2. **Instructor Account**
   - Email: `instructor@test.com`
   - Password: `password123`
   - Role: `instructor`

3. **Admin Account**
   - Email: `admin@test.com`
   - Password: `password123`
   - Role: `admin`

**Verify:**
- [ ] Can login with all 3 accounts
- [ ] Each account has correct role
- [ ] JWT tokens working

---

### Step 4: Prepare Test Courses

**Create Test Courses (as Instructor):**
1. **PUBLIC Course**
   - Title: "Test Public Course"
   - Description: "For enrollment testing"
   - Visibility: `PUBLIC`
   - Level: `beginner`

2. **DRAFT Course**
   - Title: "Test Draft Course"
   - Description: "Should not be enrollable"
   - Visibility: `DRAFT`
   - Level: `intermediate`

3. **PRIVATE Course**
   - Title: "Test Private Course"
   - Description: "Should not be enrollable"
   - Visibility: `PRIVATE`
   - Level: `advanced`

**Verify:**
- [ ] All 3 courses created successfully
- [ ] Visibility correctly set
- [ ] Courses visible in instructor dashboard

---

## 🧑‍🎓 Student Flow Testing

### Test 1: Browse Public Courses
**URL:** http://localhost:3000/my-learning

**Steps:**
1. Login as student
2. Navigate to "My Learning" page
3. View available public courses

**Expected Results:**
- [ ] Page loads without errors
- [ ] Dashboard shows stats (0 enrolled initially)
- [ ] PUBLIC course visible
- [ ] DRAFT course NOT visible
- [ ] PRIVATE course NOT visible
- [ ] "Enroll" button visible on PUBLIC course

**Error Cases:**
- [ ] Non-student cannot access page (403)
- [ ] Loading spinner shows while fetching
- [ ] Empty state shown if no courses

---

### Test 2: Enroll in Course
**URL:** Course detail page or enrollment page

**Steps:**
1. Find PUBLIC course
2. Click "Enroll" button
3. Wait for confirmation

**Expected Results:**
- [ ] Loading spinner on button
- [ ] Success toast: "Đăng ký khóa học thành công!"
- [ ] Button changes to "Hủy đăng ký"
- [ ] Course appears in "My Courses"
- [ ] Enrollment count incremented
- [ ] Dashboard stats updated

**API Call:**
```
POST /api/v1/student/courses/{course_id}/enroll
Response: 200 OK with CourseEnrollmentResponse
```

**Verify Backend:**
- [ ] Enrollment record created in database
- [ ] `status` = "active"
- [ ] `progress` = 0.0
- [ ] `course.enrollment_count` incremented
- [ ] `enrolled_at` timestamp set

---

### Test 3: View My Courses
**URL:** http://localhost:3000/my-courses

**Steps:**
1. Navigate to "My Courses" page
2. View enrolled courses

**Expected Results:**
- [ ] Enrolled course displayed
- [ ] Progress bar shows 0%
- [ ] Status shows "Đang học" (active)
- [ ] Enrollment date displayed
- [ ] "Continue Learning" button visible
- [ ] Can filter by status (all/active/completed/dropped)

**API Call:**
```
GET /api/v1/student/enrolled-courses?limit=100
Response: 200 OK with EnrolledCourseInfo[]
```

---

### Test 4: Access Course Content
**Steps:**
1. Click on enrolled course
2. View course details
3. Access chapters

**Expected Results:**
- [ ] Can view all course content
- [ ] Chapters accessible
- [ ] Progress tracking works
- [ ] "Enrolled" badge visible

---

### Test 5: Unenroll from Course
**Steps:**
1. Go to enrolled course detail
2. Click "Hủy đăng ký" button
3. Confirm in dialog

**Expected Results:**
- [ ] Confirmation dialog appears
- [ ] Success toast: "Hủy đăng ký thành công"
- [ ] Course removed from "My Courses"
- [ ] Button changes back to "Đăng ký học"
- [ ] Enrollment count decremented
- [ ] Dashboard stats updated

**API Call:**
```
DELETE /api/v1/student/courses/{course_id}/enroll
Response: 200 OK with success message
```

**Verify Backend:**
- [ ] Enrollment `status` = "dropped"
- [ ] `course.enrollment_count` decremented
- [ ] Record NOT deleted (soft delete)

---

### Test 6: Re-enroll After Dropping
**Steps:**
1. Enroll in same course again
2. Verify re-enrollment works

**Expected Results:**
- [ ] Can enroll again
- [ ] Previous enrollment reactivated
- [ ] `status` changed from "dropped" to "active"
- [ ] Enrollment count incremented again
- [ ] Progress may be preserved or reset to 0

---

### Test 7: Student Dashboard
**URL:** http://localhost:3000/my-learning

**Steps:**
1. Enroll in multiple courses
2. View dashboard stats

**Expected Results:**
- [ ] Total enrolled courses correct
- [ ] Completed courses count (if any completed)
- [ ] In-progress courses count
- [ ] Average progress calculated
- [ ] Time spent displayed
- [ ] Recent courses list shown

**API Call:**
```
GET /api/v1/student/dashboard
Response: 200 OK with StudentDashboardResponse
```

---

### Test 8: Edge Cases - Student

**Test 8a: Enroll in DRAFT Course**
- [ ] "Bản nháp" button shown (disabled)
- [ ] Cannot click to enroll
- [ ] Lock icon displayed

**Test 8b: Enroll in PRIVATE Course**
- [ ] "Riêng tư" button shown (disabled)
- [ ] Cannot click to enroll
- [ ] Lock icon displayed

**Test 8c: Enroll Twice**
- [ ] Second enrollment attempt fails
- [ ] Error toast: "Already enrolled in this course"
- [ ] 400 Bad Request from API

**Test 8d: Enroll in Own Course**
- [ ] If student also creates course
- [ ] Enroll button not visible
- [ ] (Students typically can't create courses, but test if possible)

**Test 8e: Unenroll from Non-enrolled Course**
- [ ] API returns 404
- [ ] Error toast shown
- [ ] UI handles gracefully

---

## 👨‍🏫 Instructor Flow Testing

### Test 9: Instructor Dashboard
**URL:** http://localhost:3000/instructor/dashboard

**Steps:**
1. Login as instructor
2. Navigate to "Instructor Dashboard"
3. View overview stats

**Expected Results:**
- [ ] Total courses count correct
- [ ] Total students count correct
- [ ] Total enrollments count correct
- [ ] Average rating displayed (if implemented)
- [ ] Course analytics list shown
- [ ] Recent course performance visible

**API Call:**
```
GET /api/v1/instructor/dashboard
Response: 200 OK with InstructorDashboardResponse
```

**Verify:**
- [ ] Only instructor's courses counted
- [ ] Not seeing other instructors' data

---

### Test 10: View Instructor Courses
**Steps:**
1. View courses list on dashboard
2. See student count per course

**Expected Results:**
- [ ] All instructor courses shown
- [ ] Student count correct for each
- [ ] Enrollment status visible
- [ ] Can see DRAFT, PRIVATE, PUBLIC courses

**API Call:**
```
GET /api/v1/instructor/courses
Response: 200 OK with Course[] (with enrollment_count)
```

---

### Test 11: View Course Students
**Steps:**
1. Click on a course with enrollments
2. View student list

**Expected Results:**
- [ ] All enrolled students shown
- [ ] Student name displayed
- [ ] Student email displayed
- [ ] Enrollment date shown
- [ ] Progress percentage shown
- [ ] Status (active/completed/dropped)
- [ ] Last accessed timestamp

**API Call:**
```
GET /api/v1/instructor/courses/{course_id}/students
Response: 200 OK with StudentEnrollmentInfo[]
```

**Verify:**
- [ ] Can filter by status (active/completed/dropped)
- [ ] Only students in THIS course shown
- [ ] Dropped students included (if no filter)

---

### Test 12: View Course Analytics
**Steps:**
1. View analytics for a course
2. Check metrics

**Expected Results:**
- [ ] Total enrollments count
- [ ] Active students count
- [ ] Completed students count
- [ ] Average progress percentage
- [ ] Average time spent
- [ ] Completion rate percentage
- [ ] Charts/visualizations (if implemented)

**API Call:**
```
GET /api/v1/instructor/courses/{course_id}/analytics
Response: 200 OK with CourseAnalytics
```

**Calculations to Verify:**
```
completion_rate = (completed_students / total_enrollments) * 100
average_progress = sum(all_student_progress) / total_students
```

---

### Test 13: Change Course Visibility
**Steps:**
1. Set course from DRAFT to PUBLIC
2. Verify students can now enroll

**Expected Results:**
- [ ] Visibility updated successfully
- [ ] Course now visible to students
- [ ] Enroll button enabled for students
- [ ] DRAFT → PUBLIC transition works
- [ ] PUBLIC → DRAFT hides from students

**Verify:**
- [ ] Students cannot enroll in DRAFT
- [ ] Students CAN enroll in PUBLIC
- [ ] Existing enrollments preserved

---

### Test 14: View All Students
**Steps:**
1. View all students across all courses
2. Check aggregated list

**Expected Results:**
- [ ] Students from all instructor courses
- [ ] Deduplicated (student appears once per course)
- [ ] Pagination works (if many students)

**API Call:**
```
GET /api/v1/instructor/students
Response: 200 OK with StudentEnrollmentInfo[]
```

---

### Test 15: Edge Cases - Instructor

**Test 15a: View Empty Course**
- [ ] Course with 0 enrollments shows correctly
- [ ] Empty state message
- [ ] No errors

**Test 15b: Access Other Instructor's Students**
- [ ] Cannot see other instructor's students
- [ ] Only own courses shown
- [ ] Security enforced

**Test 15c: Delete Course with Enrollments**
- [ ] Warning about enrolled students
- [ ] Cascade behavior defined
- [ ] (Test based on implementation)

---

## 👨‍💼 Admin Flow Testing

### Test 16: Admin Access to Instructor Dashboard
**Steps:**
1. Login as admin
2. Access instructor dashboard

**Expected Results:**
- [ ] Can access instructor dashboard
- [ ] Can see ALL courses (all instructors)
- [ ] Can see ALL students
- [ ] Full system-wide analytics

**Verify:**
- [ ] Admin has instructor privileges
- [ ] Can perform all instructor actions

---

### Test 17: Admin Access to Student Pages
**Steps:**
1. Try accessing student pages as admin

**Expected Results:**
- [ ] Cannot access student-only pages
- [ ] 403 Forbidden or redirect
- [ ] Role restriction enforced

---

## 🔒 Security Testing

### Test 18: Role-Based Access Control

**Test 18a: Student Access to Instructor Pages**
```
URL: /instructor/dashboard
Expected: 403 Forbidden or redirect
```
- [ ] Access denied
- [ ] Error message shown
- [ ] Redirect to appropriate page

**Test 18b: Instructor Access to Student Pages**
```
URL: /my-learning
Expected: 403 Forbidden or redirect
```
- [ ] Access denied
- [ ] Cannot view student dashboard
- [ ] Cannot enroll in courses

**Test 18c: Unauthenticated Access**
```
All enrollment pages
Expected: Redirect to login
```
- [ ] Redirected to /login
- [ ] Protected routes working
- [ ] Return URL preserved

---

### Test 19: API Authorization

**Test with Invalid Token:**
```bash
curl -H "Authorization: Bearer invalid_token" \
  http://localhost:8000/api/v1/student/enrolled-courses
```
- [ ] Returns 401 Unauthorized
- [ ] Error message clear
- [ ] No data leaked

**Test with Wrong Role:**
```bash
# Instructor token on student endpoint
POST /api/v1/student/courses/{id}/enroll
```
- [ ] Returns 403 Forbidden
- [ ] "Only students can enroll" message
- [ ] Role checked correctly

---

## 🔍 Data Consistency Testing

### Test 20: Enrollment Count Accuracy

**Steps:**
1. Note initial enrollment_count
2. Enroll 3 students
3. Check count = initial + 3
4. Unenroll 1 student
5. Check count = initial + 2

**Verify:**
- [ ] Count always accurate
- [ ] Incremented on enroll
- [ ] Decremented on unenroll
- [ ] Not affected by re-enrollment of dropped

---

### Test 21: Progress Tracking

**Steps:**
1. Enroll in course
2. Complete some chapters
3. Check progress updates
4. Verify dashboard reflects changes

**Verify:**
- [ ] Progress percentage calculated correctly
- [ ] Last accessed timestamp updated
- [ ] Time spent tracked
- [ ] Dashboard stats sync with reality

---

### Test 22: Database Integrity

**Verify in MongoDB:**
```javascript
// Check enrollment record
db.course_enrollment.findOne({ student_id: ObjectId("...") })

// Check course enrollment_count
db.course.findOne({ _id: ObjectId("...") })
```

**Assertions:**
- [ ] Enrollment record exists
- [ ] Status field correct
- [ ] Timestamps accurate
- [ ] Course count matches enrollments
- [ ] No orphaned records
- [ ] Indexes working

---

## ⚡ Performance Testing

### Test 23: Load Time

**Measure:**
- [ ] Student dashboard < 1s load
- [ ] Instructor dashboard < 1.5s load
- [ ] Course list < 800ms load
- [ ] Enroll action < 500ms response

---

### Test 24: Concurrent Enrollments

**Steps:**
1. Multiple students enroll simultaneously
2. Check enrollment count accuracy

**Verify:**
- [ ] No race conditions
- [ ] Count always correct
- [ ] All enrollments succeed
- [ ] Database transactions work

---

## 🐛 Error Handling Testing

### Test 25: Network Errors

**Simulate:**
- [ ] Stop backend mid-request
- [ ] Slow network (throttle)
- [ ] Timeout scenarios

**Expected:**
- [ ] Error toast shown
- [ ] Loading state cleared
- [ ] UI remains functional
- [ ] Can retry action

---

### Test 26: Invalid Data

**Test:**
- [ ] Enroll in non-existent course (404)
- [ ] Invalid course ID format
- [ ] Missing required fields
- [ ] Malformed requests

**Expected:**
- [ ] Appropriate error messages
- [ ] No app crashes
- [ ] User-friendly feedback

---

## 📱 Responsive Design Testing

### Test 27: Mobile View
**Devices:** iPhone 12, iPad, Android

**Verify:**
- [ ] Dashboard cards stack properly
- [ ] Enroll button accessible
- [ ] Navigation menu works
- [ ] Tables scroll horizontally
- [ ] Touch targets adequate (44x44px)

---

### Test 28: Dark Mode
**Steps:**
1. Toggle dark mode
2. Check all enrollment pages

**Verify:**
- [ ] All colors readable
- [ ] Contrast sufficient
- [ ] Icons visible
- [ ] No white flashes
- [ ] Consistent styling

---

## 🌐 Internationalization Testing

### Test 29: Language Switching

**Test Both Locales:**
```
Vietnamese (vi) and English (en)
```

**Verify:**
- [ ] All labels translated
- [ ] Toast messages translated
- [ ] Error messages translated
- [ ] Button text translated
- [ ] No missing keys
- [ ] Number/date formatting correct

---

## 📊 Analytics Verification

### Test 30: Course Analytics Calculation

**Setup:**
- Course with 10 students:
  - 3 completed (progress 100%)
  - 5 active (progress 50% avg)
  - 2 dropped (progress 20% avg)

**Expected Analytics:**
```
total_enrollments: 10
active_students: 5
completed_students: 3
average_progress: (300 + 250 + 40) / 10 = 59%
completion_rate: 3 / 10 = 30%
```

**Verify:**
- [ ] Calculations correct
- [ ] All students counted
- [ ] Dropped students included in total
- [ ] Percentages accurate

---

## ✅ Final Verification

### Test 31: Complete User Journey

**Student Journey:**
1. ✅ Register account
2. ✅ Login
3. ✅ Browse courses
4. ✅ Enroll in PUBLIC course
5. ✅ View My Courses
6. ✅ Access course content
7. ✅ Complete chapters (progress)
8. ✅ View dashboard stats
9. ✅ Unenroll
10. ✅ Re-enroll
11. ✅ Complete course
12. ✅ View achievements

**Instructor Journey:**
1. ✅ Register account (instructor)
2. ✅ Login
3. ✅ Create course (DRAFT)
4. ✅ Add chapters
5. ✅ Set visibility PUBLIC
6. ✅ View instructor dashboard
7. ✅ See student enrollments
8. ✅ View course analytics
9. ✅ Check student progress
10. ✅ Update course content

---

## 📝 Testing Summary Template

```markdown
## Test Results - Enrollment System

**Date:** [Date]
**Tester:** [Name]
**Environment:** Development/Staging/Production

### Summary
- Total Tests: 31
- Passed: ___
- Failed: ___
- Blocked: ___
- Success Rate: ___%

### Critical Issues Found
1. [Issue description]
   - Severity: Critical/High/Medium/Low
   - Steps to reproduce: ...
   - Expected vs Actual: ...

### Non-Critical Issues
1. [Issue description]
   - Impact: ...
   - Recommendation: ...

### Performance Metrics
- Avg API Response Time: ___ ms
- Dashboard Load Time: ___ s
- Enroll Action Time: ___ ms

### Browser Compatibility
- Chrome: ✅/❌
- Firefox: ✅/❌
- Safari: ✅/❌
- Edge: ✅/❌

### Device Compatibility
- Desktop: ✅/❌
- Tablet: ✅/❌
- Mobile: ✅/❌

### Overall Status
🟢 Ready for Production
🟡 Minor Issues (can deploy)
🔴 Critical Issues (cannot deploy)

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Sign-off
- Developer: ________ Date: ________
- QA: ________ Date: ________
- Product Owner: ________ Date: ________
```

---

## 🎯 Success Criteria

**Minimum Requirements for Production:**
- [ ] All critical tests pass (1-22)
- [ ] No data corruption
- [ ] No security vulnerabilities
- [ ] Role-based access working
- [ ] Error handling graceful
- [ ] Performance acceptable
- [ ] Mobile responsive
- [ ] Translations complete

**Nice to Have:**
- [ ] All tests pass (1-31)
- [ ] Zero errors in console
- [ ] < 500ms API response
- [ ] 100% test coverage

---

**Good luck with testing! 🚀**

When all tests pass, the enrollment system is ready for production deployment!
