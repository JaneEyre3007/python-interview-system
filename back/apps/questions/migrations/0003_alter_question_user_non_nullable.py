# Generated manually

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def set_default_user(apps, schema_editor):
    Question = apps.get_model("questions", "Question")
    User = apps.get_model("users", "User")
    default_user = User.objects.order_by("id").first()
    if default_user:
        Question.objects.filter(user__isnull=True).update(user=default_user)


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0002_question_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(set_default_user, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="question",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="所属用户",
            ),
        ),
    ]
