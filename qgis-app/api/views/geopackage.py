# api/views/geopackages.py
from api.serializers.geopackage import (GeopackageSerializer,
                                        GeopackageThumbnailSerializer)
from base.views.processing_view import ResourceAPIList, ResourceAPIDetail
from geopackages.views import ResourceMixin

class GeopackageAPIList(ResourceMixin, ResourceAPIList):
    serializer_class = GeopackageSerializer

class GeopackageDetailAPI(ResourceMixin, ResourceAPIDetail):
    serializer_class = GeopackageThumbnailSerializer