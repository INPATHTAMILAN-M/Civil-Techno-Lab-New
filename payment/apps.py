from django.apps import AppConfig

class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        import payment.audit
        import payment.signals.quatation_signals
        import payment.signals.invoice_signals
