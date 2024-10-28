from rest_framework import serializers
from .models import LearnerCourse, CourseContent, VideoContent, ImageContent, TextContent, ObjectiveQuestion, ObjectiveOption


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['video_file', 'description']


class ImageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageContent
        fields = ['image_file', 'caption']


class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = ['text']


class ObjectiveOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectiveOption
        fields = ['option_text', 'is_correct']


class ObjectiveQuestionSerializer(serializers.ModelSerializer):
    options = ObjectiveOptionSerializer(many=True)

    class Meta:
        model = ObjectiveQuestion
        fields = ['question_text', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = ObjectiveQuestion.objects.create(**validated_data)
        for option_data in options_data:
            ObjectiveOption.objects.create(question=question, **option_data)
        return question


class CourseContentSerializer(serializers.ModelSerializer):
    video_content = VideoContentSerializer(required=False)
    image_content = ImageContentSerializer(required=False)
    text_content = TextContentSerializer(required=False)
    objective_question = ObjectiveQuestionSerializer(required=False)

    class Meta:
        model = CourseContent
        fields = ['title', 'watch_order', 'video_content', 'image_content', 'text_content', 'objective_question']

    def create(self, validated_data):
        content_type_data = {}
        if 'video_content' in validated_data:
            content_type_data = {'content_object': VideoContent.objects.create(**validated_data.pop('video_content'))}
        elif 'image_content' in validated_data:
            content_type_data = {'content_object': ImageContent.objects.create(**validated_data.pop('image_content'))}
        elif 'text_content' in validated_data:
            content_type_data = {'content_object': TextContent.objects.create(**validated_data.pop('text_content'))}
        elif 'objective_question' in validated_data:
            content_type_data = {'content_object': ObjectiveQuestion.objects.create(**validated_data.pop('objective_question'))}

        return CourseContent.objects.create(**validated_data, **content_type_data)


class LearnerCourseCreateSerializer(serializers.ModelSerializer):
    contents = CourseContentSerializer(many=True)

    class Meta:
        model = LearnerCourse
        fields = ['name', 'description', 'cover_image', 'contents']

    def create(self, validated_data):
        contents_data = validated_data.pop('contents')
        course = LearnerCourse.objects.create(**validated_data)
        for content_data in contents_data:
            CourseContentSerializer().create(validated_data=content_data | {'course': course})
        return course