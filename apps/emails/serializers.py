from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Email model.

    Converts Email model instances into JSON format for API responses.
    The associated client and accountant are represented using their
    string representations instead of their primary keys.
    """
    accountant = serializers.StringRelatedField()
    client = serializers.StringRelatedField()

    class Meta:
        model = Email
        fields = [
            "id",
            "subject",
            "body",
            "client",
            "accountant",
            "sent_at",
        ]