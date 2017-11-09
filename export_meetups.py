import sys
import urllib.request
from google_cal_connector import get_authenticated_service, getEvent, createEvent

from icalendar import Calendar

meetup_groups = ['Meetup-Open-Data-Barcelona',
                 'Barcelona-Amazon-Web-Services-Meetup',
                 'Barcelona-Software-Craftsmanship',
                 'Meetup-de-Big-Data-de-datahack-en-Barcelona',
                 'Big-Data-Barcelona',
                 'Big-Data-Developers-in-Barcelona',
                 'UXer-Team',
		 'AngularJS-Beers',
		 'BarcelonaTesters',
		 'codeworksbcn',
		 'frontend-barcelona']

def parsefile ( file ):
    events = []
    g = open(file, 'rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            link = component.get('url')
            summary = component.get('summary')
            location = component.get('location')
            description = component.get('description')
            organizer_email = component.get('organizer')
            start = component.get('dtstart').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
            end = component.get('dtend').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
            uid = component.get('uid')
            timezone = component.get('dtstart').dt.tzinfo.zone
            events.append(getEvent(link, summary, location, description, organizer_email, start, end, uid, timezone))
    g.close()
    return events

def main(argv):

    service = get_authenticated_service()

    for meetup_group in meetup_groups:
        url = "http://api.meetup.com/" + meetup_group + "/upcoming.ical"
        file = "upcoming-" + meetup_group + ".ical"
        urllib.request.urlretrieve (url, filename=file)
        events = parsefile(file)

        for event in events:
            created_event = createEvent(service, event)
            print ('Event created: %s' % (created_event.get('summary')))

if __name__ == '__main__':
    main(sys.argv)

