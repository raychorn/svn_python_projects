from django.contrib import admin

from models import SampleHeatMapData

class SampleHeatMapDataAdmin(admin.ModelAdmin):
    list_display = ('heat_gps','heat_lat','heat_lng','heat_x','heat_y','heat_num','data_name','data_value','timestamp')
    search_fields = ('heat_gps','heat_lat','heat_lng','heat_x','heat_y','heat_num','data_name','data_value')
    ordering = ['heat_gps','heat_lat','heat_lng','heat_x','heat_y','heat_num','data_name','data_value']

admin.site.register(SampleHeatMapData, SampleHeatMapDataAdmin)

