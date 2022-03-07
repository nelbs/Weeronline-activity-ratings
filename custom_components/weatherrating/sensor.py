# Sensor for scrape Weeronline.nl
import logging
import datetime
import json
import voluptuous as vol

from homeassistant.util import dt
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME, CONF_SCAN_INTERVAL, CONF_URL, CONF_TYPE)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = 'Information provided by Weeronline.nl'

DEFAULT_NAME = 'Weatherrating'

DEFAULT_TYPE = 'bicycle'

SCAN_INTERVAL = datetime.timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL):
        cv.time_period,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TYPE, default=DEFAULT_TYPE): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    url = config.get(CONF_URL)
    name = config.get(CONF_NAME)
    activity = config.get(CONF_TYPE)
    add_entities([Weatherrating(url, name, activity)], True)

class Weatherrating(RestoreEntity):
    def __init__(self, url, name, activity):
        # initialiseren sensor
        self._url = url
        self._name = name
        self._activity = activity
        self._state = 0
        self._attributes = {'Hardlopen': None, 'Golf': None, 'Watersport': None, 'Wandelen': None, 'Tennis': None, 'Fietsen': None,
                            'Terras': None, 'Barbecue': None, 'Strand': None}
        if activity not in self._attributes:
            _LOGGER.error('Activity ' + str(activity) + ' does not exist. Possible activities are: running, walking, bicycle, barbeque, beach, terrace, golf, wintersport, tennis and waterSport')
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        # Return the unit of measurement of this entity, if any.
        return 

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        # Return the state attributes.
        return self._attributes

    @property
    def icon(self):
        # Icon to use in the frontend.
        icon_dic = {'Hardlopen': 'mdi:run-fast',
                    'Wandelen': 'mdi:walk',
                    'Fietsen': 'mdi:bike',
                    'Barbeque': 'mdi:grill',
                    'Strand': 'mdi:beach',
                    'Terras': 'mdi:glass-cocktail',
                    'Golf': 'mdi:golf',
                    'Tennis': 'mdi:tennis',
                    'Watersport': 'mdi:ski-water'}
                            
        return icon_dic.get(self._activity)

    def update(self):
        import requests
        from bs4 import BeautifulSoup

        activity_ratings = list()
        activities = list()
        response = requests.get(self._url + '/activiteiten')
        data = BeautifulSoup(response.text, 'html.parser')
        # Get activity ratings
        for div in data.find_all('div', class_="styled__Grades-sc-1plaa7g-7 guwBGH"):
            for img in div.find('span', class_="Icon__Container-glcq76-0 ckAteM"):
                activity_ratings.append(int(img['alt'].rsplit("_")[1]))

        # Get activities
        for div in data.find_all('div', class_="styled__ActivityLabel-sc-1plaa7g-6 cplFdr"):
            activities.append(div.text)

        activity_dict = dict(zip(activities, activity_ratings))

        self._state = activity_dict.get(self._activity)
        for activity in activities:
            self._attributes[activity] = activity_dict.get(activity)
