from rest_framework import serializers
from .models import Quiz

# serializer를 통해서 Quizmodel에 있는 데이터를 
# title, body, answer를 담고있는 json타입의 데이터로 변환해준다.
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('title', 'body', 'answer')