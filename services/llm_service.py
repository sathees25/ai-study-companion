from openai import OpenAI
from congif import OPENROUTER_API_KEY,MODEL,BASE_URL

client = OpenAI(
    api_key= OPENROUTER_API_KEY,
    base_url=BASE_URL

)

def get_response(prompt: str):

    messages =[{"role": "system", "content": "You are a helpful AI tutor. Always explain step-by-step, simple, with examples."},
                {"role": "system", "content": prompt}]
    
    try:
        respone = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            
        )

        print("Full Response:",respone)

        if respone and respone.choices:
            return respone.choices[0].message.content
        else:
            return "No response from model"
    
    except Exception as e:
        print("Error",e)
        return f"Error: {str(e)}"