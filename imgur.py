import asyncio
from aiohttp import ClientSession
#import requests

IMGUR_URL = 'https://api.imgur.com/3/image'
payload = {'image': 'https://cdn.discordapp.com/attachments/453093998404567040/459599556477321219/2WYMtKn.png'} #image can be binary data or url
headers = {
          'Authorization': 'Client-ID 7a5b765577a8b34'
          }

async def add_to_album(imageDeleteHashes,albumDeleteHash,clientID):
    payload = {'deletehashes': imageDeleteHashes}
    headers = { 'Authorization': 'Client-ID ' + clientID }
    async with ClientSession(raise_for_status=True) as session:
        async with session.post(url=f"https://api.imgur.com/3/album/{albumDeleteHash}/add",data = payload,headers = headers) as response:
            respDic = await response.json()
            if respDic['success']:
                return respDic
            else:
                #print('blah: ' + respDic['data']['error'])
                return respDic['data']['error']

async def image_upload(imageData,clientID):
    #imageData is either a B64 or url
    imageData = imageData.strip()
    payload = {'image': imageData}
    headers = { 'Authorization': 'Client-ID ' + clientID }
    async with ClientSession(raise_for_status=True) as session:
        async with session.post(url='https://api.imgur.com/3/image',data = payload,headers = headers) as response:
            respDic = await response.json()
            if respDic['success']:
                return respDic
            else:
                #print('blah: ' + respDic['data']['error'])
                return respDic['data']['error']

async def image_get(imageID,header):
    async with ClientSession(raise_for_status=True) as session:
        async with session.get(url='https://api.imgur.com/3/image/'+imageID,data = {},headers = headers) as response:
            respDic = await response.json()
            if respDic['success']:
                return respDic
            else:
                #print('blah: ' + respDic['data']['error'])
                return respDic['data']['error']

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(image_get('r9OxkBE'))

    #files = {}
    #response = requests.request('POST', url, headers = headers, data = payload, files = files, allow_redirects=False, timeout=10)
    #print(type(response.text))
    #print(response.text)
