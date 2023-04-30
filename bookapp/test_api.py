import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Book, Author
from .serializers import BookSerializer


@pytest.mark.django_db
def test_get_all_books():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    url = reverse('book-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    assert response.data == serializer.data


@pytest.mark.django_db
def test_get_book_detail():
    author = Author.objects.create(first_name="Ivan", last_name="Ivanov", birth_date="2022-01-01")
    book = Book.objects.create(
        title="Test Book",
        description="This is a test book",
        publication_date="2022-01-01",
        author=author
    )
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    url = reverse('book-detail', kwargs={'pk': book.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    serializer = BookSerializer(book)
    assert response.data == serializer.data


@pytest.mark.django_db
def test_create_book():
    client = APIClient()
    author = Author.objects.create(first_name="Ivan", last_name="Ivanov", birth_date="2022-01-01")
    user = User.objects.create_user(username='testuser', password='testpass')
    user.author = author
    user.save()
    client.force_authenticate(user=user)
    url = reverse('book-list')
    data = {
        "title": "New Book",
        "description": "This is a new book",
        "publication_date": "2022-05-01",
        "author": author.id
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.count() == 1
    assert Book.objects.get().title == 'New Book'


@pytest.mark.django_db
def test_update_book():
    author = Author.objects.create(first_name="Ivan", last_name="Ivanov", birth_date="2022-01-01")
    book = Book.objects.create(
        title="Test Book",
        description="This is a test book",
        publication_date="2022-01-01",
        author=author
    )
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    url = reverse('book-detail', kwargs={'pk': book.id})
    data = {
        "title": "Updated Book",
        "description": "This book has been updated",
        "publication_date": "2022-05-01",
        "author": author.id
    }
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert Book.objects.get().title == 'Updated Book'


@pytest.mark.django_db
def test_delete_book():
    author = Author.objects.create(first_name="Ivan", last_name="Ivanov", birth_date="2022-01-01")
    book = Book.objects.create(
    title="Test Book",
    description="This is a test book",
    publication_date="2022-01-01",
    author=author
    )
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    url = reverse('book-detail', kwargs={'pk': book.id})
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0
