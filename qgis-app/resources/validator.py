from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

GPKG_MAX_SIZE = getattr(settings, 'GPKG_MAX_SIZE', 1000000)  # 1MB


def gpkg_validator(gpkg_file):
    """GeoPackage File Validation"""

    print(gpkg_file.getbuffer().nbytes)
    print("-"*100)

    try:
        if gpkg_file.getbuffer().nbytes > GPKG_MAX_SIZE:
            raise ValidationError(
                _("File is too big. Max size is %s Megabytes") % (
                        GPKG_MAX_SIZE / 1000000))
    except AttributeError:
            raise ValidationError(_("Can not calculate filesize."))
    return True
