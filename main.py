import asyncio
import os
import re
import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
from guild import *
import server
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

intents = discord.Intents.default()
client = discord.Client(intents=intents)

GUILD_ID=1122707918177960047
RESULT=None
THREADS=[]
TIMERAND=None
STEP=111510
TOKEN=None
@client.event
async def on_ready():
    global RESULT,THREADS,TIMERAND
    try:
        req=requests.get('http://localhost:8888')
        print(req.status_code)
        await client.close() 
        print('Client closed')
        exit()
    except:
        server.b()
        guild=client.get_guild(GUILD_ID)
        RESULT=await getBasic(guild)
        if not getToken.is_running():
            getToken.start()
        if not fetchData.is_running():
            fetchData.start()
        '''await asyncio.sleep(60)
        if not updateData.is_running():
            updateData.start(guild)'''
@tasks.loop(seconds=60)
async def getToken():
    global TOKEN,RESULT
    try:
        print('getToken is running')
        url='https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal'
        headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
        }
        data={
            "app_id": "cli_a6a20c5f68b8d010",
            "app_secret": "72ULXn53ZAUVr1Vme6aNkhzQf2DDaLSd"
        }
        req=requests.post(url,headers=headers,json=data)
        if req.status_code<400:
            js=req.json()
            TOKEN={
                'token':js['tenant_access_token'],
                'expire':js['expire']
            }
            print(TOKEN)
    except Exception as err:
        await RESULT['logsCh'].send(err)
        pass
        
@tasks.loop(seconds=.1)
async def fetchData():
    global STEP,TOKEN,RESULT
    try:
        if int(str(round(datetime.now().timestamp())).split(',')[0])%10==0:
            await RESULT['logsCh'].send(STEP)
        done=False
        print('fetchData is running')
        print(STEP)
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.9',
            }
        url=f'https://main.v2.beatstars.com/musician?id={STEP}&fields=profile,user_contents,stats,bulk_deals,social_networks,email'
        try:
            req=requests.get(url,headers=headers)
        except Exception as err:
            await RESULT['logsCh'].send(err)
            pass
        data=req.json()
        print(data)
        if data['response']['type']=='success':
            data=data['response']['data']
            url='https://open.larksuite.com/open-apis/sheets/v2/spreadsheets/ObB8syGTHhzLpjtkIuvlL893gcf/values_append'
            headers={
                'authorization':'Bearer '+TOKEN['token']
            }
            raw=[
                data['profile']['user_id'],
                data['email'],
                data['profile']['first_name'],
                data['profile']['last_name'],
                data['profile']['display_name'],
                data['profile']['avatar']['original'] if data['profile']['avatar'] else None,
                data['profile']['location'],
                data['profile']['permalink'],
                data['profile']['relative_uri'],
                data['profile']['beatstars_uri'],
                data['profile']['propage_uri'],
                data['profile']['user_type'],
                data['profile']['subscription_id'],
                data['profile']['subscription_type'],
                str(data['profile']['verified']),
                data['profile']['biography'],
                data['profile']['biography_summary'],
                data['stats']['followers'],
                data['stats']['plays'],
                data['stats']['tracks'],
                data['stats']['following']
            ]
            if data['social_networks']:
                for item in data['social_networks']:
                    raw.append(item['uri'])
            data={
                "valueRange": {
                    "range": "V5HL6x",
                    "values": [
                        raw
                    ]
                }
            }
            try:
                req=requests.post(url,headers=headers,json=data)
            except Exception as err:
                await RESULT['logsCh'].send(err)
                pass
            if(req.status_code<400):
                print('Created new record success')
                STEP+=1
                done=True
        if done==False and 'musician not found' in data['response']['data']['message'].lower():
            STEP+=1
    except Exception as err:
        await RESULT['logsCh'].send(err)
        pass
client.run(os.environ.get('t'))

