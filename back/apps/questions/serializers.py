from rest_framework import serializers
from .models import Question, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'type', 'difficulty', 'category', 'category_name', 'content', 'options', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_staff:
            self.Meta.fields = self.Meta.fields + ['answer', 'explanation']


class QuestionCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Question
        fields = ['type', 'difficulty', 'category', 'content', 'options', 'answer', 'explanation', 'user']
