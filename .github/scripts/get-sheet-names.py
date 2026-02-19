#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Получить названия листов из всех Google Sheets
"""

import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SHEETS = [
    ("1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU", "Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ"),
    ("1iHcpofQz8WjyPnYlAZOl6RKrh4MQze1T20d3npXMdJg", "Калькулятор подсчета приготовленных продуктов"),
    ("1JLmJ7KuSdj2reJlasvtFQekKrPb8-7yKZkPUEOMWFvE", "Список продуктов учет"),
]

def get_credentials():
    creds = None
    token_path = Path(__file__).parent / 'token.pickle'

    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = Path(__file__).parent / 'credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_sheet_names(service, sheet_id):
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        return [sheet['properties']['title'] for sheet in sheets]
    except Exception as e:
        return [f"ERROR: {e}"]

creds = get_credentials()
service = build('sheets', 'v4', credentials=creds)

print("Названия листов в таблицах:\n")
for sheet_id, name in SHEETS:
    print(f"📊 {name}")
    sheet_names = get_sheet_names(service, sheet_id)
    for sname in sheet_names:
        print(f"   - {sname}")
    print()
