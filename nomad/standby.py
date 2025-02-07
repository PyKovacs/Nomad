from datetime import datetime, timedelta

from astral import LocationInfo
from astral.sun import sun

from nomad.settings import get_astral_settings

settings = get_astral_settings()


def get_dusk_dawn(city_name: str) -> tuple[datetime, datetime]:
    """
    Get the sunrise and sunset times for today.
    """
    city = LocationInfo(city_name, timezone=settings.timezone)
    s = sun(city.observer, date=datetime.date(datetime.now()))
    dusk = s["dusk"]
    dawn = s["dawn"]
    return dusk, dawn


def get_standby_from_to(city_name: str = settings.city) -> tuple[datetime, datetime]:
    """
    Get the standby times for today.
    """
    dusk, dawn = get_dusk_dawn(city_name)
    extra_minutes = settings.extra_minutes
    return dusk + timedelta(minutes=extra_minutes), dawn - timedelta(minutes=extra_minutes)
