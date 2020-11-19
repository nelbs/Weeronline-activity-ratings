# Sensor for scrape Weeronline.nl
import logging
import datetime
import json
import voluptuous as vol

from homeassistant.util import dt
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME, CONF_SCAN_INTERVAL, CONF_URL, CONF_ACTIVITY)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = 'Information provided by Weeronline.nl'

DEFAULT_NAME = 'Weatherrating'

DEFAULT_ACTIVITY = 'bicycle'

SCAN_INTERVAL = datetime.timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL):
        cv.time_period,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_ACTIVITY, default=DEFAULT_ACTIVITY): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    url = config.get(CONF_URL)
    name = config.get(CONF_NAME)
    activity = config.get(CONF_ACTIVITY)
    add_entities([Weatherrating(url, name, activity)], True)

class Weatherrating(RestoreEntity):
    def __init__(self, url, name, activity):
        # initialiseren sensor
        self._url = url
        self._name = name
        self._activity = activity
        self._state = 0
        self._attributes = {'running': None, 'walking': None, 'bicycle': None, 'barbecue': None,
                            'beach': None, 'terrace': None, 'golf': None, 'winterSport': None, 'tennis': None,
                            'waterSport': None}
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
    def device_state_attributes(self):
        # Return the state attributes.
        return self._attributes

    @property
    def icon(self):
        # Icon to use in the frontend.
        icon_dic = {'running': 'mdi:run-fast',
                    'walking': 'mdi:walk',
                    'bicycle': 'mdi:bike',
                    'barbecue': 'mdi:grill',
                    'beach': 'mdi:beach',
                    'terrace': 'mdi:glass-cocktail',
                    'golf': 'mdi:golf',
                    'winterSport': 'mdi:ski',
                    'tennis': 'mdi:tennis',
                    'waterSport': 'mdi:ski-water'}
                            
        return icon_dic.get(self._activity)

    def update(self):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(self._url)
        data = BeautifulSoup(response.text, 'html.parser')

        activities = []
        ratings = []
        i = 1
        for div in data.find_all('div', class_="wol-activities-module__activity___2okN7"):
            for img in div.find_all('img', alt=True):
                if i % 2 == 0:
                    ratings.append(int((img['alt']).rsplit("_")[1]))
                else:
                    activities.append(img['alt'])
                i += 1
        result = dict(zip(activities, ratings))
        self._state = result.get(self._activity)
        for activity in activities:
            self._attributes[activity] = result.get(activity)

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state

