from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.

    Converts Client model instances into JSON format for API responses.
    The associated firm is represented using its string representation
    instead of its primary key.
    """

    firm = serializers.StringRelatedField()

    class Meta:
        """
        Metadata for the ClientSerializer.
        Specifies the model and fields to be included in the serialized output.
        """
        model = Client
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "firm",
            "created_at",
        ]