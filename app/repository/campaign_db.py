from datetime import datetime
from .database import db
from dataclasses import dataclass, field


@dataclass
class Campaign(db.Model):
    id: int
    campaign_type: str
    agent_id: int
    min_age: int
    max_age: int
    gender: str
    country: str
    deleted: bool
    count: int
    start: datetime = field(default_factory=datetime(2000, 1, 1))
    end: datetime = field(default_factory=datetime(2000, 1, 1))
    timestamp: datetime = field(default_factory=datetime(2000, 1, 1))

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    count = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    campaign_type = db.Column(db.String(50))
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    country = db.Column(db.String(50))
    deleted = db.Column(db.Boolean, default=False)
    advertisements = db.relationship("Advertisement", backref="campaign", lazy=True)
