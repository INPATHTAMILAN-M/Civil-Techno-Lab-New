from simple_history import register
from django.contrib.auth.models import User

# Register models that cannot be modified directly
register(User)