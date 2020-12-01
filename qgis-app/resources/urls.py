from django.urls import path

from resources.views import (GeopackageCreateView,
                             GeopackageDetailView,
                             GeopackageUpdateView,
                             GeopackageListView,
                             GeopackageDeleteView,
                             geopackage_review,
                             geopackage_download,)


urlpatterns = [
    #  GeoPackage
    path('geopackages/', GeopackageListView.as_view(), name='geopackage_list'),
    path('geopackages/add/', GeopackageCreateView.as_view(), name='geopackage_create'),
    path('geopackages/<int:pk>/', GeopackageDetailView.as_view(), name='geopackage_detail'),
    path('geopackages/<int:pk>/update/', GeopackageUpdateView.as_view(), name='geopackage_update'),
    path('geopackages/<int:pk>/delete/', GeopackageDeleteView.as_view(), name='geopackage_delete'),
    path('geopackages/<int:pk>/review/', geopackage_review, name='geopackage_review'),
    path('geopackages/<int:pk>/download/', geopackage_download, name='geopackage_download'),
]