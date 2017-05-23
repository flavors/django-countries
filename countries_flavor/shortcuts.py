import babel

from django.apps import apps


def get_model(model_name):
    return apps.get_model(app_label=__package__, model_name=model_name)


def get_babel(locale):
    if locale.country is not None:
        cca2 = locale.country.cca2
    else:
        cca2 = None

    try:
        locale = babel.Locale(locale.short_code, cca2)
    except babel.UnknownLocaleError:
        return None
    return locale
