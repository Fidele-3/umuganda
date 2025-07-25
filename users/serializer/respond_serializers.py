# user/serializer/respond_serializer.py

from rest_framework import serializers
from admn.models.respond import Respond, RespondMedia

class RespondMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespondMedia
        fields = [
            'id',
            'respond',
            'media_file',
            'media_type',
            'uploaded_at',
            'file_size',
            'file_extension',
            'width',
            'height',
            'duration',
        ]


class RespondSerializer(serializers.ModelSerializer):
    media = RespondMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Respond
        fields = [
            'id',
            'responder',
            'report',
            'message',
            'status',
            'concerned_sector',
            'respond_id',
            'created_at',
            'updated_at',
            'media',
        ]
