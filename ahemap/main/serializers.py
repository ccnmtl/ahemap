from rest_framework import serializers
from ahemap.main.models import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Institution
        fields = ('id', 'title', 'latlng')
