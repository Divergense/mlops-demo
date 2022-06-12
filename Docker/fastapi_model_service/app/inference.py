import os
import sys
import pandas as pd

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException

from app.model import Model


load_dotenv()
mlflow_endpoint = os.getenv("MLFLOW_S3_ENDPOINT_URL")
if mlflow_endpoint is not None:
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = mlflow_endpoint
else:
    print('Variable "MLFLOW_S3_ENDPOINT_URL" is not set. Exit...')
    sys.exit(1)

MODEL_NAME = os.getenv("SERVICE_MODEL_NAME")
MODEL_STAGE = os.getenv("MODEL_STAGE")


app = FastAPI()
model = Model(MODEL_NAME, MODEL_STAGE)


@app.post("/invocations")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        with open(file.filename, "wb") as f:
            f.write(file.file.read())

        data = pd.read_csv(file.filename)
        os.remove(file.filename)
        return list(model.predict(data))
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file extension. Only csv supported."
        )


if os.getenv("AWS_ACCESS_KEY_ID") is None or os.getenv("AWS_SECRET_ACCESS_KEY") is None:
    print(
        "Environment variables is not set. Check 'AWS_ACCESS_KEY_ID' and"
        " 'AWS_SECRET_ACCESS_KEY'"
    )
    sys.exit(1)
