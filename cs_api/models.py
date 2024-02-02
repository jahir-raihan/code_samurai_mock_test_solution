from django.db import models

# Create your models here.


class Book(models.Model):
    """
    Model for book
    """
    book_id = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return f'{self.title} - Author is {self.author}'