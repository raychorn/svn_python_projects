from models import District, Campus
from rest_framework import serializers

from django.db import models

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ('name', 'campusid', 'datecreated')


class DistrictSerializer(serializers.ModelSerializer):
    campuses = serializers.RelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return District(**validated_data)

    def update(self, instance, validated_data):
        instance.districtid = validated_data.get('districtid', instance.email)
        instance.name = validated_data.get('name', instance.content)
        instance.datecreated = validated_data.get('datecreated', instance.created)
        instance.campusid = validated_data.get('campusid', instance.email)
        return instance
    
    class Meta:
        model = District


class DistrictsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District

        