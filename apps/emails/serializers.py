from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):

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