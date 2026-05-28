from fastapi import FastAPI, HTTPException, Header, Body
import os
import uvicorn
from main import main
from workflow.save_to_data_base import update_medication_schedule

app = FastAPI()

@app.post("/process-text")
async def receive_text(
    day: str = Body(..., media_type="text/plain"), 
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ")[1]
    
    try:
        result = main( token,day)
        update_medication_schedule(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Word processed",
        "day": day,
        "status": "success"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)