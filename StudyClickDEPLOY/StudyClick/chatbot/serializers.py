
from rest_framework import serializers
from .models import Chat, QuestionExamples, StudyField

class QuestionExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionExamples
        fields = '__all__'

class StudyFieldSerializer(serializers.ModelSerializer):
    questions = QuestionExampleSerializer(many=True, read_only=True)
    class Meta:
        model = StudyField
        fields = ['id', 'name', 'questions', 'prompt']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    history_id = serializers.CharField(required=True)
    session_id = serializers.CharField(required=True)
    study_field_id = serializers.IntegerField(required=True)
