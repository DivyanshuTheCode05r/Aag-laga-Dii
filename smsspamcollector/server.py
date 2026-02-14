# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import os
import uvicorn

class SMSInput(BaseModel):
    text: str

app = FastAPI(title="SMS Spam Detector")

MODEL_PATH = "sms_spam_model.joblib"
model = None

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        print(f"❌ ERROR: Model file '{MODEL_PATH}' not found!")
        return
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>SMS Spam Detector</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', system-ui, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 14px;
            }
            textarea {
                width: 100%;
                height: 150px;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                font-size: 15px;
                font-family: inherit;
                resize: vertical;
                transition: border-color 0.3s;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                margin-top: 15px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .result {
                margin-top: 25px;
                padding: 20px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: 600;
                text-align: center;
                display: none;
                animation: slideIn 0.3s ease;
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .spam {
                background: #fee;
                color: #c00;
                border: 2px solid #fcc;
            }
            .ham {
                background: #efe;
                color: #0a0;
                border: 2px solid #cfc;
            }
            .loading {
                background: #f0f0f0;
                color: #666;
                border: 2px solid #ddd;
            }
            .confidence {
                font-size: 14px;
                margin-top: 8px;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 SMS Spam Detector</h1>
            <p class="subtitle">Enter any SMS text to check if it's spam or legitimate</p>
            <textarea id="msg" placeholder="Type SMS message here...
Example: Congratulations! You won a lottery..."></textarea>
            <button id="btn">🔍 Check Message</button>
            <div id="out" class="result"></div>
        </div>

        <script>
            const btn = document.getElementById('btn');
            const out = document.getElementById('out');
            const msgBox = document.getElementById('msg');
            
            btn.onclick = async () => {
                const text = msgBox.value.trim();
                
                if(!text) {
                    out.className = 'result loading';
                    out.style.display = 'block';
                    out.innerHTML = '⚠️ Please enter some text';
                    return;
                }
                
                out.className = 'result loading';
                out.style.display = 'block';
                out.innerHTML = '⏳ Analyzing message...';
                btn.disabled = true;
                
                try {
                    const r = await fetch('/predict', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text})
                    });
                    
                    if(!r.ok) throw new Error('Prediction failed');
                    
                    const data = await r.json();
                    const isSpam = data.label === 'spam' || data.label === 'SPAM';
                    const className = isSpam ? 'spam' : 'ham';
                    const emoji = isSpam ? '🚫' : '✅';
                    const labelText = isSpam ? 'SPAM DETECTED' : 'SAFE MESSAGE';
                    const conf = data.confidence 
                        ? `<div class="confidence">Confidence: ${(data.confidence*100).toFixed(1)}%</div>` 
                        : '';
                    
                    out.className = 'result ' + className;
                    out.innerHTML = `${emoji} ${labelText}${conf}`;
                    
                } catch(e) {
                    out.className = 'result loading';
                    out.innerHTML = '❌ Error: ' + e.message;
                } finally {
                    btn.disabled = false;
                }
            };
            
            // Allow Enter key to submit
            msgBox.addEventListener('keydown', (e) => {
                if(e.ctrlKey && e.key === 'Enter') {
                    btn.click();
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/predict")
def predict(item: SMSInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    text = item.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        pred = model.predict([text])[0]
        
        if pred == 1 or str(pred).lower() == "spam":
            label = "spam"
        else:
            label = "ham"
        
        confidence = None
        try:
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba([text])[0]
                confidence = float(max(proba))
        except:
            pass
        
        return {"label": label, "confidence": confidence}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("\n🚀 Starting SMS Spam Detector Server...")
    print("📍 Open in browser: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
