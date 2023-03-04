import requests
import graphql
import os
from bs4 import BeautifulSoup as bs
import traceback
from fflask import thread
import json

pre_id = ''
id = ''

print('동작 중...')

#로그인

print('\n로그인 중...')
with requests.Session() as s:
    loginPage = s.get('https://playentry.org/signin')
    soup = bs(loginPage.text, 'html.parser')
    csrf = soup.find('meta', {'name': 'csrf-token'})
    login_headers={'CSRF-Token': csrf['content'], "Content-Type": "application/json"}
    req = s.post('https://playentry.org/graphql',     
    headers=login_headers, json={'query':graphql.login, 'variables':{"username":os.environ['id'],"password":os.environ['pass']}})
    print("로그인 완료!\n")
    soup = bs(s.get("https://playentry.org").text, "html.parser")
    xtoken = json.loads(soup.select_one("#__NEXT_DATA__").get_text()
                        )["props"]["initialState"]["common"]["user"]["xToken"]
    headers = {'X-Token': xtoken, 'x-client-type': 'Client', 'CSRF-Token': csrf['content'], "Content-Type": "application/json"}

    def createComment(lid, ccontent):
        global pre_id
        s.post('https://playentry.org/graphql', headers=headers, json={'query':graphql.createComment, "variables":{"content":ccontent,"target":lid,"targetSubject":"discuss","targetType":"individual"}})
        print(f"{lid}, {ccontent}")

    print('동작 중!\n')

#글 읽고 답하기

    while True:
      try:
        req = s.post('https://playentry.org/graphql', headers=headers, json={'query':graphql.loadStory, "variables":{"category":"free","searchType":"scroll","term":"all","discussType":"entrystory","pageParam":{"display":1,"sort":"created"}}})
        story = req.text
        llid = story[story.index('"id"')+6:story.index('"id"')+6+24]
        content = story[story.index('"content"')+11:story.index('"content"')+11+(story.index('"created"')-94)]
        
        if pre_id != llid:
            if content[0]=='!':
                command = content[1:]
                
                # if ~ createComment 부분 복붙해서 명령어 추가
              
                if command == '테스트':
                  createComment(llid, '테스트중')

                pre_id = llid
      except:
        print(traceback.format_exc())
