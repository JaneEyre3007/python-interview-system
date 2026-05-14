from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from .mimo_client import generate_questions, evaluate_answer
from .models import TokenUsage
from apps.questions.models import Question, Category
from apps.questions.serializers import QuestionSerializer


class GenerateQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        topic = request.data.get('topic', 'Python基础')
        question_type = request.data.get('type', 'choice')
        difficulty = request.data.get('difficulty', 'medium')
        count = request.data.get('count', 1)
        save_to_db = request.data.get('save', True)

        try:
            result = generate_questions(topic, question_type, difficulty, count, request.user)
            questions_data = result.get('questions', [])

            if not questions_data:
                return Response({
                    'error': '生成题目失败',
                    'raw': result.get('raw_response', '')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            saved_questions = []
            if save_to_db:
                for q_data in questions_data:
                    question = Question.objects.create(
                        type=question_type,
                        difficulty=difficulty,
                        content=q_data.get('content', ''),
                        options=q_data.get('options', {}),
                        answer=q_data.get('answer', ''),
                        explanation=q_data.get('explanation', ''),
                        created_by_ai=True
                    )
                    saved_questions.append(question)

                return Response({
                    'message': f'成功生成{len(saved_questions)}道题目',
                    'questions': QuestionSerializer(saved_questions, many=True).data
                })
            else:
                return Response({
                    'message': f'成功生成{len(questions_data)}道题目',
                    'questions': questions_data
                })

        except Exception as e:
            return Response({
                'error': f'生成题目时出错: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EvaluateAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question', '')
        correct_answer = request.data.get('correct_answer', '')
        user_answer = request.data.get('user_answer', '')

        if not question or not user_answer:
            return Response({
                'error': '请提供题目和用户答案'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            feedback = evaluate_answer(question, correct_answer, user_answer, request.user)
            return Response({
                'feedback': feedback
            })
        except Exception as e:
            return Response({
                'error': f'评判答案时出错: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TokenUsageStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)

        records = TokenUsage.objects.filter(created_at__gte=start_date)

        total_stats = records.aggregate(
            total_prompt=Sum('prompt_tokens'),
            total_completion=Sum('completion_tokens'),
            total_tokens=Sum('total_tokens'),
            total_calls=Count('id')
        )

        generate_stats = records.filter(api_type='generate').aggregate(
            prompt_tokens=Sum('prompt_tokens'),
            completion_tokens=Sum('completion_tokens'),
            total_tokens=Sum('total_tokens'),
            call_count=Count('id')
        )

        evaluate_stats = records.filter(api_type='evaluate').aggregate(
            prompt_tokens=Sum('prompt_tokens'),
            completion_tokens=Sum('completion_tokens'),
            total_tokens=Sum('total_tokens'),
            call_count=Count('id')
        )

        daily_stats = records.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            prompt_tokens=Sum('prompt_tokens'),
            completion_tokens=Sum('completion_tokens'),
            total_tokens=Sum('total_tokens'),
            call_count=Count('id')
        ).order_by('date')

        daily_generate = records.filter(api_type='generate').annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total_tokens=Sum('total_tokens'),
            call_count=Count('id')
        ).order_by('date')

        daily_evaluate = records.filter(api_type='evaluate').annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total_tokens=Sum('total_tokens'),
            call_count=Count('id')
        ).order_by('date')

        recent_records = records[:20].values(
            'id', 'api_type', 'prompt_tokens', 'completion_tokens', 'total_tokens', 'model_name', 'created_at'
        )

        def safe_stats(stats):
            return {
                'prompt_tokens': stats['prompt_tokens'] or 0,
                'completion_tokens': stats['completion_tokens'] or 0,
                'total_tokens': stats['total_tokens'] or 0,
                'call_count': stats['call_count'] or 0,
            }

        return Response({
            'total': {
                'prompt_tokens': total_stats['total_prompt'] or 0,
                'completion_tokens': total_stats['total_completion'] or 0,
                'total_tokens': total_stats['total_tokens'] or 0,
                'total_calls': total_stats['total_calls'] or 0,
            },
            'generate': safe_stats(generate_stats),
            'evaluate': safe_stats(evaluate_stats),
            'daily': list(daily_stats),
            'daily_generate': list(daily_generate),
            'daily_evaluate': list(daily_evaluate),
            'recent': list(recent_records)
        })
