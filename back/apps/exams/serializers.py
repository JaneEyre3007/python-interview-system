from rest_framework import serializers
from .models import Exam, Answer, ExamQuestion
from apps.questions.serializers import QuestionSerializer


class AnswerSerializer(serializers.ModelSerializer):
    question_content = serializers.CharField(source='question.content', read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['is_correct', 'score', 'ai_feedback']


class ExamQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = ExamQuestion
        fields = ['id', 'question', 'order', 'score']


class ExamSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['user', 'total_score', 'status']

    def get_questions(self, obj):
        exam_questions = ExamQuestion.objects.filter(exam=obj).select_related('question')
        return ExamQuestionSerializer(exam_questions, many=True).data


class ExamCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    question_count = serializers.IntegerField(default=10, min_value=1, max_value=50)
    question_type = serializers.ChoiceField(choices=['choice', 'fill', 'code', 'short', 'mixed'], default='mixed')
    difficulty = serializers.ChoiceField(choices=['easy', 'medium', 'hard', 'mixed'], default='mixed')


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
