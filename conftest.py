import pytest
from django.test import Client
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
django.setup()


@pytest.fixture(scope='module')
def client():
    return Client()
