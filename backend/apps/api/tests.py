import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
@pytest.mark.django_db
def test_create_application():
    user=User.objects.create_user('demo','demo@example.com','pass1234')
    client=APIClient(); client.force_authenticate(user=user)
    r=client.post('/api/applications/',{'company':'Acme','role':'Python Developer','status':'applied'},format='json')
    assert r.status_code==201
    assert r.data['company']=='Acme'