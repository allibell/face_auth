# -*- coding: utf-8 -*-
import uuid
import os
import shutil

# PATHS ARE BASED ON ROOT FACE_AUTH DIR, WHICH IS STUPID

def new_user(name, image_path) :
    new_id = str(uuid.uuid4())
    dir_name = "users/users/" + new_id
    print(dir_name)
    os.mkdir(dir_name)
    print("Directory " + dir_name + "/ created.")
    
    name_file = open(dir_name + "/name.txt", "w")
    name_file.write(name)
    name_file.close()
    
    if (os.path.isdir(image_path)) :
        src_files = os.listdir(image_path)
        for file_name in src_files:
            full_file_name = os.path.join(image_path, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dir_name)
    
    elif (os.path.isfile(image_path)) :
        shutil.copy(image_path, dir_name)
        
        
def get_id_from_name(name) :
    users = os.listdir("users/users")
    for uid in users :
        name_file = open("users/users/" + uid + "/name.txt", "r")
        if (name in name_file.read()) :
            return uid
    return "INVALID"

# get all pictures
def get_pictures_from_id(uid) :
    files = os.listdir("users/users/" + uid)
    image_files = set(files) - set(["name.txt"])
    return ["users/users/" + uid + "/" + x for x in image_files]
    

# get one picture
def get_picture_from_id(uid) :
    files = os.listdir("users/users/" + uid)
    image_files = set(files) - set(["name.txt"])
    return "users/users/" + uid + "/" + next(iter(image_files))

def get_name_from_id(uid) :
    return open("users/users/" + uid + "/name.txt").read()

def get_all_users() :
    return os.listdir("users/users/")
        
    
    