import change_directory as cdir
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from file_handling import determine_data_type

class folder():
      def __init__(self,id,datatype="",mimetype="") -> None:
            self.id=id
            self.file_ids={}
            self.datatype=datatype
            self.mimetype=mimetype
            self.query_response=None
      def search_folder(self):
            q_string="mimeType="+"'"+self.mimetype+"'"+" and "+"'"+self.id+"'"+" in parents"
            response = service.files().list(q=q_string,spaces='drive').execute()
            self.query_response=response
            print(self.query_response)
      def assign_files(self):
            for dictionary in self.query_response["files"]:
                  self.file_ids[dictionary["name"]]=dictionary["id"]
               
class file():
    def __init__(self,id,name) -> None:
      self.name=name
      self.id=id=id


SCOPES = ['https://www.googleapis.com/auth/drive']

def check_if_token_is_valid():
      cdir.chdir_auth()
      if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if not creds.valid:
                  os.remove("token.json")
                  print("token is not valid")
            else:
                  print("token is valid")
def token():
      cdir.chdir_auth()
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
      return creds

def build_service():
      try:
          service = build('drive', 'v3', credentials=creds)
      except HttpError as error:
          # TODO(developer) - Handle errors from drive API.
          print(f'An error occurred: {error}')
      return service


pdf_folder=folder("1fef38fwmg4UYGfcxhMfLB3OldTIkPWDn","pdf",'application/pdf')
txt_folder=folder("1ojawRL5SkCgwc-ZMc2zQUFOh6y4y3TSm","txt",'text/plain')

datatype_folder_dict={"pdf":pdf_folder,"txt":txt_folder}





def upload_drive(name):
    data_type=determine_data_type(name)
    cdir.switch_dir(data_type)
    parent_id=datatype_folder_dict[data_type].id
    mimetype=datatype_folder_dict[data_type].mimetype
    file_metadata = {'name': name,"parents":[parent_id]}
    media = MediaFileUpload(name,mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media).execute()


def update_drive(name,id):
    data_type=determine_data_type(name)
    cdir.switch_dir(data_type)
    parent_id=datatype_folder_dict[data_type].id
    mimetype=datatype_folder_dict[data_type].mimetype
    file_metadata = {'name': name,"parents":[parent_id]}
    media = MediaFileUpload(name,mimetype=mimetype)    
    file = service.files().update(media_body=media,fileId=id).execute()



def complete_upload(directory):
     for file in os.listdir(directory):
            try:
                  id=pc_dir_drive_dict[directory].file_ids[file]
                  update_drive(file,id)
                  print(f"{file} updated")
            except:
                  upload_drive(file)
                
def upload_missing_files(directory):
     for file in os.listdir(directory):
            try:
                  id=pc_dir_drive_dict[directory].file_ids[file]
            except:
                  upload_drive(file)



pdf_dir="C:/Users/lukas/Desktop/bachelor/pdf"
pc_dir_drive_dict={pdf_dir:pdf_folder}

check_if_token_is_valid()
creds=token()
service=build_service()
pdf_folder.search_folder()
pdf_folder.assign_files()
txt_folder.search_folder()
txt_folder.assign_files()
complete_upload(pdf_dir)


#das id dict in die class