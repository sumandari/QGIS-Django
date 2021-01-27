from base.serializers import ResourceBaseSerializer

from geopackages.models import Geopackage


class GeopackageSerializer(ResourceBaseSerializer):
    class Meta(ResourceBaseSerializer.Meta):
        model = Geopackage
