import bson
import datetime
import json
from dateutil.relativedelta import relativedelta


def aggregate_data(dt_from, dt_upto, group_type):
    with open('dump/sampleDB/sample_collection.bson', 'rb') as f:
        data = bson.decode_all(f.read())
    dt_from = datetime.datetime.fromisoformat(dt_from)
    dt_upto = datetime.datetime.fromisoformat(dt_upto)
    aggregated_data = []
    dates = []
    current_date = dt_from
    while current_date <= dt_upto:
        dates.append(current_date)
        if group_type == "month":
            current_date = current_date.replace(day=1) + relativedelta(months=1)
        elif group_type == "day":
            current_date += relativedelta(days=1)
        elif group_type == "hour":
            current_date += relativedelta(hours=1)

    for date in dates:
        date_data = {}

        if group_type == "month":
            date_data["date"] = date.replace(day=1).isoformat()
        elif group_type == "day":
            date_data["date"] = date.isoformat()
        elif group_type == "hour":
            date_data["date"] = date.replace(minute=0, second=0, microsecond=0).isoformat()

        date_data["value"] = 0

        if dt_from <= date <= dt_upto:

            for item in data:
                item_date = item["dt"]
                if dt_from <= item_date <= dt_upto:
                    if group_type == "month" and item_date.month == date.month and item_date.year == date.year:
                        date_data["value"] += item["value"]
                    elif group_type == "day" and item_date.day == date.day and item_date.month == date.month and item_date.year == date.year:
                        date_data["value"] += item["value"]
                    elif group_type == "hour" and item_date.replace(minute=0, second=0, microsecond=0) == date.replace(
                            minute=0, second=0, microsecond=0):
                        date_data["value"] += item["value"]

        aggregated_data.append(date_data)

    response = {}
    response["dataset"] = [date_data["value"] for date_data in aggregated_data]
    response["labels"] = [date_data["date"] for date_data in aggregated_data]

    return json.dumps(response)
