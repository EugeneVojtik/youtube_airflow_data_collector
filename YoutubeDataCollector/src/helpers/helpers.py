"""
This module contains helper functions for dags
"""
from isodate import parse_duration


def convert_duration_to_minutes(iso_date: str) -> float:
    """
    Method for conversion of iso_date format string to Float with number of minutes
    """
    return parse_duration(iso_date).seconds / 60
