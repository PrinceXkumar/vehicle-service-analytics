from django.apps import AppConfig

class ServicesConfig(AppConfig):
    name = 'services'

    def ready(self):
        # Import signals so they are registered
        import services.signals
