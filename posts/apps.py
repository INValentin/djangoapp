from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'posts'

    def ready(self):
    	try:
	        from posts import signals
	    except ImportError:
	    	pass
