#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json
import time
import pickle
import os
import shutil
import skimage as sk
from skimage import io
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from overall import *
import smtplib
import json
import imghdr
from email.message import EmailMessage
from skimage.transform import resize
from sql_functions import *
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

with open('secret.json') as json_file:
    env_variables = json.load(json_file)
    os.environ['EMAIL_ADD'] = env_variables['EMAIL_ADD']
    os.environ['EMAIL_PASS'] = env_variables['EMAIL_PASS']
    os.environ['AZURE'] = env_variables['AZURE']
    os.environ['SQL_HOST'] = env_variables['SQL_HOST']
    os.environ['SQL_USER'] = env_variables['SQL_USER']
    os.environ['SQL_PASS'] = env_variables['SQL_PASS']
    os.environ['SQL_DB'] = env_variables['SQL_DB']
config = {
  'host':os.environ.get('SQL_HOST'),
  'user':os.environ.get('SQL_USER'),
  'password':os.environ.get('SQL_PASS'),
  'database':os.environ.get('SQL_DB')
}

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[4]:


azure_key = os.environ.get('AZURE')
EMAIL_ADD = os.environ.get('EMAIL_ADD')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
blob_service_client = BlobServiceClient.from_connection_string(azure_key)


# In[5]:


def im_resize(fname):
    img = io.imread(fname)
    img = resize(img, (800, 600, 3))
    io.imsave(fname, img)


# In[6]:


containers = blob_service_client.list_containers() 
cs = {}
for c in containers:
    cs[c.name] = c.last_modified
container_name = sorted(cs, key=cs.get, reverse=True)[0]


# In[7]:


def send_email(file_name, obj_name):
    msg = EmailMessage()
    msg['Subject'] = 'Rectify: Item wrongly recycled'
    msg['From'] = EMAIL_ADD
    msg['To'] = 'rectify.hackathon@gmail.com'
    msg.set_content('Oops, you have incorrectly placed an {} into recycling ;)'.format(obj_name))
    
    file = open("status_email.txt","w+") 
    file.write("Rectifying") 
    file.close()

    with open(file_name, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADD, EMAIL_PASS)

        # Args: sender, reciever, message
        smtp.send_message(msg)


# In[8]:


def send_reward():
    msg = EmailMessage()
    msg['Subject'] = 'Rectify Reward: You are a star!'
    msg['From'] = EMAIL_ADD
    msg['To'] = 'rectify.hackathon@gmail.com'
    msg.set_content('You have been recycling correctly for 10 days, keep it up!')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADD, EMAIL_PASS)

        # Args: sender, reciever, message
        smtp.send_message(msg)


# In[9]:


clear_items(1, config)
clear_items(2, config)

set_consecutive_days(1, 9, config)
    
users_to_df(config)


# In[10]:


def check_recycle(objects, fname):
    recycle_dict = ['water_bottle', 'mixing_bowl']
    flag = False
    user = 1
    for obj in objects:
        if obj not in recycle_dict:
            flag = True
        
        add_item(obj, not flag, user, config)
        check_clean(user, 1000, config) 
    reward = False
    if len(objects)!=0:
        reward = check_reward(user, 10, config)
        file = open("status_email.txt","w+") 
        file.write("Reward Sent") 
        file.close()
    if reward == True:
        send_reward()
    if flag:
        print("Non-recyclable object detected! Rectifying...\n\n")
        send_email(fname, objects[0])


# In[11]:


import time
import shutil
from datetime import datetime
image_history = []
obj_list_history = []
SSIM_THRESH = 0.5
pickle.dump([], open( "item_list.pkl", "wb" ) )

while True:
    # get latest date
    container_client = blob_service_client.get_container_client(container_name)
    container_client.list_blobs()
    blobs = []
    for i in container_client.list_blobs():
        blobs.append(i)
    latest_date = sorted([b['last_modified'] for b in blobs])[-1]
    time.sleep(1)
    # new container client
    container_client = blob_service_client.get_container_client(container_name)
    #container_client.list_blobs()
    #blobs = []
    #for i in container_client.list_blobs():
        #blobs.append(i)
    #print("Num blobs: {}".format(len(blobs)))
    file = open("status.txt","w+") 
    file.write("IDLE") 
    file.close()
    
    file = open("status_email.txt","w+") 
    file.write("--") 
    file.close()
    
    for blob in container_client.list_blobs():
        name = blob['name']
        t = blob['last_modified']
        if name not in image_history and t > latest_date:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=name)
            # save current image
            this_name = 'real_time/{}.jpg'.format(int(time.time()))
            with open(this_name, 'wb') as f:
                f.write(blob_client.download_blob().readall())
                
            time.sleep(1)
            if len(os.listdir('real_time'))!=0:
                last_img = sorted(os.listdir('real_time'))[-2]
                if last_img != '.DS_Store':
                    last_img = io.imread('real_time/{}'.format(last_img))
                    current_img_name = sorted(os.listdir('real_time'))[-1]
                    current_img = io.imread('real_time/{}'.format(current_img_name))
                    sim_idx = ssim(last_img, current_img, multichannel=True)
                    
                    print(sim_idx)
                    
                    if sim_idx <= 0.85:
                        
                        file = open("status.txt","w+") 
                        file.write("Inferencing") 
                        file.close() 
                        
                        shutil.rmtree("adian")
                        os.makedirs("adian")
                        print("New event found!!!!")
                        
                        fname = 'real_time/{}'.format(current_img_name)
                        obj_list = get_object_list(fname)
                        
                        file = open("status.txt","w+") 
                        file.write("Done!") 
                        file.close() 
                        
                        new_objs = [i for i in obj_list if i not in obj_list_history]
                        obj_list_history = obj_list_history + new_objs
                        check_recycle(new_objs, fname)
                        pickle.dump(obj_list_history, open("item_list.pkl", "wb" ))
                        
            image_history.append(name)

from overall import *
obj_list = get_object_list('figs/final/bo2.jpg')
#obj_list = get_object_list('image_cut/test.jpg')
# In[12]:


obj_list_history


# In[12]:


new_objs


# In[ ]:




