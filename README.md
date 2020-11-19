# Weather ratings
This platform scrapes the weather activity ratings from weeronline.nl. The ratings for the following activities are included as attributes of a sensor.
- Running
- Walking
- Bicycle
- Barbeque
- Beach
- Terrace
- Golf
- Wintersport
- Tennis
- Watersport

## HACS Installation
1. Make sure you've installed [HACS](https://hacs.xyz/docs/installation/prerequisites)
2. In the integrations tab, search for weatherratings.
3. Install the Integration.
4. Add weatherratings entry to configuration (see below)


## Configuration
```yaml
sensor:
  - platform: weatherratings
    url: 'https://www.weeronline.nl/Europa/Frankrijk/Parijs/4266446'
    name: 'weatherratings'
    type: 'tennis'
```

All the activity ratings are stored as attributes. The state of the sensor is set by the type entry.
