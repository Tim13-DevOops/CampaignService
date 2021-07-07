
from app.app import app
from app.repository.database import db
import pytest
from test.tokens import agent1_token
from datetime import datetime, time, timedelta
import json
import requests_mock
from app.repository.advertisement_db import Advertisement
from app.repository.campaign_db import Campaign

def populate_db():

    campaign = Campaign(
        campaign_type='single',
        agent_id=2,
        min_age=10,
        max_age=19,
        gender='female',
        country='Serbia',
        count='1',
        start=datetime.now(),
        end=datetime.now() + timedelta(days=1),
        timestamp=datetime.now()
    )

    advert1 = Advertisement(
        date_of_publishing=datetime.now(),
        post_id=1,
        product_id=None,
        timestamp=datetime.now() - timedelta(days=1)
    )
    advert2 = Advertisement(
        date_of_publishing=datetime.now(),
        post_id=1,
        product_id=None,
        timestamp=datetime.now() - timedelta(days=1)
    )
    advert3 = Advertisement(
        date_of_publishing=datetime.now(),
        post_id=1,
        product_id=None,
        timestamp=datetime.now() + timedelta(days=1)
    )

    campaign.advertisements.append(advert1)
    campaign.advertisements.append(advert2)
    campaign.advertisements.append(advert3)

    db.session.add(campaign)
    db.session.commit()


@pytest.fixture
def client():
    app.config["TESTING"] = True

    db.create_all()

    populate_db()

    with app.app_context():
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all()


def test_post_single_campaign(client):
    with requests_mock.Mocker() as mocker:
        mocker.post(
            "http://api_gateway:8000/post/post", json={'id': 2}
        )

        campaign_dict = {
            'campaign_type': 'single',
            'min_age': 10,
            'max_age': 19,
            'gender': 'male',
            'country': 'Serbia',
            'count': 1,
            'start': (datetime.now() - timedelta(days=1)).isoformat(),
            'end': (datetime.now() + timedelta(days=1)).isoformat(),
            'post': {
                'image': "image1.jpg",
                'description':"description1",
                'product_id': '',
            }
        }

        result = client.post("/campaign", json=campaign_dict, headers={"Authorization": "Bearer " + agent1_token, 'content-type': 'application/json'})
        

        assert result.json["campaign_type"] == "single"
        assert result.json["min_age"] == 10
        assert result.json["max_age"] == 19
        assert result.json["gender"] == "male"
        assert result.json["country"] == "Serbia"
        assert result.json["count"] == 1
        assert result.json["start"] != None
        assert result.json["end"] != None

    params = {
        'page_size': 3
    }
        
    result = client.get('/advertisement', query_string=params)

    assert len(result.json) == 3

def test_post_multi_campaign(client):
    with requests_mock.Mocker() as mocker:
        mocker.post(
            "http://api_gateway:8000/post/post", json={'id': 2}
        )

        campaign_dict = {
            'campaign_type': 'multi',
            'min_age': 10,
            'max_age': 19,
            'gender': 'male',
            'country': 'Serbia',
            'count': 3,
            'start': (datetime.now() - timedelta(days=2)).isoformat(),
            'end': (datetime.now() + timedelta(days=1)).isoformat(),
            'post': {
                'image': "image1.jpg",
                'description':"description1",
                'product_id': 1,
            }
        }

        result = client.post("/campaign", json=campaign_dict, headers={"Authorization": "Bearer " + agent1_token, 'content-type': 'application/json'})
        

        assert result.json["campaign_type"] == "multi"
        assert result.json["min_age"] == 10
        assert result.json["max_age"] == 19
        assert result.json["gender"] == "male"
        assert result.json["country"] == "Serbia"
        assert result.json["count"] == 3
        assert result.json["start"] != None
        assert result.json["end"] != None

    params = {
        'page_size': 3
    }
        
    result = client.get('/advertisement', query_string=params)

    assert len(result.json) == 3


def test_get_advertisement(client):
    result = client.get('/advertisement')

    assert len(result.json) == 1

    params = {
        'page_size': 3
    }
    result = client.get('/advertisement', query_string=(params))

    assert len(result.json) == 3
