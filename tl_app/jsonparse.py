from django.test import RequestFactory
from .views import upload

factory=RequestFactory()
req=factory.post('/upload/')
response=upload(req)