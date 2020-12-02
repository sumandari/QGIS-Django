from django.urls import path

from resources.views import (GeopackageCreateView,
                             GeopackageDetailView,
                             GeopackageUpdateView,
                             GeopackageListView,
                             GeopackageDeleteView,
                             GeopackageUnapprovedListView,
                             GeopackageRequireActionListView,
                             geopackage_review,
                             geopackage_download,
                             geopackage_nav_content,)


urlpatterns = [
    #  GeoPackage
    path('geopackages/', GeopackageListView.as_view(), name='geopackage_list'),
    path('geopackages/add/', GeopackageCreateView.as_view(), name='geopackage_create'),
    path('geopackages/<int:pk>/', GeopackageDetailView.as_view(), name='geopackage_detail'),
    path('geopackages/<int:pk>/update/', GeopackageUpdateView.as_view(), name='geopackage_update'),
    path('geopackages/<int:pk>/delete/', GeopackageDeleteView.as_view(), name='geopackage_delete'),
    path('geopackages/<int:pk>/review/', geopackage_review, name='geopackage_review'),
    path('geopackages/<int:pk>/download/', geopackage_download, name='geopackage_download'),

    path('geopackages/unapproved/', GeopackageUnapprovedListView.as_view(),
         name='geopackage_unapproved'),
    path('geopackages/require_action/', GeopackageRequireActionListView.as_view(),
         name='geopackage_require_action'),

    #JSON
    path('geopackages/sidebarnav/', geopackage_nav_content, name="geopackage_nav_content"),
]