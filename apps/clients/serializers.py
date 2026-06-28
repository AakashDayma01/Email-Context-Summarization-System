from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    firm = serializers.StringRelatedField()
    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "firm",
            "created_at",
        ]