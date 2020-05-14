import requests as r
import pandas as pd
import numpy as np
import time
import csv
import json
import matplotlib.pyplot as plt
from datetime import datetime,date
import plotly as py
from pprint import pprint
import re
import scipy
import scipy.stats
from PyQt5 import QtWidgets

TOKEN_VK = '23acc95023acc95023acc9504023c092a1223ac23acc9507ef4dc240205bcafea27244d' #vk service token
version = 5.101
def get_members(group_id):
    try_count = 0
    while (try_count<2):
        try:
            response = r.get('https://api.vk.com/method/groups.getById',
                 params={
                     'v' : version ,
                     'access_token' : TOKEN_VK,
                     'group_ids' : group_id,
                     'fields' : 'members_count'
            })
            return response.json()['response'][0]['members_count']
        except:
            try_count +=1;
        time.sleep(0.06)

def cleanText(raw_text):
	cleanr=re.compile('<.*?>|(\[.*?\|)|\]')
	cleantext = re.sub(cleanr,'',raw_text)
	return cleantext

def load_from_vk(group_id,date_from,date_to):
    print(group_id,date_from,date_to)
    likes_list,posts_list,members_list, views_list,err_list = ([] for i in range(5));
    
    headers = ['group name','post date','post link', 'text', 'views','likes','reposts','comments']
    all_posts_period = pd.DataFrame(columns=headers)
    posts_in_group = [];
    offset = 0;
    members = get_members(group_id)

    date_ok = True;
    last_try = 0;
    #Выгружаем посты на стенке, пока не выйдем за "левую" дату

    while (date_ok or last_try <=1):
        res = r.get('https://api.vk.com/method/wall.get',
             params={
                 'v' : version,
                 'access_token' : TOKEN_VK,
                 'domain' : group_id,
                 'offset' : offset,
                 'count': '100',
                 'extended':'1',
                 'fields':'name'
             })
        try:
            response = res.json()['response']
        except:
            date_ok = False;
            last_try = 2;
            continue;

        if (response['count']==0): #если в выгрузке пусто, переходим к следующей группе
            date_ok = False;
            last_try = 2;
            continue;

        #считаем посты удовлетворяющие условию по датам  
        all_posts = response['items']
        group_name = response['groups'][0]['name']
        if all(datetime.fromtimestamp(post['date']).date() < date_from 
              for post in all_posts):
            date_ok = False
            last_try += 1;
        else:
            for post in all_posts:
                post_info = []
                post_date = datetime.fromtimestamp(post['date'])
                if (post_date.date() > date_from and post_date.date() < date_to):
                    
                    post_link='https://vk.com/wall'+str(post['owner_id'])+'_'+str(post['id'])
                    post_text = cleanText(post['text'])
                    try:
                        # post_ERR = round(post['views']['count']/ members * 100,2)
                        post_info.append((group_name,post_date,post_link,post_text,
                                      post['views']['count'],post['likes']['count'],post['reposts']['count'],post['comments']['count']));
                    except:
                        post_info.append((group_name,post_date,post_link,post_text,
                                      0,post['likes']['count'],post['reposts']['count'],post['comments']['count']));
                    posts_in_group.extend(post_info)
            offset += len(all_posts)
        time.sleep(0.06)

    # members_list.append(members)
    # likes_list.append(like_counter)

    posts_data = pd.DataFrame(posts_in_group, columns=headers)
    mean_ = int(posts_data.groupby(posts_data ['post date'].dt.to_period('d')).mean()['views'].mean())
    std_ = int(posts_data.groupby(posts_data['post date'].dt.to_period('d')).std()['views'].mean())
    def three_sigma_anomaly(views):
        ano_cut_off = 3*std_
        upper_cut = mean_ + ano_cut_off
        return(views>upper_cut)

    anomalies = posts_data.views.apply(three_sigma_anomaly)
    posts_data['is_nomaly'] = anomalies

          



    # all_posts_period = pd.concat([all_posts_period,posts_data],sort=False)
    # posts_data.sort_values(['views'], axis=0, ascending=False, inplace=True)
    # for i in range(3):
    #     try:
    #         top_viewed_posts = top_viewed_posts.append(posts_data.iloc[[i]])
    #     except:
    #         continue

    
    # df=df.join(pd.DataFrame(
    # {
    #     'vk members' : members_list,
    #     'vk posts' : posts_list,
    #     'vk likes' : likes_list,
    #     'vk avg views' : views_list,
    #     'vk avg err' : err_list
    # }, index=df.index )) 
    # new_order = [0,1,4,5,6,7,8,2,3]
    # df = df[df.columns[new_order]]
    # posts_in_group.to_excel('posts_in_group.xlsx', encoding='utf-8',engine='xlsxwriter')
    return posts_data