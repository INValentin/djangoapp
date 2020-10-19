from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'posts'

    def ready(self):
        import posts.signals
