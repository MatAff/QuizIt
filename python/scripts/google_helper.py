#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# required installation:
# google-api-python-client
# google-auth-httplib2
# google-auth-oauthlib

import pickle
import os.path
import string
import pandas as pd

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class Google(object):


    def __init__(self, file_creds, file_token):
        self.service = Google.get_service(file_creds, file_token)


    def get_creds(file_creds, file_token):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists(file_token):
            with open(file_token, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(file_creds, 
                                                                 SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(file_token, 'wb') as token:
                pickle.dump(creds, token)
        return creds


    def get_service(file_creds, file_token):
        creds = Google.get_creds(file_creds, file_token)
        service = build('sheets', 'v4', credentials=creds)
        return service


    def sheet_content(self, sheet_id, sheet_name, nr_cols):
        range_text = sheet_name + '!A1:' + string.ascii_uppercase[nr_cols - 1]
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=range_text).execute()
        values = result.get('values', [])
        df = pd.DataFrame(values)
        df.columns = df.iloc[0,:]
        df = df.drop(0)
        return df
