"""A library that provides a Python interface to Nightscout"""
import requests
import hashlib
from nightscout import (
    SGV,
    Treatment,
    Activity,
    ProfileDefinition,
    ProfileDefinitionSet,
)

class Api(object):
    """A python interface into Nightscout

    Example usage:
      To create an instance of the nightscout.Api class, with no authentication:
        >>> import nightscout
        >>> api = nightscout.Api('https://yournightscoutsite.herokuapp.com')
      To use authentication, instantiate the nightscout.Api class with your
      api secret:
        >>> api = nightscout.Api('https://yournightscoutsite.herokuapp.com', api_secret='your api secret')
      To fetch recent sensor glucose values (SGVs):
        >>> entries = api.get_sgvs()
        >>> print([entry.sgv for entry in entries])
    """

    def __init__(self, site_url, api_secret=None):
        """Instantiate a new Api object."""
        self.site_url = site_url
        self.api_secret = api_secret

    def request_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.api_secret:
            headers['api-secret'] = hashlib.sha1(self.api_secret.encode('utf-8')).hexdigest()
        return headers

    def get_sgvs(self, params={}):
        """Fetch sensor glucose values
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_sgvs({'count':0, 'find[dateString][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          A list of SGV objects
        """
        r = requests.get(self.site_url + '/api/v1/entries/sgv.json', headers=self.request_headers(), params=params)
        return [SGV.new_from_json_dict(x) for x in r.json()]

    def get_treatments(self, params={}):
        """Fetch treatments
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_treatments({'count':0, 'find[timestamp][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          A list of Treatments
        """
        r = requests.get(self.site_url + '/api/v1/treatments.json', headers=self.request_headers(), params=params)
        if len(r.content) > 0:
            return [Treatment.new_from_json_dict(x) for x in r.json()]
        else:
            return []

    def get_profiles(self, params={}):
        """Fetch profiles
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_profiles({'count':0, 'find[startDate][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          ProfileDefinitionSet
        """
        r = requests.get(self.site_url + '/api/v1/profile.json', headers=self.request_headers(), params=params)
        return ProfileDefinitionSet.new_from_json_array(r.json())

    def get_activities(self, params={}):
        """Fetch treatments
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_activities({'count':0, 'find[timestamp][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          A list of activities
        """
        r = requests.get(self.site_url + '/api/v1/activity.json', headers=self.request_headers(), params=params)
        if len(r.content) > 0:
            return [Activity.new_from_json_dict(x) for x in r.json()]
        else:
            return []


    def create_activity(self):
        """
        Create a new activity in the API.
        Args:
            activity_data: A dictionary containing the data for the new activity.

        Returns:
            The response from the API.
        """
        activity_data = [
            {
                "timestamp": "2023-10-18T08:30:00.000Z",
                "created_at": "2023-10-18T08:30:00.000Z",
                "activity_type": "Running",
                #"duration_minutes": 60,
                #"distance_km": 5.0,
                #"calories_burned": 400
            },
            {
                "timestamp": "2023-10-18T12:00:00.000Z",
                "created_at": "2023-10-18T12:00:00.000Z",
                "type": "Cycling",
                "duration": 100,
                "eventType": "Cycling",
                #"duration_minutes": 45,
                #"distance_km": 10.0,
                #"calories_burned": 300
            }
        ]

        url = self.site_url + '/api/v1/activity.json'
        response = requests.post(url, json=activity_data, headers=self.request_headers())

        if response.status_code == 201:
            # Activity created successfully
            return response.json()
        else:
            # Handle error
            print(f"Error creating activity. Status code: {response.status_code}")
            return None

    def create_heartrate(self):
        """
        Create a new activity in the API.
        Args:
            activity_data: A dictionary containing the data for the new activity.

        Returns:
            The response from the API.
        """
        activity_data = [
            {
                "timestamp": "2023-10-18T08:30:00.000Z",
                "created_at": "2023-10-18T08:30:00.000Z",
                "activity_type": "Heartrate",
                "value": 70,
                #"duration_minutes": 60,
                #"distance_km": 5.0,
                #"calories_burned": 400
            },
            {
                "timestamp": "2023-10-18T12:00:00.000Z",
                "created_at": "2023-10-18T12:00:00.000Z",
                "eventType": "Heartrate",
                "value": 80,
                #"duration_minutes": 45,
                #"distance_km": 10.0,
                #"calories_burned": 300
            }
        ]

        url = self.site_url + '/api/v1/activity.json'
        response = requests.post(url, json=activity_data, headers=self.request_headers())

        if response.status_code == 201:
            # Activity created successfully
            return response.json()
        else:
            # Handle error
            print(f"Error creating activity. Status code: {response.status_code}")
            return None

    def get_heartrate(self, params={}):
        """Fetch treatments
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_treatments({'count':0, 'find[timestamp][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          A list of activities
        """
        r = requests.get(self.site_url + '/api/v1/activity.json', headers=self.request_headers(), params=params)
        if len(r.content) > 0:
            return [Treatment.new_from_json_dict(x) for x in r.json()]
        else:
            return []

