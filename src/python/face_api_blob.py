#impor Azure
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

#import Others
import cv2
import csv
from time import sleep
import json
import requests
import ast
from ftplib import FTP
#blob設定
account_name = 'storageaccounttest91a3'
account_key = 'QCxTMQ8IEprjrU4XCRzxodEWh7o8QiXc3CPULJJexS3sMbhtC0rK7XmtMJJeHSIFTSOb6mpmAgrYc53akPjMVA=='
container_name1 = 'climbanother'
container_name2 = 'climbanother-results'
file_name = {'img_1':'img_origin.png','img_2':'img_rectangle.png','data':'face_data.json','cnt':'count.json'}

#webカメラ設定
web_camera = 1
INTERVAL = 3
font = cv2.FONT_HERSHEY_TRIPLEX

# Face API 設定
KEY = '16e5282de5c44319bfd3823c684d848c'
ENDPOINT = 'https://mthouse.cognitiveservices.azure.com/'
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


#リクエスト設定
request_url = 'https://mthouse.cognitiveservices.azure.com/face/v1.0/detect'
hedder = {
'Content-Type': 'application/octet-stream',
'Ocp-Apim-Subscription-Key': KEY,
}
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

#長方形情報取得
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    right = left + rect['width']
    bottom = top + rect['height']
    
    return (left, top), (right, bottom) ,(left,bottom+25),(left,bottom+50)


#blob upload
def upload_blob(filename,container,pngflag=True):
    service = BlockBlobService(account_name=account_name,account_key=account_key)
    if pngflag:
        service.create_blob_from_path(container,filename, filename, content_settings=ContentSettings(content_type="image/png"))
    else:
        service.create_blob_from_path(container,filename, filename, content_settings=ContentSettings(content_type="application/json"))


#映像キャプチャ
cap = cv2.VideoCapture(web_camera)

flag=True
while(flag):

    _, frame = cap.read()
    cv2img = cv2.flip(frame, 1)

    #画像一時保存
    cv2.imwrite(file_name['img_1'],cv2img)
    img = open(file_name['img_1'],'rb')

    #画像分析
    response = requests.post(request_url,params=params,headers=hedder,data=img)
    if len(response.json())!=0:
        flag = False
    sleep(INTERVAL)

json_data = response.json()
#画像情報付与
for i in json_data:
    x,y,t1,t2= getRectangle(i)
    cv2img_2 = cv2.rectangle(cv2img,x,y,(0,0,255),2)
    age = int(i['faceAttributes']['age'])
    gender = i['faceAttributes']['gender']
    cv2.putText(cv2img,f'age:{age}',t1,font,fontScale = 1,thickness=1,color = (0,0,0),lineType= cv2.LINE_AA)
    cv2.putText(cv2img,f'gender:{gender}',t2,font,fontScale = 1,thickness=1,color = (0,0,0),lineType= cv2.LINE_AA)
    #画像一時保存
    cv2.imwrite(file_name['img_2'],cv2img_2)
    img = open(file_name['img_2'],'rb')

#ファイル作成
with open(file_name['data'],'w')as f:
    f.write(json.dumps(json_data,indent=4))
with open(file_name['cnt'],'w')as f:
    f.write(str(len(json_data)))

#Blobにアップロード
upload_blob(file_name['data'],container_name2,pngflag=False)
upload_blob(file_name['img_2'],container_name1)
upload_blob(file_name['cnt'],container_name2,pngflag=False)
#upload_blob(file_name['img_2'])

#ftp接続
# ftp = FTP(
#     '52.191.169.175',
#     'ftp_user',
#     passwd='0000'
# )

# with open(file_name['data'],'rb') as f:
#     ftp.storlines('STOR /'+file_name['data'],f)
# with open(file_name['img_1'],'rb') as f:
#     ftp.storbinary('STOR /'+file_name['img_1'],f) 
# with open(file_name['img_2'],'rb') as f:
#     ftp.storbinary('STOR /'+file_name['img_2'],f)
# ftp.quit()
 