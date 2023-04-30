from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        author = self.request.user.author
        serializer.save(author=author)

