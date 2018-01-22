from django.apps import apps


def get_model(model_name):
    return apps.get_model(app_label=__package__, model_name=model_name)
