from rest_framework import serializers
from umuganda.models import Fine
from umuganda.models.umugandasession import UmugandaSession
from users.serializer.dashbord_serializer import CustomUserSerializer, UmugandaSessionSerializer

class FineSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    session = UmugandaSessionSerializer(read_only=True)

    class Meta:
        model = Fine
        fields = [
            'id', 'user', 'session', 'amount', 'status',
            'moths_overdue', 'issued_at', 'paid_at',
            'payment_method', 'payment_id',
            'reason', 'claim', 'claim_has_been_approved',
        ]
