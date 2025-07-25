from rest_framework import serializers
from report.models import CreateReport, ReportStatus
from admn.models.respond import Respond  

class ReportFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respond
        fields = ['message', 'created_at']

class ReportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportStatus
        fields = ['status', 'last_updated']

class UserReportSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    feedback = serializers.SerializerMethodField()

    class Meta:
        model = CreateReport
        fields = ['report_id', 'report_title', 'explanation', 'created_at', 'status', 'feedback']

    def get_status(self, obj):
        status = ReportStatus.objects.filter(report=obj).first()
        return ReportStatusSerializer(status).data if status else None

    def get_feedback(self, obj):
        feedback = Respond.objects.filter(report=obj).first()
        return ReportFeedbackSerializer(feedback).data if feedback else None
