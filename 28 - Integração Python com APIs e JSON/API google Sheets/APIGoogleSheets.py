#!/usr/bin/env python
# coding: utf-8

# In[16]:


from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1c03q-w3ydDjY7Gy3lJPzho69d2LYq8z7GhpE4aCp33U'
SAMPLE_RANGE_NAME = 'Página1!A1:C14'


def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Ler informacoes do Google Sheets
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        valores = result['values']
        print(valores)
        
        valores_adicionar = [
            ["Imposto"],
        ]
        
        for i, linha in enumerate(valores):
            if i > 0:
                vendas = linha[1]
                vendas = vendas.replace("R$ ", "").replace(".", "")
                vendas = float(vendas.replace(",", "."))
                imposto = vendas * 0.1
                imposto = f'R$ {imposto}'.replace(".", ",")
                valores_adicionar.append([imposto])
        
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="C1", valueInputOption="USER_ENTERED",
                              body={'values': valores_adicionar}).execute()
        # adicionar/editar uma informação
        
#         valores_adicionar = [
#             ["dezembro", 'R$ 127.300,15'],
#             ["janeiro", "R$ 100.000,00"],
#         ]
        
#         result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                     range="A13", valueInputOption="USER_ENTERED",
#                                       body={'values': valores_adicionar}).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()


# In[ ]:




