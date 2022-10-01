import os
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('auto_delete.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

SCOPES = 'https://mail.google.com/'  # read-write mode

SERVICE = None

def init(user_id='me', token_file='token.json', credentials_file='credentials.json'):

    global SERVICE

    if not os.path.exists(credentials_file):
        raise AutoDeleteException('Can\'t find credentials file at %s. You can download this file from https://developers.google.com/gmail/api/quickstart/python and clicking "Enable the Gmail API"' % (os.path.abspath(credentials_file)))

    store = file.Storage(token_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials_file, SCOPES)
        creds = tools.run_flow(flow, store)
    SERVICE = build('gmail', 'v1', http=creds.authorize(Http()))


class AutoDeleteException(Exception):
    pass

if __name__ == '__main__':
    init()
def search(query, user_id='me'):

    if SERVICE is None:
        init()

{'id': '15573cf1adfassafas', 'threadId': '15573cf1adfassafas'}

    try:
        response = SERVICE.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = SERVICE.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages

    except errors.HttpError as e:
        logger.exception(f'An error occurred:{e}')
def delete_messages(query, user_id='me'):
    messages = search(query)
    if messages:
        for message in messages:
            SERVICE.users().messages().delete(userId=user_id, id=message['id']).execute()
            logger.info(f'Message with id: {message["id"]} deleted successfully.')
    else:
        logger.info("There was no message matching the query.")
if __name__ == '__main__':
    logger.info("Deleting messages from abc@gmail.com.")
    delete_messages('from:abc@gmail.com\
            subject:"Go Shopping"\
            older_than:1d'
                    )
