# yourapp/signals.py

from simple_history.signals import pre_create_historical_record
from civiltech.middleware import get_current_ip

def add_ip_to_history_reason(sender, instance, history_instance, **kwargs):
    ip = get_current_ip()
    if ip:
        history_instance.history_change_reason = ip
    print(ip)

pre_create_historical_record.connect(add_ip_to_history_reason)
