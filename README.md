# Weeronline activity ratings
This platform scrapes the weather activity ratings from https://www.weeronline.nl/. The ratings for the following activities are included as attributes of a sensor.
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
4. Go to https://www.weeronline.nl/, search your city and copy the url
4. Add weatherratings entry to configuration (see below)

## Configuration
```yaml
sensor:
  - platform: weatherratings
    url: 'https://www.weeronline.nl/Europa/Frankrijk/Parijs/4266446'
    name: 'weatherratings'
    type: 'tennis'
```

url: weeronline url of the location you want (required)
name: name of the sensor  (optional) default=weatherratings
type: activity which will be used as the state of the sensor (optional) default=bicycle

