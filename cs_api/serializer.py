from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):

    """
    Model serializer for serializing Books model data
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.book_id
        return data
