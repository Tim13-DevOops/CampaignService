from flask_restful import Resource
from flask import jsonify, request, abort
from app.services import advertisement_service
from app.rbac import rbac
import logging
import json

logger = logging.getLogger(__name__)

class AdvertisementAPI(Resource):

    def get(self):
        return jsonify(advertisement_service.get_advertisements(**request.args))