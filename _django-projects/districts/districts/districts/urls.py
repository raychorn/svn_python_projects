from django.conf.urls import url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'districts', views.DistrictViewSet)
router.register(r'campuses', views.CampusViewSet)
router.register(r'linkeddistricts', views.DistrictViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
