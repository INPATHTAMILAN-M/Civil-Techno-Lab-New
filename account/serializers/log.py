# auditlog_api/serializers.py

from rest_framework import serializers
from auditlog.models import LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    content_type = serializers.StringRelatedField()
    action = serializers.CharField(source='get_action_display')
    changes = serializers.SerializerMethodField()
    actor = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = [
            'id',
            'actor',
            'timestamp',
            'action',
            'changes',
            'object_pk',
            'content_type',
            'remote_addr',
            'object_repr',
        ]

    def get_actor(self, obj):
        return obj.actor.username  if obj.actor else "System"

    def get_changes(self, obj):
        changes = obj.changes_dict or {}
        formatted = []
        for field, (old, new) in changes.items():
            if field == "report_template":
                formatted.append(f"{field}: [HTML content changed]")
            else:
                formatted.append(f"{field}: {old} → {new}")
            
        return formatted

