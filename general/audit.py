from auditlog.registry import auditlog
from general.models import (
    Tax,
    Print_Format,
    Letter_Pad_Logo,
    Material,
    Report_Template,
    Test,
    Expense,
)
    
for model in [Tax, Print_Format, Letter_Pad_Logo, Material, Report_Template,Test, Expense]:
    auditlog.register(model)