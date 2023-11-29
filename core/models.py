from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField()

class Song(models.Model):

    TYPES = (
        ('happy','happy'),
        ('sad','sad'),
        ('fear','fear'),
        ('angry','angry'),
        ('disgust','disgust'),
        ('surprise','surprise'),
        ('neutral','neutral'),

    )

    name = models.CharField(max_length=150);
    type = models.CharField(choices= TYPES,max_length= 50);
    link = models.CharField(max_length= 1000)

    def __str__(self):
        return self.type + " " + self.name;    

class Book(models.Model):
    GENRES = (
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('science fiction', 'Science Fiction'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('historical fiction', 'Historical Fiction'),
        ('self-help', 'Self-Help'),
        ('biography', 'Biography'),
        ('poetry', 'Poetry'),
        # Add more genres as needed
    )

    EMOTIONS = (
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('fear', 'Fear'),
        ('angry', 'Angry'),
        ('disgust', 'Disgust'),
        ('surprise', 'Surprise'),
        ('neutral', 'Neutral'),
        # Add more emotions as needed
    )

    title = models.CharField(max_length=150)
    genre = models.CharField(choices=GENRES, max_length=50)
    author = models.CharField(max_length=150)
    link = models.CharField(max_length=1000)
    emotion = models.CharField(choices=EMOTIONS, max_length=50)

    def __str__(self):
        return f"{self.emotion} - {self.genre} - {self.title} by {self.author}"


class Emotion(models.Model):
    emotion = models.CharField(max_length=50)


# class Conditions(models.Model):

#     TYPES = (
#         ('happy','happy'),
#         ('sad','sad'),
#         ('fear','fear'),
#         ('angry','angry'),
#         ('disgust','disgust'),
#         ('surprise','surprise'),
#         ('neutral','neutral'),

#     )
#     condition = models.CharField(max_length=150);
#     type = models.CharField(choices= TYPES,max_length= 50);

#     def __str__(self):
#         return self.type + " " + self.condition;        