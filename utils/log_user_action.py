from account.models import UserActivity

def log_user_activity(user, action, ip, details=None):
    UserActivity.objects.create(
        user=user,
        action=action,
        details=details,
        login_ip=ip
    )
