from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# calendar id
CALENDAR_ID = '[[CALENDAR_ID]]'

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = 'client_secrets.json'

# This access scope grants read-only access to the authenticated user's Drive
# account.
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def getEvent( link, summary, location, description, organizer_displayname, start, end, icaluid, timeZone ):
    event = {
        'htmlLink': link,
        'summary': summary,
        'location': location,
        'description': description,
        'organizer': {
            'displayName': organizer_displayname
        },
        'start': {
            'dateTime': start,
            'timeZone': timeZone
        },
        'end': {
            'dateTime': end,
            'timeZone': timeZone #always the same
        },
        'iCalUID': icaluid
    }
    return event

def createEvent(service, event):
    return service.events().import_(calendarId=CALENDAR_ID,body=event).execute()