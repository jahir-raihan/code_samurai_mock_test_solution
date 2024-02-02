from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializer import BookSerializer


class BookApiView(APIView):

    """
    View for api endpoints of book.
    """

    def get(self, request, book_id=None):

        """
        Get method for getting & filtering books data
        :param request:
        :param queryset:
        :return: queryset
        """

        many = False
        # If book id provided then return only that book or error
        if book_id:

            try:
                books = Book.objects.get(book_id=book_id)
            except:
                return Response({"message": f"book with id: {book_id} was not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            books = Book.objects.all().order_by('book_id')
            many = True

        query = request.GET

        if 'title' in query:
            title = query.get('title')
            books = books.filter(title=title)
        if 'author' in query:
            author = query.get('author')
            books = books.filter(author=author)
        if 'genre' in query:
            genre = query.get('genre')
            books = books.filter(genre=genre)
        if 'sort' in query:

            order_in = '-' if query.get('order') == 'DESC' else ''
            sort_by = order_in + query.get('sort')
            books = books.order_by(sort_by)

        if 'order' in query and 'sort' not in query:
            order_in = '-' if query.get('order') == 'DESC' else ''
            sort_by = order_in + 'book_id'
            books = books.order_by(sort_by)

        book_serializer = BookSerializer(books, many=many)
        if many:
            return Response({"books": book_serializer.data}, status=status.HTTP_200_OK)
        return Response(book_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        post_data = request.data

        book = Book()
        book.book_id = int(post_data['id'])
        book.title = post_data['title']
        book.author = post_data['author']
        book.genre = post_data['genre']
        book.price = float(post_data['price'])
        book.save()

        serialized_data = BookSerializer(book, many=False)

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def put(self, request, book_id):
        # Extract data from the request
        put_data = request.data

        # Check if a book with the given book_id  exists
        try:
            book = Book.objects.get(book_id=book_id)
        except:
            # If the book doesn't exist, return error response
            return Response({"message": f"book with id: {book_id} was not found"},
                            status=status.HTTP_404_NOT_FOUND)

        # Update the book data
        book.title = put_data.get('title', book.title)
        book.author = put_data.get('author', book.author)
        book.genre = put_data.get('genre', book.genre)
        book.price = float(put_data.get('price', book.price))

        # Save the updated/created book
        book.save()

        # Serialize and return the updated/created book data
        serialized_data = BookSerializer(book, many=False)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

