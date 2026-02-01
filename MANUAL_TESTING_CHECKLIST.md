# 🧪 Manual Testing Checklist - Prodigy Auth Security Features

## 🚀 **BEFORE YOU START**

1. **Make sure both servers are running:**
   ```bash
   # Terminal 1 - Backend
   python manage.py runserver
   
   # Terminal 2 - Frontend  
   cd frontend
   npm run dev
   ```

2. **Have these credentials ready:**
   - Admin: `admin@prodigyauth.com` / `ProdigyAdmin123!`
   - Test user: Create a new one during testing

---

## 📋 **TESTING CHECKLIST**

### ✅ **1. Login Endpoint Fix**
**What to test:** Basic login functionality
**Steps:**
1. Go to `http://localhost:5173/login`
2. Try logging in with admin credentials
3. **Expected:** Login should work without 500 errors
4. **Check:** You should get redirected to dashboard

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **2. Audit Logging**
**What to test:** All actions are being logged
**Steps:**
1. Login as admin
2. Go to Django Admin: `http://127.0.0.1:8000/admin/`
3. Navigate to `Accounts > Audit logs`
4. **Expected:** See login entries with IP addresses and timestamps
5. Try other actions (logout, role changes) and verify they're logged

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **3. Session Management**
**What to test:** Session tracking and termination
**Steps:**
1. Login from multiple browsers/devices
2. Use API endpoint: `GET /api/auth/sessions/` (with auth header)
3. **Expected:** See multiple active sessions
4. Test session termination: `POST /api/auth/terminate-session/`
5. **Expected:** Session should be deactivated

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **4. Rate Limiting**
**What to test:** Protection against brute force attacks
**Steps:**
1. Try logging in with wrong password 6+ times rapidly
2. **Expected:** Should get rate limited (429 error) after 5 attempts
3. Wait 5 minutes and try again
4. **Expected:** Should be able to attempt login again

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **5. 2FA Backup Codes**
**What to test:** 2FA recovery system
**Steps:**
1. Login as admin
2. Go to 2FA verification page
3. If 2FA not enabled, enable it first
4. Use API: `POST /api/auth/regenerate-backup-codes/`
5. **Expected:** Get 10 backup codes
6. Test verification: `POST /api/auth/verify-backup-code/`
7. **Expected:** Valid codes work, invalid codes rejected

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **6. Enhanced Logout**
**What to test:** Proper token invalidation and session cleanup
**Steps:**
1. Login and note your session
2. Logout using the logout button
3. Try accessing protected pages
4. **Expected:** Should be redirected to login
5. Check Django admin for session status
6. **Expected:** Session should be marked as inactive

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **7. Admin 2FA Enforcement**
**What to test:** Admins must enable 2FA
**Steps:**
1. Create a new admin user without 2FA
2. Login as that admin
3. **Expected:** Should be forced to 2FA setup page
4. Try to skip 2FA setup
5. **Expected:** Should not be allowed to skip

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **8. Database Models**
**What to test:** New tables are working
**Steps:**
1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Check for these new sections:
   - `Audit logs` - Should show login/logout entries
   - `User sessions` - Should show active sessions
   - `Two factor backup codes` - Should show backup codes
3. **Expected:** All tables accessible and populated

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **9. Email Notifications**
**What to test:** Security-related emails are sent
**Steps:**
1. Enable 2FA - should get email notification
2. Change password - should get email notification
3. Admin changes your role - should get email notification
4. Check `sent_emails/` folder for email logs
5. **Expected:** All security actions trigger emails

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

### ✅ **10. Frontend Integration**
**What to test:** Frontend works with new backend features
**Steps:**
1. Test login flow with session creation
2. Test 2FA verification with backup codes option
3. Test logout with proper cleanup
4. Test admin panel with new audit features
5. **Expected:** All frontend features work smoothly

**Status:** ⬜ Pass ⬜ Fail
**Notes:** _____________________

---

## 🔧 **AUTOMATED TESTING**

Run the comprehensive test suite:
```bash
python test_all_security_features.py
```

This will automatically test:
- Login endpoint functionality
- Audit logging system
- Session management
- Rate limiting
- 2FA backup codes
- Enhanced logout
- Database models
- Security headers

---

## 📊 **TESTING RESULTS SUMMARY**

**Total Tests:** 10
**Passed:** ___/10
**Failed:** ___/10
**Success Rate:** ___%

### **Critical Issues Found:**
1. _____________________
2. _____________________
3. _____________________

### **Minor Issues Found:**
1. _____________________
2. _____________________
3. _____________________

---

## 🚀 **PRODUCTION READINESS CHECKLIST**

After all tests pass, verify these for production:

- ⬜ **Environment Variables**: All secrets in `.env` file
- ⬜ **Database**: PostgreSQL configured for production
- ⬜ **Email**: SMTP properly configured
- ⬜ **HTTPS**: SSL certificates installed
- ⬜ **Rate Limiting**: Enabled and tested
- ⬜ **Audit Logging**: Working and monitored
- ⬜ **Backup Strategy**: Database and files backed up
- ⬜ **Monitoring**: Error tracking and alerts set up

---

## 💡 **TROUBLESHOOTING**

### **Common Issues:**

1. **Login 500 Error:**
   - Clear Python cache: `rm -rf **/__pycache__`
   - Restart Django server
   - Check for decorator conflicts

2. **Rate Limiting Not Working:**
   - Check `RATELIMIT_ENABLE = True` in settings
   - Verify middleware is in `MIDDLEWARE` list
   - Test with different IP addresses

3. **Audit Logs Empty:**
   - Check database migration: `python manage.py migrate`
   - Verify audit logging in views
   - Check Django admin permissions

4. **2FA Issues:**
   - Verify user has `otp_secret` set
   - Check cache configuration
   - Test with authenticator app

---

**Testing Date:** ___________
**Tester:** ___________
**Environment:** Development / Staging / Production
**Overall Status:** ⬜ Ready for Production ⬜ Needs Fixes