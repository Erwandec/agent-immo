import requests
import os
import json

# ✅ BASE_DIR : chemin réel du dossier /backend/ (correct sur Render et en local)
BASE_DIR =os.path.dirname(os.path.abspath(__file__)) 

OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
api_key =os.getenv('OPENAI_API_KEY') 


def analyze_text(text):
    """ 
    Analyse le texte de l'annonce. 
    Charge correctement le prompt depuis backend/prompts/
    """ 
# ✅ Chemin absolu correct du fichier nlp_prompt.txt
    prompt_path = os.path.join(BASE_DIR, "prompts", "nlp_prompt.txt")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read().replace("{{TEXT}}", text) 
        
        response = requests.post(
            OPENAI_API_URL,
            json={
                'model': 'gpt-4o-mini',
                'messages': [
                    {'role': 'user', 'content': prompt}
                ]
            },
            headers={'Authorization': f'Bearer {api_key}'}
        ) 
        
        return json.loads(response.json()['choices'][0]['message']['content'])
        
        
def analyze_photos(photos): 
            """
            Analyse les photos de l'annonce. 
            Charge correctement le prompt depuis backend/prompts/ 
            """
# ✅ Chemin absolu correct du fichier vision_prompt.txt
            prompt_path = os.path.join(BASE_DIR, "prompts", "vision_prompt.txt") 
            
            with open(prompt_path, "r", encoding="utf-8") as f: 
                prompt = f.read()

                # ✅ Construction du payload avec texte + images 
                content = [{'type': 'text', 'text': prompt}]
                for p in photos:
                    content.append({'type': 'image_url', 'image_url': p}) 
                    
                    response = requests.post(
                        OPENAI_API_URL, 
                        json={ 
                            'model': 'gpt-4o',
                            'messages': [ 
                                {'role': 'user', 'content': content} 
                            ]
                        },
                        headers={'Authorization': f'Bearer {api_key}'} 
                    )
                    
                    return json.loads(response.json()['choices'][0]['message']['content'])
