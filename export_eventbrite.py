import urllib.request, json
import ssl
import sys

from google_cal_connector import get_authenticated_service, getEvent,createEvent

TOKEN = '[[TOKEN]]'
URL_EVENTBRITE_EVENTS = 'https://www.eventbriteapi.com/v3/events/search/?location.address=barcelona&location.within=10km&categories=102&subcategories=2003%2C2004%2C2005&token=' + TOKEN
URL_EVENTBRITE_ORGANISERS = 'https://www.eventbriteapi.com/v3/organizers/'

context = ssl._create_unverified_context()

def getOrganizer(id):
    with urllib.request.urlopen(URL_EVENTBRITE_ORGANISERS + id + '?token=' + TOKEN, context=context) as url:
        data = json.loads(url.read().decode())
        return data['name']

def main(argv):

    with urllib.request.urlopen(URL_EVENTBRITE_EVENTS, context=context) as url:
        data = json.loads(url.read().decode())
        print(data)

    service = get_authenticated_service();

    for event in data['events']:
        link = event['url']
        summary = event['name']['text']
        location = 'Barcelona'
        description = event['description']['text']
        organizer_email = getOrganizer(event['organizer_id'])
        start = event['start']['local']
        end = event['end']['local']
        uid = event['id'] + '@eventbrite'
        timezone = event['start']['timezone']
        myEvent = getEvent(link, summary, location, description, organizer_email, start, end, uid, timezone)
        created_event = createEvent(service, myEvent)
        print('Event created: %s' % (created_event.get('summary')))

if __name__ == '__main__':
    main(sys.argv)



