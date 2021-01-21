from django import forms

from geopackages.models import Geopackage

from base.forms.processing_forms import ResourceBaseCleanFileForm


class ResourceFormMixin(forms.ModelForm):
    class Meta:
        model = Geopackage
        fields = ['file', 'thumbnail_image', 'name', 'description', ]


class UploadForm(ResourceBaseCleanFileForm, ResourceFormMixin):
    """Upload Form."""


class UpdateForm(ResourceFormMixin):
    """GeoPackage Update Form."""
