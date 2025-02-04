from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, ChatMessage, QuestionExamples, StudyField
from .serializers import ChatMessageSerializer, ChatSerializer, QuestionExampleSerializer, StudyFieldSerializer
import openai
from openai import OpenAI
from django.conf import settings
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework.views import APIView
client = OpenAI(
    api_key="sk-IdmJMXNU1gZPbd1Isu38a1IqFVW3jZQ0",
    base_url="https://api.proxyapi.ru/openai/v1",
)

@extend_schema(summary="показать все сферы для обучения", tags=['Сферы обучения'], request=StudyFieldSerializer)
@api_view(['GET'],)
def list_study_fields(request):
    fields = StudyField.objects.all()
    serializer = StudyFieldSerializer(fields, many=True)
    return Response(serializer.data)


class ChatView(APIView):
    @extend_schema(
        summary="Отправить сообщение",
        request=ChatSerializer,
        responses={
            200: OpenApiResponse(
                description="Успешный ответ",
                examples=[
                    OpenApiExample(
                        'Пример ответа',
                        value={"response": "Ваш ответ от бота."}
                    ),
                ]
            ),
            400: OpenApiResponse(
                description="Ошибка валидации",
                examples=[
                    OpenApiExample(
                        'Пример ошибки',
                        value={"error": "Message, session_id, and study_field_id are required."}
                    ),
                ]
            ),
            404: OpenApiResponse(
                description="Область исследования не найдена",
                examples=[
                    OpenApiExample(
                        'Пример ошибки',
                        value={"error": "StudyField not found."}
                    ),
                ]
            ),
        },
        # parameters=[
        #     OpenApiParameter(name='session_id', description='ID сессии', required=True, type=str),
        #     OpenApiParameter(name='study_field_id', description='ID области исследования', required=True, type=str)
        # ]
    )
    def post(self, request):
        # Используйте сериализатор для валидации и обработки данных
        serializer = ChatSerializer(data=request.data)
        # Валидация и создание исключений при ошибках
        serializer.is_valid(raise_exception=True)
        history_id = serializer.validated_data['history_id']
        user_message = serializer.validated_data['message']
        session_id = serializer.validated_data['session_id']
        study_field_id = serializer.validated_data['study_field_id']

        if not all([user_message, session_id, study_field_id, history_id]):
            return Response({"error": "Message, session_id, and study_field_id are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Получаем область исследования
        try:
            study_field = StudyField.objects.get(id=study_field_id)
        except StudyField.DoesNotExist:
            return Response({"error": "StudyField not found."}, status=status.HTTP_404_NOT_FOUND)

        # Генерируем название чата на основе первого сообщения пользователя
        # Отображаем первые 20 символов
        chat_title = f"Чат по теме: {user_message[:20]}..."

        # Создаем новый чат или получаем существующий
        chat, created = Chat.objects.get_or_create(
            session_id=session_id,
            defaults={'title': chat_title, 'study_field': study_field, 'history_id' : history_id }
        )

        # Сохраняем сообщение пользователя в базе данных
        user_chat_message = ChatMessage(
            chat=chat, role='user', message=user_message)
        user_chat_message.save()

        prompt = study_field.prompt + "\n" + user_message

        messages = []
        messages = [{"role": "user", "content": prompt}]
        # Отправляем запрос в OpenAI
        response_big = client.chat.completions.create(
            # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            n=1,
            # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
            max_tokens=3000,
            # опционально - передача информация об источнике API-вызова
            extra_headers={"X-Title": "My App"},
        )

        response = response_big.choices[0].message.content
        # Сохраняем ответ от OpenAI в базе данных
        ai_chat_message = ChatMessage(chat=chat, role='bot', message=response)
        ai_chat_message.save()
        return Response({"response": response, "history_id" : history_id}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Chat Management"],
        summary="Получить все сообщения из чата",
        parameters=[
                OpenApiParameter(
                    'session_id',  # Имя параметра
                    str,           # Тип параметра (в данном случае строка)
                    OpenApiParameter.QUERY,  # Тип передачи параметра: QUERY - GET параметр
                    description="Уникальный идентификатор сессии чата"  # Описание параметра
                ),
        ],
        responses={
            # Определение ожидаемого ответа
            200: ChatSerializer(many=True),
            400: {"description": "Если параметр session_id не предоставлен"},
            404: {"description": "Чат не найден"},
        }
    )
    def get(self, request):
        # Извлекаем session_id из параметров запроса
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"error": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Извлекаем чат по session_id
        try:
            chat = Chat.objects.get(session_id=session_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # Получаем все сообщения из чата
        messages = chat.messages.values("role", "message", "created_at")
        return Response({"chat_title": chat.title, "messages": messages})

@extend_schema(
    summary="Получить все session_id по history_id.",
    operation_id='getSessionIdsByUser',
    description="Получить все session_id по history_id.",
    parameters=[
        OpenApiParameter('history_id', str, description='ID пользователя для получения session_id', required=True),
    ],
    responses={
        200: OpenApiResponse(
            response=dict,
            description='Список session_id успешно получен.'
        ),
        400: OpenApiResponse(
            description='Ошибка: history_id не указан.'
        ),
        404: OpenApiResponse(
            description='Ошибка: чаты не найдены для данного history_id.'
        ),
    }
)

@api_view(['GET'])
def get_session_ids_by_user(request):
    history_id = request.query_params.get("history_id")

    if not history_id:
        return Response({"error": "history_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем все чаты, связанные с history_id
    chats = Chat.objects.filter(history_id=history_id).values("session_id")

    if not chats:
        return Response({"error": "No chats found for this history_id."}, status=status.HTTP_404_NOT_FOUND)

    # Преобразуем queryset в список и убираем дубликаты session_id
    session_ids = list(set(chat['session_id'] for chat in chats))

    return Response({"session_ids": session_ids}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Сферы обучения'],
    summary="Получить все примеры вопросов для сферы обучения.",
    operation_id='get_examples_by_field_id',
    description="Получить все примеры вопросов для заданной сферы обучения по её ID.",
    parameters=[
        OpenApiParameter('field_id', int, description='ID сферы обучения', required=True),
    ],
    responses={
        200: QuestionExampleSerializer(many=True),
        404: OpenApiResponse(description='Ошибка: Сфера обучения не найдена или нет вопросов.'),
    }
)
@api_view(['GET'])
def get_examples_by_field_id(request):
    field_id = request.query_params.get('field_id')

    if field_id is None:
        return Response({"error": "field_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Получаем вопросы по ID сферы обучения
        examples = QuestionExamples.objects.filter(field_id=field_id)

        if not examples.exists():
            return Response({"error": "No examples found for this field_id."}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionExampleSerializer(examples, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:  # Ловим все ошибки для отладки
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@extend_schema(
    summary="Удалить чат по session_id",
    operation_id="deleteChat",
    tags=["Chat Management"],  # Укажите теги для организации в документации
    description="Удаляет чат по заданному session_id. Необходимо передать session_id в параметрах запроса.",
    parameters=[
        OpenApiParameter("session_id", type=str, required=True, description="Уникальный идентификатор сессии, чата для удаления.")
    ],
    responses={
        200: OpenApiResponse(
            response={"message": "Chat deleted successfully."}, 
            description="Успешное удаление чата."
        ),
        400: OpenApiResponse(
            response={"error": "session_id is required."}, 
            description="Ошибка, если session_id не передан."
        ),
        404: OpenApiResponse(
            response={"error": "Chat not found."}, 
            description="Ошибка, если чат не найден по заданному session_id."
        ),
    },
)
@api_view(['DELETE'])
def delete_chat(request):
    session_id = request.query_params.get("session_id")

    if not session_id:
        return Response({"error": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        chat = Chat.objects.get(session_id=session_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

    chat.delete()

    return Response({"message": "Chat deleted successfully."}, status=status.HTTP_200_OK)

@extend_schema(
    summary="Получить заголовок чата по session_id",
    operation_id="getChatTitle",
    tags=["Chat Management"],
    parameters=[
        OpenApiParameter("session_id", type=str, required=True, description="Уникальный идентификатор сессии чата.")
    ],
    responses={
        200: OpenApiResponse(
            response={"title": "Название чата"},
            description="Успешное получение заголовка чата."
        ),
        400: OpenApiResponse(
            response={"error": "session_id is required."},
            description="Ошибка, если session_id не передан."
        ),
        404: OpenApiResponse(
            response={"error": "Chat not found."},
            description="Ошибка, если чат не найден по заданному session_id."
        ),
    },
)
@api_view(['GET'])
def get_chat_title(request):
    session_id = request.query_params.get("session_id")

    if not session_id:
        return Response({"error": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        chat = Chat.objects.get(session_id=session_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"title": chat.title}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Получить все названия чатов и их session_id по history_id.",
    operation_id='getChatTitlesByHistoryId',
    parameters=[
        OpenApiParameter('history_id', str, description='ID пользователя для получения названий чатов и session_id', required=True),
    ],
    responses={
        200: OpenApiResponse(
            response=dict,
            description='Список названий чатов и их session_id успешно получен.'
        ),
        400: OpenApiResponse(
            description='Ошибка: history_id не указан.'
        ),
        404: OpenApiResponse(
            description='Ошибка: чаты не найдены для данного history_id.'
        ),
    }
)
@api_view(['GET'])
def get_chat_titles_by_history_id(request):
    history_id = request.query_params.get("history_id")

    if not history_id:
        return Response({"error": "history_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем все чаты, связанные с history_id
    chats = Chat.objects.filter(history_id=history_id).values("session_id")

    if not chats:
        return Response({"error": "No chats found for this history_id."}, status=status.HTTP_404_NOT_FOUND)

    # Преобразуем queryset в список и убираем дубликаты session_id
    session_ids = list(set(chat['session_id'] for chat in chats))

    # Получаем названия чатов для каждого session_id
    chat_titles = Chat.objects.filter(session_id__in=session_ids).values("title", "session_id")

    return Response({"chats": list(chat_titles)}, status=status.HTTP_200_OK)

@extend_schema(
    request=StudyFieldSerializer,
    responses={201: StudyFieldSerializer},
)
@api_view(['POST'])
def add_study_field(request):
    serializer = StudyFieldSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)