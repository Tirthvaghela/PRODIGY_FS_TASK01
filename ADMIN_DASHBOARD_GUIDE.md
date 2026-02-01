# 🔐 Prodigy Auth Admin Dashboard Guide

## Two Powerful Admin Interfaces

Your Prodigy Auth system now has **two comprehensive admin interfaces** for complete user and system management:

### 1. 🌐 Django Admin (Built-in)
**URL:** http://127.0.0.1:8000/admin  
**Login:** Prodigy / [your password]

**Features:**
- ✅ **Enhanced User Management** with colored badges and status indicators
- ✅ **Bulk Actions**: Send verification emails, verify users, promote to admin
- ✅ **Advanced Filtering**: By role, verification status, join date, locked accounts
- ✅ **Quick Actions**: Reset failed attempts, send emails directly from user list
- ✅ **Professional Interface** with custom branding and intuitive layout
- ✅ **Security Features**: View failed login attempts, account lock status
- ✅ **Email Integration**: Send verification emails directly from admin

**Admin Actions Available:**
- 📧 Send verification emails to unverified users
- ✅ Manually verify users
- 👑 Promote users to admin role
- 👤 Demote admins to regular users
- 🔓 Reset failed login attempts and unlock accounts

### 2. ⚛️ React Admin Panel (Modern UI)
**URL:** http://localhost:5173/admin  
**Login:** Use your admin account

**Features:**
- ✅ **Real-time Dashboard** with live statistics
- ✅ **User Management Table** with inline actions
- ✅ **System Status Monitoring** 
- ✅ **Recent User Activity** tracking
- ✅ **Professional Design** matching your brand
- ✅ **Mobile Responsive** interface
- ✅ **Quick Actions** for common admin tasks

**Three Main Tabs:**
1. **📊 Dashboard**: Statistics, recent users, quick actions
2. **👥 User Management**: Full user table with inline actions
3. **⚙️ System Status**: Health monitoring and configuration

## 📊 Admin Dashboard Features

### Statistics Overview
- **Total Users**: Complete user count
- **Verified Users**: Email-verified accounts
- **Admin Users**: Users with admin privileges
- **Unverified Users**: Pending email verification
- **Locked Accounts**: Temporarily locked due to failed attempts
- **Recent Registrations**: New users in last 7 days

### User Management Actions
- **📧 Send Verification**: Email verification to unverified users
- **🔒/🔓 Toggle Status**: Activate/deactivate user accounts
- **🔄 Reset Attempts**: Clear failed login attempts and unlock accounts
- **👑 Role Management**: Promote/demote admin privileges (Django admin)

### System Monitoring
- **🔐 Authentication System**: JWT token service status
- **📧 Email Service**: SMTP configuration and status
- **🗄️ Database**: Connection and health status
- **🌐 CORS**: Cross-origin configuration status
- **🔒 Security**: Account locking and security features

## 🚀 Getting Started

### Access Django Admin
1. Go to http://127.0.0.1:8000/admin
2. Login with: **Prodigy** / [your password]
3. Click "Custom users" to manage users
4. Use bulk actions for multiple users
5. View individual user details and security info

### Access React Admin Panel
1. Go to http://localhost:5173/admin
2. Login with your admin account
3. Navigate between Dashboard, Users, and System tabs
4. Use inline actions for quick user management
5. Monitor system health and statistics

## 🔧 Admin Capabilities

### User Management
```
✅ View all users with detailed information
✅ Send verification emails individually or in bulk
✅ Manually verify user accounts
✅ Activate/deactivate user accounts
✅ Reset failed login attempts
✅ Promote users to admin role
✅ View user login history and security status
✅ Monitor account lock status
```

### System Administration
```
✅ Monitor system health and status
✅ View email service configuration
✅ Track user registration trends
✅ Monitor authentication system status
✅ View CORS and security configuration
✅ Access Django's full admin interface
```

### Security Features
```
✅ Account locking after failed attempts
✅ Failed login attempt tracking
✅ Admin-only access controls
✅ JWT token management
✅ Email verification enforcement
✅ Role-based permissions
```

## 📧 Email Management

### From Django Admin:
- Select users → Actions → "Send verification emails"
- Individual user page → Send verification email
- Bulk verify users without email requirement

### From React Admin:
- User Management tab → Click email icon for individual users
- Dashboard shows verification status for all users
- Quick actions for unverified users

## 🔒 Security Controls

### Account Locking:
- Automatic lock after 5 failed login attempts
- 30-minute lockout period
- Admin can reset attempts instantly
- Visual indicators for locked accounts

### Role Management:
- Two roles: 'user' and 'admin'
- Admin promotion/demotion capabilities
- Role-based access to admin interfaces
- Visual role badges and indicators

## 📱 Mobile & Responsive

Both admin interfaces are fully responsive:
- ✅ Mobile-friendly Django admin
- ✅ Responsive React admin panel
- ✅ Touch-friendly controls
- ✅ Optimized for tablets and phones

## 🎯 Quick Admin Tasks

### Daily Admin Tasks:
1. **Check Dashboard** - Monitor new registrations and system health
2. **Review Unverified Users** - Send verification emails as needed
3. **Monitor Locked Accounts** - Reset failed attempts for legitimate users
4. **System Health Check** - Verify all services are running properly

### Weekly Admin Tasks:
1. **User Activity Review** - Check recent user activity and trends
2. **Security Audit** - Review failed login attempts and security logs
3. **Email System Check** - Verify email delivery and templates
4. **Database Maintenance** - Monitor user growth and system performance

## 🔗 Quick Links

- **Django Admin**: http://127.0.0.1:8000/admin
- **React Admin**: http://localhost:5173/admin
- **User Registration**: http://localhost:5173/register
- **Login Page**: http://localhost:5173/login
- **Email Viewer**: http://localhost:5173/email-viewer

## 🆘 Troubleshooting

### Common Issues:
- **Can't access admin**: Ensure user has admin role
- **Email not sending**: Check SMTP configuration in Django admin
- **Users can't verify**: Check email service status
- **Stats not loading**: Refresh admin panel or check API endpoints

### Admin Account Recovery:
```bash
# Create new superuser if needed
python manage.py createsuperuser

# Reset admin password
python manage.py changepassword [username]
```

Your admin dashboard system is now fully operational with comprehensive user management, system monitoring, and security controls! 🎉