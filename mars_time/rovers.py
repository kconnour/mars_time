"""The rovers module is a collection of constants related to rover landings and end of life.
"""
import datetime

opportunity_landing_date: datetime.datetime = datetime.datetime(2004, 1, 25, 5, 5, 0, 0, tzinfo=datetime.timezone.utc)
"""Time when the Opportunity (MER-B) rover landed."""

opportunity_last_contact_date: datetime.datetime = datetime.datetime(2018, 6, 10, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
"""Time when the Opportunity (MER-B) rover had last contact."""

perseverance_landing_date: datetime.datetime = datetime.datetime(2021, 2, 18, 20, 55, 0, 0, tzinfo=datetime.timezone.utc)
"""Time when the Perseverance rover from the Mars 2020 mission landed."""
