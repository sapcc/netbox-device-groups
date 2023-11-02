"""The base model definition for the Plugin."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel

__all__ = ("PluginBaseModel",)


class PluginBaseModel(NetBoxModel):
    """
    Base model class from which all plug-in models inherit.

    This abstract base provides globally common fields and functionality.
    """

    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(verbose_name=_("description"), max_length=200, blank=True)
    comments = models.TextField(verbose_name=_("comments"), blank=True)

    class Meta:
        abstract = True

    @property
    def present_in_database(self):
        """
        True if the record exists in the database, False if it does not.
        """
        return not self._state.adding

    def validated_save(self, *args, **kwargs):
        """
        Perform model validation during instance save.

        This is a convenience method that first calls `self.full_clean()` and then `self.save()`
        which in effect enforces model validation prior to saving the instance, without having
        to manually make these calls seperately. This is a slight departure from Django norms,
        but is intended to offer an optional, simplified interface for performing this common
        workflow during testing.
        """
        self.full_clean()
        self.save(*args, **kwargs)
