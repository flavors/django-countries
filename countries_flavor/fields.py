from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.db import models


def get_many_to_one_fields(model):
    return [
        field for field in model._meta.get_fields()
        if field.is_relation and field.many_to_one
    ]


def get_non_self_reference_fields(model):
    return [
        field for field in models.Country._meta.many_to_many
        if field not in get_self_reference_fields()
    ]


def get_one_to_many_fields(model):
    return [
        field for field in model._meta.get_fields()
        if field.is_relation and
        field.one_to_many and
        not isinstance(field, GenericRelation)
    ]


def get_self_reference_fields(model):
    return [
        field for field in model._meta.get_fields()
        if field.is_relation and field.related_model == model
    ]


class CodeISOField(models.CharField):
    description = 'code ISO field using fixed length'

    def __init__(self, verbose_name, length, regex, *args, **kwargs):
        self.length = length
        self.regex = regex

        kwargs.update({
            'max_length': length,
            'validators': [RegexValidator(
                regex=r"^{regex}{{{length}}}$".format(
                    regex=regex,
                    length=length)
            )]
        })

        super(CodeISOField, self).__init__(verbose_name, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CodeISOField, self).deconstruct()
        kwargs['length'] = self.length
        kwargs['regex'] = self.regex
        return name, path, args, kwargs
