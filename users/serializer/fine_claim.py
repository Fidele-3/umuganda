# serializers/fine_claim.py
from rest_framework import serializers
from umuganda.models import Fine

class FineClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ['id', 'reason', 'claim']  
        read_only_fields = ['id', 'claim']  

    reason = serializers.CharField(write_only=True)
