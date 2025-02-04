from django.db import models
from django.utils.translation import gettext_lazy as _

class StudyField(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField()

    def __str__(self):
        return self.name

class QuestionExamples(models.Model):
    field = models.ForeignKey(StudyField, verbose_name=_("сфера обучения"), related_name='questions', on_delete=models.CASCADE)
    example = models.CharField(_("пример вопроса"), max_length=255)


class Chat(models.Model):
    history_id = models.CharField(max_length=100, unique=False)
    title = models.CharField(max_length=255)
    # Уникальный идентификатор сессии
    session_id = models.CharField(max_length=100, unique=True)
    study_field = models.ForeignKey(
        StudyField, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=50, choices=[
                            ('user', 'User'), ('bot', 'Bot')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Сортировка по времени создания

    def __str__(self):
        # Отображает первые 20 символов сообщения
        return f"{self.role}: {self.message[:20]}..."


