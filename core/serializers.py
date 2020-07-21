from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import UserProfile, ClassRoom, Quiz, Question, QuizAnswer, Answer
from django.utils.translation import gettext as _

from core.permissions import IsTeacherOrSuperuser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.pop('user'), is_staff=True)
        _profile = UserProfile(**validated_data, user=user)
        _profile.save()

        return _profile


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'class_name', 'teacher']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'quiz_name', 'class_room', 'credit']
        extra_kwargs = {
            'class_room': {'read_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'credit']
        extra_kwargs = {
            'quiz': {'read_only': True}
        }


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'quiz_answer', 'answer', 'score']
        extra_kwargs = {
            'score': {'read_only': True}
        }

    def validate(self, attrs):
        question = attrs.get('question')
        quiz_answer = attrs.get('quiz_answer')

        if not quiz_answer.is_active:
            raise serializers.ValidationError(_("Quiz is not active for answering"))

        if question.quiz != quiz_answer.quiz:
            raise serializers.ValidationError(_("Question does not belong to the give session id"))

        if quiz_answer.user_profile != self.context['request'].user.user_profile:
            raise serializers.ValidationError(_("Current user is not the same as session user"))

        return attrs

    def create(self, validated_data):

        try:
            old = Answer.objects.get(question=validated_data.get('question'),
                                     quiz_answer=validated_data.get('quiz_answer'))

            old.answer = validated_data.get('answer')
            old.save()

            return old
        except Answer.DoesNotExist:
            new = Answer(**validated_data)
            new.save()
            return new


class ScoreAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'score']

    def validate_score(self, score):
        if score > self.instance.question.credit:
            raise serializers.ValidationError(_("Score can't be grater than question credit"))
        return score

    def validate(self, attrs):
        if not IsTeacherOrSuperuser.is_teacher_or_superuser(self.instance.question.quiz.class_room.id,
                                                            self.context['request']):
            raise serializers.ValidationError(_("You don't have permission to set score"))

        return attrs


class QuizAnswerDetailedSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAnswer
        fields = ['id', 'quiz', 'user_profile', 'score', 'answers']


class QuizAnswerSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = QuizAnswer
        fields = ['id', 'user_profile', 'quiz', 'score']
        extra_kwargs = {
            'user_profile': {'read_only': True},
            'quiz': {'read_only': True}
        }

    def create(self, validated_data):
        user_profile = self.context['request'].user.user_profile
        try:
            return QuizAnswer.objects.get(user_profile=user_profile,
                                          quiz=validated_data.get('quiz'))
        except QuizAnswer.DoesNotExist:
            question_answer = QuizAnswer(**validated_data, user_profile=user_profile)
            question_answer.save()

            return question_answer


class QuizRetrieveSerializer(serializers.ModelSerializer):
    answers__quiz_answer = QuizAnswerSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'questions', 'answers__quiz_answer']


class ClassRoomRetrieveSerializer(serializers.ModelSerializer):
    students = UserProfileSerializer(many=True)
    quizzes = QuizSerializer(many=True)

    class Meta:
        model = ClassRoom
        fields = ['id', 'class_name', 'teacher', 'students', 'quizzes']
