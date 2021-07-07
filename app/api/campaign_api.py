from flask_restful import Resource
from flask import jsonify, request
from app.services import campaign_service
from app.rbac import rbac
import logging

logger = logging.getLogger(__name__)

class CampaignAPI(Resource):
    method_decorators = {
        "post": [rbac.Allow(["agent"])],
    }

    def post(self):
        campaign_dict = request.get_json()
        return jsonify(campaign_service.create_campaign(campaign_dict))
