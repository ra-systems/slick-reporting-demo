from django.apps import AppConfig


class SlickExampleConfig(AppConfig):
    name = 'slick_example'

    def ready(self):
        super().ready()
        from . import fields


