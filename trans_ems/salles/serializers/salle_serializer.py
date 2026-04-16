from rest_framework import serializers
from ..models import Salle

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'slug')
