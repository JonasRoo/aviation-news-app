from celery import shared_task
from data.fetch_data import fetch_data_from_all_sources
from .models import Source


@shared_task
def fetch_data():
    fetch_data_from_all_sources()


@shared_task
def create_dummy_source_for_name(name):
    s = Source.objects.create(name=name, base_url="https://google.com", icon_url="https://google.com")
    s.save()


@shared_task
def send_notif():
    print("it's working!")


def create_dummy_sources_task():
    create_dummy_source_for_name(name="dummysource")