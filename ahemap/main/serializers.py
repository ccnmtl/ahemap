from rest_framework import serializers
from ahemap.main.models import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):

    lat = serializers.SerializerMethodField(read_only=True)
    lng = serializers.SerializerMethodField(read_only=True)

    def get_lat(self, obj):
        return obj.latlng.coords[0]

    def get_lng(self, obj):
        return obj.latlng.coords[1]

    class Meta:
        model = Institution
        fields = ('id', 'title', 'lat', 'lng')
