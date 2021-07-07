from werkzeug.exceptions import abort
from app.repository.advertisement_db import Advertisement
from app.repository.campaign_db import Campaign
from app.repository.database import db
from app.rbac import rbac
from datetime import date, datetime
from flask import request
import app.config as config
import requests
from dateutil import parser as date_parser


import logging

logger = logging.getLogger(__name__)

def create_campaign(campaign_dict):
    user = rbac.get_current_user()
    post_dict = campaign_dict['post']

    product_id = post_dict['product_id']
    if product_id == '':
        product_id = None
    else:
        product_id = int(product_id)
    del post_dict['product_id']


    post_id = create_post(post_dict)

    if campaign_dict['count'] < 2 and campaign_dict['campaign_type'] != 'single':
        abort(404, "Multiple Campaign has to happen at least twice")

    del campaign_dict['post']
    campaign_dict['agent_id'] = user.id

    campaign = Campaign(**campaign_dict)
    campaign.timestamp = datetime.now()

    db.session.add(campaign)

    add_advertisements(campaign, post_id, product_id)

    db.session.commit()

    return campaign

def create_post(post_dict):
    r = requests.post(
        f"{config.POST_SERVICE_URL}/post",
        json=post_dict,
        headers={ "Authorization": request.headers.get("Authorization") }
    )
    if r.status_code != 200:
        r.raise_for_status()

    post_id = r.json()['id']

    return post_id

def add_advertisements(campaign, post_id, product_id=None):
    if (campaign.campaign_type == "single"):
        advert = Advertisement(date_of_publishing=campaign.start, post_id=post_id, timestamp=datetime.now(), product_id=product_id)
        campaign.advertisements.append(advert)
        db.session.add(advert)
        return

    start = int(date_parser.parse(campaign.start).timestamp())
    end = int(date_parser.parse(campaign.end).timestamp())
    diff = (end-start)//(campaign.count-1)
    logger.error(f"Date of publishing {start}")
    logger.error(f"Date of publishing {diff}")
    for t in range(start, end+1, diff):
        logger.error(f"Date of publishing {t}")
        date_of_publishing=datetime.fromtimestamp(t)
        advert = Advertisement(date_of_publishing=date_of_publishing, post_id=post_id, timestamp=datetime.now(), product_id=product_id)
        campaign.advertisements.append(advert)
        db.session.add(advert)
