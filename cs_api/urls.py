from django.urls import path
from .views import BookApiView

urlpatterns = [
    path('books', BookApiView.as_view(), name='book_api'),
    path('books/<int:book_id>', BookApiView.as_view(), name='book_api')
]