from models import District, Campus
from rest_framework import viewsets
from serializers import DistrictSerializer, CampusSerializer, DistrictsSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = District.objects.all()
    serializer_class = DistrictsSerializer


class CampusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer

    