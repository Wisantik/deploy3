from django.contrib import admin
from .models import Chat, ChatMessage, QuestionExamples, StudyField


@admin.register(StudyField)
class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prompt',)
    search_fields = ('name',)
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    # search_fields = ('title')
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'role', 'message', 'created_at')
    # search_fields = ('chat')
@admin.register(QuestionExamples)
class QuestionExamplesAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'example')
    # search_fields = ('chat')
