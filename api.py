
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import uvicorn
from main import main
app = FastAPI()

@app.post("/upload-image")
async def schedule(user_id):


    #scheduling
    main(user_id)

    return {
        "message": "Scheduling in process"
    }

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)