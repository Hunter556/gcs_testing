from os import name
from google.cloud import storage
from google.oauth2 import service_account
import io
import cv2
import numpy as np
import time

def load_files_into_ram():

    #change json service account with your proper json
    keypath = 'your_service_account_file_name.json'
    credentials = service_account.Credentials.from_service_account_file(
        keypath, scopes=["https://www.googleapis.com/auth/cloud-platform"])

    client = storage.Client(credentials=credentials)

    #create a bytesIO buffer object
    buffer = io.BytesIO()
    #get the bucket
    bucket = client.get_bucket('bucket_name')
    #get list of blobs (list of images)
    blobs = bucket.list_blobs(prefix="folder")
    i = 0
    for idx, bl in enumerate(blobs):
        if idx == 0:
            continue
        if i == 10:
            #read only 10 images
            break
        #download file directly to RAM
        bl.download_to_file(buffer)
        #When you write to the buffer, the pointer goes to the end
        #That's why you need to reset it
        buffer.seek(0)
        #Convert bytes into a numpy array
        image = np.asarray(bytearray(buffer.read()), dtype="uint8")
        #Decode numpy array of bytes into an image
        #Equivalant to cv2.imread(path_to_local_file)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        i += 1
if name == "__main__":
    start_time = time.time()
    load_files_into_ram()
    print("--- %s seconds ---" % (time.time() - start_time))




