from django.contrib import admin
from resources.models import Geopackage, GeopackageReview


class GeopackageInline(admin.TabularInline):
    model = GeopackageReview

@admin.register(Geopackage)
class GeopackageAdmin(admin.ModelAdmin):
    inlines = [GeopackageInline, ]
    list_display = ('name', 'description', 'creator', 'upload_date',)
    search_fields = ('name', 'description',)

