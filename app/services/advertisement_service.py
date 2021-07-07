from werkzeug.exceptions import abort
from app.repository.advertisement_db import Advertisement
from app.repository.campaign_db import Campaign
from app.repository.database import db
from app.rbac import rbac
from datetime import datetime
from sqlalchemy import desc


def get_advertisements(page=1, page_size=1):
    page = int(page)
    page_size = int(page_size)

    now = datetime.now()

    if page < 1 or page_size < 1:
        abort(404, "Invalid page or page size")

    query = Advertisement.query.filter_by(deleted=False)\
        .filter(Advertisement.date_of_publishing < now)\
        .order_by(desc("date_of_publishing"))\
        .paginate(page=page, per_page=page_size, error_out=False)

    total = query.total

    if page != 1 and total < 1:
        page = 1
        query = Advertisement.query.filter_by(deleted=False)\
            .filter(Advertisement.date_of_publishing < now)\
            .order_by(desc("date_of_publishing"))\
            .paginate(page=page, per_page=page_size, error_out=False)
    advertisements = query.items

    return advertisements