
from datetime import datetime
from .database import db
from dataclasses import dataclass, field


@dataclass
class Advertisement(db.Model):
    id: int
    deleted: bool
    date_of_publishing: datetime
    post_id: int
    campaign_id: int
    product_id: int
    timestamp: datetime = field(default_factory=datetime(2000, 1, 1))

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    date_of_publishing = db.Column(db.DateTime)
    post_id = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"), nullable=False)
