#importing packages
import json
import io, re
import urllib, urllib.request
import gzip, zipfile 
import pandas as pd
import numpy as np
from collections import defaultdict

link = urllib.request.URLopener()
#retrieving data
link.retrieve("https://pencilapp-dev.s3-us-west-2.amazonaws.com/mldata2020-9-3/users.json.gz", "file.gz")
link.retrieve("https://pencilapp-dev.s3-us-west-2.amazonaws.com/mldata2020-9-3/storytagownerships.json.gz","storytags.gz")
link.retrieve("https://pencilapp-dev.s3-us-west-2.amazonaws.com/mldata2020-9-3/storytags.json.gz","storytags_preprocessed.gz")
link.retrieve("https://pencilapp-dev.s3-us-west-2.amazonaws.com/mldata2020-9-3/stories.json.gz","stories.gz")
link.retrieve("https://pencilapp-dev.s3-us-west-2.amazonaws.com/mldata2020-9-3/storytagownerships.json.gz","story_tag_rel.gz")


def decompress_to_list(file,type="gz"):
  if type == "gz":
    with gzip.GzipFile(str(file), 'r') as fin:   
        json_bytes = fin.read()                      
    json_str = json_bytes.decode('utf-8')            
    data = json.loads(json_str) 
  elif type =="zip":
    with zipfile.ZipFile("likes.zip", "r") as z:
      for filename in z.namelist():    
        with z.open(filename) as f:  
          d = f.read()  
          data = json.loads(d)

  return data    

                    
#userID, tagID, storyID
storytags = decompress_to_list("storytags.gz")
storytags_preprocessed = decompress_to_list("storytags_preprocessed.gz")
#story_id,title,slug,userID,categories,description
story_info = decompress_to_list("stories.gz")
#id,tag_id,story_id
storytagrel = decompress_to_list("story_tag_rel.gz")

story_likes = decompress_to_list("likes.zip","zip")


stories_data = []
for story_id, title, slug, userId, categories, description in story_info:

  cat = ""
  
  for c in categories:
    cat += c+" "
  s = cat
  if title!= None:
    s+= title
  if description != None:
    s+= description  
  stories_data.append(s)

"""tagtostory_map maps tag_id to corresponding story_id"""
tagtostory_map = {}
for id, tag_id, story_id in storytagrel:
  tagtostory_map[tag_id] = story_id

"""ID,string of all tags, searchable tag, isCanonical(not needed)
searchable tag removes spaces, punctuation and combines multiple tags to one"""
storytags_dict = defaultdict(list)
for story in storytags_preprocessed:
  tag_id = story[0]
  if tag_id in tagtostory_map:
    story_id = tagtostory_map[tag_id]
    s = re.sub(r'[^\w\s]','',story[1])
    tags = s.split()
    for tag in tags:
    #find corresponding story_id
      storytags_dict[tag].append(story_id)


storylikes_dict = defaultdict(int)
for user_id, story_id in story_likes:
    storylikes_dict[story_id] += 1  

story_content = defaultdict(list)
for story_id, title, slug, userId, categories, description in story_info:
  if story_id in storylikes_dict:
    likes = storylikes_dict[story_id]
  else:
    likes = 0
  story_content[story_id].append([likes,[title,slug,userId,categories,description]])
  