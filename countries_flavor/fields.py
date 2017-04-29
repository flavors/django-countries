from django.core.validators import RegexValidator
from django.db import models


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
