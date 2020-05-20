from django.apps import AppConfig


class QuestionbankConfig(AppConfig):
    name = 'questionBank'

    def ready(self):
        import questionBank.signals
