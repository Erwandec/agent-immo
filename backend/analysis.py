import requests, os, json
OPENAI_API_URL='https://api.openai.com/v1/chat/completions'
api_key=os.getenv('OPENAI_API_KEY')

def analyze_text(text):
    prompt=open('backend/prompts/nlp_prompt.txt').read().replace('{{TEXT}}',text)
    r=requests.post(OPENAI_API_URL,json={'model':'gpt-4o-mini','messages':[{'role':'user','content':prompt}]},headers={'Authorization':f'Bearer {api_key}'})
    return json.loads(r.json()['choices'][0]['message']['content'])

def analyze_photos(photos):
    prompt=open('backend/prompts/vision_prompt.txt').read()
    content=[{'type':'text','text':prompt}]
    for p in photos: content.append({'type':'image_url','image_url':p})
    r=requests.post(OPENAI_API_URL,json={'model':'gpt-4o','messages':[{'role':'user','content':content}]},headers={'Authorization':f'Bearer {api_key}'})
    return json.loads(r.json()['choices'][0]['message']['content'])
