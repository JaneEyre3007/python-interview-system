#!/usr/bin/env python
"""初始化数据库和示例数据"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.questions.models import Category, Question

def init_categories():
    categories = [
        {'name': 'Python基础', 'description': 'Python语法、数据类型、控制流等基础知识'},
        {'name': 'Python进阶', 'description': '装饰器、生成器、上下文管理器等进阶内容'},
        {'name': 'Django', 'description': 'Django框架相关题目'},
        {'name': '数据库', 'description': 'SQL、ORM、数据库设计'},
        {'name': '数据结构与算法', 'description': '常见数据结构和算法问题'},
    ]

    for cat_data in categories:
        Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    print(f'初始化了 {len(categories)} 个分类')


def init_sample_questions():
    questions = [
        {
            'type': 'choice',
            'difficulty': 'easy',
            'content': 'Python中哪个关键字用于定义函数？',
            'options': {'A': 'function', 'B': 'def', 'C': 'func', 'D': 'define'},
            'answer': 'B',
            'explanation': 'Python使用def关键字来定义函数。',
        },
        {
            'type': 'choice',
            'difficulty': 'easy',
            'content': '以下哪个不是Python的内置数据类型？',
            'options': {'A': 'list', 'B': 'tuple', 'C': 'array', 'D': 'dict'},
            'answer': 'C',
            'explanation': 'array不是Python的内置数据类型，需要导入array模块或使用numpy。',
        },
        {
            'type': 'fill',
            'difficulty': 'medium',
            'content': 'Python中用于实现多继承的语法是class Child(Parent1, ______):',
            'options': {},
            'answer': 'Parent2',
            'explanation': 'Python支持多继承，使用逗号分隔多个父类。',
        },
        {
            'type': 'short',
            'difficulty': 'medium',
            'content': '请解释Python中的深拷贝和浅拷贝的区别。',
            'options': {},
            'answer': '浅拷贝只复制对象的引用（地址），深拷贝会递归复制所有嵌套对象。浅拷贝使用copy.copy()，深拷贝使用copy.deepcopy()。',
            'explanation': '浅拷贝创建新对象但引用原对象的元素，深拷贝完全独立。',
        },
        {
            'type': 'choice',
            'difficulty': 'hard',
            'content': 'Python的GIL（全局解释器锁）主要影响什么？',
            'options': {
                'A': '多进程并行',
                'B': '多线程并行',
                'C': '内存管理',
                'D': '异常处理'
            },
            'answer': 'B',
            'explanation': 'GIL限制了同一时刻只有一个线程执行Python字节码，影响多线程并行性能。',
        },
    ]

    category = Category.objects.filter(name='Python基础').first()

    for q_data in questions:
        Question.objects.get_or_create(
            content=q_data['content'],
            defaults={**q_data, 'category': category}
        )
    print(f'初始化了 {len(questions)} 道示例题目')


if __name__ == '__main__':
    print('开始初始化数据库...')
    init_categories()
    init_sample_questions()
    print('数据库初始化完成！')
