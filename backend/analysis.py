import requests 
import os 
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
api_key = os.getenv("OPENAI_API_KEY")


def analyze_text(text):
    prompt_path = os.path.join(BASE_DIR, "prompts", "nlp_prompt.txt") 
    
    with open(prompt_path, "r", encoding="utf-8") as f: 
        prompt = f.read().replace("{{TEXT}}", text) 
        
        response = requests.post( 
            OPENAI_API_URL, 
            json={ 
                "model": "gpt-4o-mini",
                "messages": [ 
                    {"role": "user", "content": [{"type":"text","text":prompt}]}
                ] 
            },
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        data = response.json() 
        
        if "choices" not in data:
            print("🔥 DEBUG OPENAI TEXT ERROR:", data) 
            raise Exception("OpenAI returned an error for analyze_text") 
            
            return json.loads(data["choices"][0]["message"]["content"]) 
            
            
def analyze_photos(photos):
    prompt_path = os.path.join(BASE_DIR, "prompts", "vision_prompt.txt")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read() 

        # ✅ Format correct demandé par OpenAI (avril 2026)
        content = [{"type": "text", "text": prompt}] 
        
        for url in photos:
            content.append({ 
                "type": "image_url",
                "image_url": {
                    "url": url
                } 
            }) 
            
            response = requests.post(
                OPENAI_API_URL,
                json={ 
                    "model": "gpt-4o", 
                    "messages": [ 
                        {"role": "user", "content": content} 
                    ]
                },
                headers={"Authorization": f"Bearer {api_key}"} 
            )
            
            data = response.json() 
            
            if "choices" not in data:
                print("🔥 DEBUG OPENAI VISION ERROR:", data) 
                raise Exception("OpenAI returned an error for analyze_photos")
                
                return json.loads(data["choices"][0]["message"]["content"])
