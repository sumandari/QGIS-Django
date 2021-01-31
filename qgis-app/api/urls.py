from django.urls import include, path

from api.views import geopackage


urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    # API
    path('geopackages/', geopackage.GeopackageAPIList.as_view(),
         name='geopackage-list'),
    path('geopackages/<int:pk>/', geopackage.GeopackageDetailAPI.as_view(),
         name='geopackage-detail')
]