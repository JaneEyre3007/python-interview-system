from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Question, Category
from .serializers import QuestionSerializer, QuestionCreateSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionCreateSerializer
        return QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        question_type = self.request.query_params.get('type')
        difficulty = self.request.query_params.get('difficulty')
        category = self.request.query_params.get('category')

        if question_type:
            queryset = queryset.filter(type=question_type)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if category:
            queryset = queryset.filter(category_id=category)

        return queryset

    @action(detail=False, methods=['get'])
    def random(self, request):
        count = int(request.query_params.get('count', 10))
        questions = Question.objects.order_by('?')[:count]
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': '请提供要删除的题目ID列表'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Question.objects.filter(id__in=ids).delete()
        return Response({'message': f'成功删除 {deleted_count} 道题目'})
