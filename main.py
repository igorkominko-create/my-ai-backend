from fastapi import FastAPI, UploadFile, File, HTTPException
import google.generativeai as genai
import os

app = FastAPI()

# Налаштування Gemini (Ваш API ключ буде в змінних оточення на Render)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Читаємо файл
        contents = await file.read()
        
        # Відправляємо в Gemini
        response = model.generate_content([
            {"mime_type": file.content_type, "data": contents},
            "Проаналізуй це зображення і дай відповідь."
        ])
        
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
