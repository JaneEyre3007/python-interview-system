from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from .models import Exam, Answer, ExamQuestion
from apps.questions.models import Question
from .serializers import ExamSerializer, ExamCreateSerializer, SubmitAnswerSerializer, AnswerSerializer
from apps.ai.mimo_client import evaluate_answer


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exam.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_exam(self, request):
        serializer = ExamCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            queryset = Question.objects.filter(Q(user=request.user) | Q(is_published=True))

            if data['question_type'] != 'mixed':
                queryset = queryset.filter(type=data['question_type'])
            if data['difficulty'] != 'mixed':
                queryset = queryset.filter(difficulty=data['difficulty'])

            questions = list(queryset.order_by('?')[:data['question_count']])

            if len(questions) < data['question_count']:
                return Response(
                    {'error': f'题库中符合条件的题目不足，仅有{len(questions)}道'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            exam = Exam.objects.create(
                user=request.user,
                title=data['title'],
                status='pending'
            )

            for i, question in enumerate(questions):
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    order=i + 1,
                    score=10
                )

            exam.total_score = len(questions) * 10
            exam.save()

            return Response(ExamSerializer(exam).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        exam = self.get_object()
        if exam.status != 'pending':
            return Response({'error': '试卷状态不允许开始'}, status=status.HTTP_400_BAD_REQUEST)

        exam.status = 'in_progress'
        exam.started_at = timezone.now()
        exam.save()
        return Response(ExamSerializer(exam).data)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        exam = self.get_object()
        if exam.status != 'in_progress':
            return Response({'error': '试卷不在进行中'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                question = Question.objects.get(
                    Q(id=serializer.validated_data['question_id']),
                    Q(user=request.user) | Q(is_published=True)
                )
            except Question.DoesNotExist:
                return Response({'error': '题目不存在'}, status=status.HTTP_404_NOT_FOUND)

            user_answer = serializer.validated_data['answer']

            if question.type == 'choice':
                is_correct = user_answer.strip().upper() == question.answer.strip().upper()
                score = 10 if is_correct else 0
                ai_feedback = '回答正确！' if is_correct else f'正确答案是：{question.answer}'
            else:
                try:
                    ai_feedback = evaluate_answer(question.content, question.answer, user_answer, request.user)
                    is_correct = '正确' in ai_feedback and '错误' not in ai_feedback
                    score = 10 if is_correct else 5 if '部分正确' in ai_feedback else 0
                except Exception:
                    is_correct = False
                    score = 0
                    ai_feedback = 'AI评判暂时不可用'

            answer, created = Answer.objects.update_or_create(
                exam=exam,
                question=question,
                defaults={
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'score': score,
                    'ai_feedback': ai_feedback,
                }
            )

            return Response(AnswerSerializer(answer).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        exam = self.get_object()
        if exam.status != 'in_progress':
            return Response({'error': '试卷不在进行中'}, status=status.HTTP_400_BAD_REQUEST)

        exam.status = 'completed'
        exam.finished_at = timezone.now()
        exam.save()

        answers = Answer.objects.filter(exam=exam)
        total_score = sum(answer.score for answer in answers)

        return Response({
            'exam': ExamSerializer(exam).data,
            'total_score': total_score,
            'correct_count': answers.filter(is_correct=True).count(),
            'total_count': exam.questions.count(),
        })

    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        exam = self.get_object()
        answers = Answer.objects.filter(exam=exam).select_related('question')

        return Response({
            'exam': ExamSerializer(exam).data,
            'answers': AnswerSerializer(answers, many=True).data,
            'total_score': sum(a.score for a in answers),
            'correct_count': answers.filter(is_correct=True).count(),
        })
