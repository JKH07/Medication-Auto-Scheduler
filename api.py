from fastapi import FastAPI, HTTPException, Header, Body
import os
import uvicorn
from main import main
from workflow.save_to_data_base import update_medication_schedule
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your local Flutter web app to talk to the server
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, etc.
    allow_headers=["*"],  # Allows all headers
)
@app.post("/process-text")
async def receive_text(
    day: str = Body(..., media_type="text/plain"), 
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ")[1]
    
    try:
        result = main(token, day)
        print(f"main() returned: {result}")        
        print(f"result type: {type(result)}")      
        update_medication_schedule(result, day, token)
    except Exception as e:
        import traceback
        traceback.print_exc()                      
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Word processed",
        "day": day,
        "status": "success"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)