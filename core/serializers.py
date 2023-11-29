from rest_framework import serializers
from .models import Photo, Song,Emotion


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', )


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ('emotion',)
