#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pickle
import os
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import webbrowser

path = '../test_location'
path2 = path.replace('/','\\')
print(path2)

def docs_create(title):
    print'st'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print 'sth'
    service = build('docs', 'v1', credentials=creds)

    body = {
        'title': title
    }
    doc = service.documents().create(body=body).execute()
    docID = doc.get('documentId')
    return docID
    #webbrowser.open('https://docs.google.com/document/d/'+docID+'/edit')
    # Retrieve the documents contents from the Docs service.
    #document = service.documents().get(documentId=DOCUMENT_ID).execute()

#docs_create('test doc')

def abs_name(file_name):
    return ".".join(file_name.split(".")[:-1])


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_name = event.src_path[len(path)+1:]
        pure_name = ".".join(file_name.split(".")[:-1])
        os.chdir(path2)
        new_name=pure_name
        while 1:
            try:
                os.rename(file_name,new_name+'.html')
            except WindowsError as we:
                if we.winerror == 183:
                    new_name += '(1)'
                    print(new_name)
            else:
                break
        print(path2 + new_name+'.html')
        file = open(path2 + '\\' + new_name + '.html', 'w')
        temphtml="""<h1>Sorry, the file isn't on google yet, try to open it again later</h1>"""
        file.write(temphtml)
        file.close()
        os.chdir(sys.path[0])
        ID = docs_create(new_name)
        url = '\'https://docs.google.com/document/d/' + ID + '/edit\''
        temp = '''<script language="javascript" type="text/javascript"> window.location.href=''' + url + ''';</script>'''
        file = open(path2+'\\' + new_name+'.html', 'w')
        print(temp)
        file.write(temp)
        file.close()

    def on_moved(self, event):
        print(event.event_type, event.src_path,event.dest_path)
        src_end = event.src_path.split('.')[-1]
        dest_end =event.dest_path.split('.')[-1]
        src_file_name = event.src_path[len(path) + 1:]
        dest_file_name = event.dest_path[len(path) + 1:]
        print(dest_end,dest_file_name)
        if src_end == 'html' and dest_end != 'html':
            time.sleep(1)
            os.chdir(path2)
            os.rename(dest_file_name,src_file_name)
            print('done')

    def on_any_event(self, event):
        print(event.event_type, event.src_path)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()