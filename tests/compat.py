"""
This file exists to contain all Django and Python compatibility issues.
In order to avoid circular references, nothing should be imported from suit lib.
"""

try:
    from django.urls import reverse
except ImportError:  # Django < 1.10
    from django.core.urlresolvers import reverse
