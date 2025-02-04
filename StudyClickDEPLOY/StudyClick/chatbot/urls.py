from django.urls import path
from .views import ChatView, add_study_field, get_chat_title, get_chat_titles_by_history_id, get_examples_by_field_id, get_session_ids_by_user, list_study_fields, delete_chat

urlpatterns = [
    path('fields/', list_study_fields, name='list_study_fields'),
    path('chat/', ChatView.as_view(), name='chat_with_gpt'),
    path('chats', get_session_ids_by_user, name='get_session_ids_by_user'),
    path('study-field/questions', get_examples_by_field_id, name='get_examples_by_field_id'),
    path('chat/delete', delete_chat, name='delete_chat'),
    path('chat/get_chat_title', get_chat_title, name='get_chat_title'),
    path('chat/get_chat_titles_by_history_id', get_chat_titles_by_history_id, name='get_chat_titles_by_history_id'),
    path('api/study-fields/', add_study_field, name='add-study-field'),
]
