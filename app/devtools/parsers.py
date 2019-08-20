import os
import re
import json
import requests

from decimal import Decimal
from datetime import datetime

from django.conf import settings

from parties.models import DemoPartyLocation, DemoPartySeries, DemoParty


def str2date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def read_file(filepath):
    with open(filepath, 'rb') as raw_data:
        data = raw_data.read()
    return data


def get_data(slug=None):
    if not slug:
        filepath = os.path.join(settings.BASE_DIR, 'parties', 'fixtures', 'payback-2013.json')
        data = read_file(filepath)
        json_data = json.loads(data)
    else:
        res = requests.get(url=f"https://www.demoparty.net/api/v1_parties.php?slug={slug}")
        if res.status_code == requests.codes.ok:
            json_data = res.json()
        else:
            json_data = dict()
    return json_data


def get_location(json_data):
    location = json_data.get("party").get("location")

    name = location.get("name").strip()
    city = location.get("addr_city").strip()
    address = location.get("addr_street").strip()
    postal_code = location.get("addr_zip").strip()
    latitude = Decimal(location.get("geo_lat").strip())
    longitude = Decimal(location.get("geo_long").strip())
    country = json_data.get("party").get("countryname")

    obj, created = DemoPartyLocation.objects.get_or_create(
        name=name,
        address=address,
        postal_code=postal_code,
        city=city,
        country=country,
        latitude=latitude,
        longitude=longitude,
        defaults={
            'name': name,
            'address': address,
            'postal_code': postal_code,
            'city': city,
            'country': country,
            'latitude': latitude,
            'longitude': longitude
        }
    )

    return obj


def get_demo_party_series(json_data):
    title = json_data.get("party").get("title")
    name = re.sub(r'(.*?)\s?([12]\d{3})', r'\1', title).strip()
    ser, created = DemoPartySeries.objects.get_or_create(
        name=name,
        defaults={'name': name}
    )
    return ser


def get_demo_party(json_data, location):
    party = json_data.get("party")
    name = party.get("title").strip()
    slug = party.get("title_url").strip()
    series = get_demo_party_series(json_data)
    url = party.get("url").strip()
    demo_party_start = str2date(party.get("datestart"))
    demo_party_end = str2date(party.get("dateend"))

    obj, created = DemoParty.objects.get_or_create(
        name=name,
        slug=slug,
        series=series,
        url=url,
        location=location,
        demo_party_start=demo_party_start,
        demo_party_end=demo_party_end,
        defaults={
            'name': name,
            'slug': slug,
            'series': series,
            'url': url,
            'location': location,
            'demo_party_start': demo_party_start,
            'demo_party_end': demo_party_end
        }
    )

    return obj


def import_demo_party(slug=None):
    json_data = get_data(slug)
    if json_data.get("success", False) is not True:
        return print("PIER DATA PASKANA")

    location = get_location(json_data)
    party = get_demo_party(json_data, location)
    return f"CREATED {party}"
