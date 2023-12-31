from django.core.files.storage import default_storage
from rest_framework.generics import ListAPIView
from .models import Photo,Emotion , Song, Book
from rest_framework.response import Response
# from .serializers import ImageSerializer
from .serializers import ImageSerializer, SongSerializer, BookSerializer, EmotionSerializer
from rest_framework import status
from django.conf import settings
from PIL import Image as PImage
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
from numpy import asarray
from fer import FER
import uuid


def detect_faces(image_path):
    image = PImage.open(default_storage.open(image_path))
    image = image.convert('RGB')
    pixels = asarray(image)

    detector = MTCNN()

    results = detector.detect_faces(pixels)

    detected_faces = list()
    print("emotion extracted")
    for result in results:
        if result['confidence'] > 0.90:
            detected_faces.append({
                "face_id": uuid.uuid4(),
                "confidence": result['confidence'],
                "bounding_box": result['box'],
                "keypoints": result['keypoints']
            })

    return detected_faces


class ImageViewSet(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = ImageSerializer

    
    def post(self, request, *args, **kwargs):
        try:
            print(request.data.keys())
            file = request.data['image']
            if not file:
                return Response({"error": "Image key not found in the request data"}, status=status.HTTP_400_BAD_REQUEST)
            Photo.objects.create(image=file)
            obj = Photo.objects.all().last()
            image = obj.image

            detector = FER(mtcnn=True)
            img = plt.imread(settings.MEDIA_ROOT + "/" + image.name)

            detected_emotions = detector.detect_emotions(img)

            dominant_emotion = max(detected_emotions[0]['emotions'], key=detected_emotions[0]['emotions'].get)

            obj.delete()

            emotion_obj = Emotion.objects.create(emotion=dominant_emotion)
            print("emotion checked ")

            songs = Song.objects.filter(type=dominant_emotion.lower())
            # songs_serialized = [{"id": song.id, "name": song.name, "emotion": song.type, "link": song.link} for song in songs]
            songs_serialized = SongSerializer(songs, many=True).data
            print(songs_serialized)


            books = Book.objects.filter(emotion=dominant_emotion.lower())
            # books_serialized = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre, "link": book.link} for book in books]
            books_serialized = BookSerializer(books, many=True).data
            print(books_serialized)

            return Response({"success": dominant_emotion, "songs": songs_serialized, "books": books_serialized}, status=status.HTTP_202_ACCEPTED)
        except KeyError:
            # Handle the case where the 'image' key is not present in request.data
            return Response({"error": "Image key not found in the request data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other exceptions gracefully
            print(f"Error processing image: {str(e)}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, *args, **kwargs):
        # Retrieve the last posted photo
        last_photo = Photo.objects.last()
        last_emotion = Emotion.objects.last()
        songs = Song.objects.filter(type=last_emotion.emotion.lower())
        books = Book.objects.filter(emotion=last_emotion.emotion.lower())

        emotion_serialized = EmotionSerializer(last_emotion).data
        songs_serialized = SongSerializer(songs, many=True).data
        books_serialized = BookSerializer(books, many=True).data

        response_data = {
            "last_emotion": emotion_serialized,
            "songs": songs_serialized,
            "books": books_serialized,
        }

        return Response(response_data, status=status.HTTP_200_OK)

# class EmotionViewSet(ListAPIView):
#     queryset = Emotion.objects.all()
#     serializer_class = EmotionSerializer


#     def post(self, request, *args, **kwargs):
#         typed = ""; 
#         string = request.data['emotion']
#         conditions = Conditions.objects.filter(condition = string);
#         if(len(conditions) == 0):
#             typed = string;
#         else:
#             typed = conditions[0].type;
#         songs = Song.objects.filter(type = typed);
#         songs = serializers.serialize('json', songs);   
#         print(songs)
        
#         return Response(songs, status=status.HTTP_202_ACCEPTED)


# class ConditionViewSet(ListAPIView):
#     queryset = Emotion.objects.all()
#     serializer_class = EmotionSerializer


#     def post(self, request, *args, **kwargs):

#         string = request.data['emotion']
#         print(string);
#         conditions = Conditions.objects.filter(type = string);
#         conditions = serializers.serialize('json', conditions);   
#         print(conditions)
        
#         return Response(conditions, status=status.HTTP_202_ACCEPTED)
