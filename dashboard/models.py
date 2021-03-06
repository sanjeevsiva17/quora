from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)


class Answer(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=2000)

    @classmethod
    def already_answered(cls, question_id, user_id):
        return cls.objects.filter(
            question=question_id,
            user=user_id).exists()


class Vote(TimeStampMixin):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # count = models.IntegerField(default=0)

    @classmethod
    def upvote_or_delete(cls, answer_id, user_id):
        vote = cls.objects.filter(answer_id=answer_id, user_id=user_id)
        if vote.exists():
            vote.delete()
        else:
            Vote.objects.create(answer_id=answer_id, user_id=user_id)

        count = cls.objects.filter(answer_id=answer_id).count()
        return count



class Comment(TimeStampMixin):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=2000)
