from base.serializers import (ResourceBaseSerializer,
                              ResourceThumbnailBaseSerializer)

from geopackages.models import Geopackage


class GeopackageSerializer(ResourceBaseSerializer):
    class Meta(ResourceBaseSerializer.Meta):
        model = Geopackage


class GeopackageThumbnailSerializer(ResourceThumbnailBaseSerializer):
    class Meta(ResourceThumbnailBaseSerializer.Meta):
        model = Geopackage