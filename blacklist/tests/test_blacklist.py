import json
from unittest import TestCase
from faker import Faker
from faker.providers import internet, misc
from flask_jwt_extended import create_access_token

from app import app


fake = Faker()
fake.add_provider(internet)
fake.add_provider(misc)

token=fake.pystr(min_chars=16, max_chars=16)

data = 	{
   "email": fake.email(),
   "app_uuid": fake.uuid4(),
   "blocked_reason": fake.paragraph(nb_sentences=1)
}

def test_blacklist_post_200():
  response = app.test_client().post('/blacklists', json=data, headers={"Authorization": f'Bearer {token}'})
  assert response.status_code == 200

def test_blacklist_post_exist_mail_412():
  response = app.test_client().post('/blacklists', json=data, headers={"Authorization": f'Bearer {token}'})
  assert response.status_code == 412

def test_blacklist_post_email_412():
  data = {
     "app_uuid": fake.uuid4(),
     "blocked_reason": fake.paragraph(nb_sentences=1)
  }
  response = app.test_client().post('/blacklists', json=data, headers={"Authorization": f'Bearer {token}'})
  assert response.status_code == 412

def test_blacklist_post_uuid_412():
  data = {
    "email": fake.fake.paragraph(nb_sentences=1),
    "app_uuid": fake.uuid4()
  }
  response = app.test_client().post('/blacklists', json=data, headers={"Authorization": f'Bearer {token}'})
  assert response.status_code == 412

def test_blacklist_post_uuid_412():
  data = {
     "app_uuid": fake.uuid4(),
  }
  response = app.test_client().post('/blacklists', json=data, headers={"Authorization": f'Bearer {token}'})
  assert response.status_code == 412

def test_blacklist_email_get_200():
  token = create_access_token('root')
  expected_response = True 
  response = app.test_client().get(f'/blacklists/pruebas@gmail.com', headers={"Authorization": f'Bearer {token}'})
  assert response.status_code == 200
  assert response.json['exist'] == expected_response
  

def test_blacklist_not_email_get_200():
  token = create_access_token('root')
  expected_response = False 
  response = app.test_client().get(f'/blacklists/${fake.email()}', headers={"Authorization": f'Bearer {token}'})
  response_info= json.loads(response.data.decode('utf-8'))
  assert response.status_code == 200
  assert response.json['exist'] == expected_response
  assert len(list(response_info.keys())) == 1

def test_blacklist_email_invalid_token_get_401():
  token = create_access_token(fake.user_name())
  response = app.test_client().get(f'/blacklists/${fake.email()}', headers={"Authorization": f'Bearer {token}'})
  response_info= json.loads(response.data.decode('utf-8'))
  assert response.status_code == 401
  assert len(list(response_info.keys())) == 1
 

def test_token():
    response = app.test_client().get('/blacklists/token')
    data = response.json
    assert response.status_code == 200
    assert 'access_token' in data

def test_ping():
    response = app.test_client().get('/blacklists/ping')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'pong'
