from auditlog.registry import auditlog
from django.contrib.auth.models import User
from account.models import (
    Employee,
    State,
    Country,
    City,
    Customer
)
for model in [Employee, State, Country, City, Customer, User]:
    auditlog.register(model)

