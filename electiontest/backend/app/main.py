from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import os
import shutil

from backend.app.model import train_and_predict
from backend.app.pm_logic import predict_pm
from backend.app.chart_generator import generate_charts
from backend.app.shap_report import generate_shap
from backend.app.pdf_report import generate_pdf

app = FastAPI(title="Election AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = "backend/app"
TEMP_DIR = f"{BASE_DIR}/temp_data"
REPORT_DIR = f"{BASE_DIR}/reports"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ✅ ROOT ENDPOINT (THIS FIXES THE 404 YOU SAW)
@app.get("/")
def root():
    return {
        "status": "Election AI backend is running",
        "docs": "/docs",
        "predict": "/predict"
    }

@app.post("/upload/elections")
async def upload_elections(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        df.to_csv(f"{TEMP_DIR}/elections.csv", index=False)
        return {"status": "elections uploaded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload/social")
async def upload_social(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        df.to_csv(f"{TEMP_DIR}/social.csv", index=False)
        return {"status": "social uploaded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/predict")
def predict():
    elections_path = f"{TEMP_DIR}/elections.csv"
    social_path = f"{TEMP_DIR}/social.csv"

    if not os.path.exists(elections_path) or not os.path.exists(social_path):
        raise HTTPException(status_code=400, detail="Upload both CSV files first")

    elections = pd.read_csv(elections_path)
    social = pd.read_csv(social_path)

    df = elections.merge(social, on="candidate_id")
    df["vote_share"] = df["votes"] / df["total_votes"]

    result_df, model, accuracy = train_and_predict(df)

    predictions = result_df[
        ["constituency_id", "candidate_id", "win_probability"]
    ].to_dict(orient="records")

    bar_path, pie_path = generate_charts(predictions)

    try:
        shap_path = generate_shap(
            model,
            result_df[["vote_share", "sentiment", "engagement"]]
        )
    except Exception:
        shap_path = None

    pm_result = predict_pm(elections, predictions)

    response = {
        "predictions": predictions,
        "pm_prediction": pm_result,
        "model_accuracy": round(accuracy * 100, 2),
        "shap_report": shap_path
    }

    try:
        pdf_path = generate_pdf(response, bar_path, pie_path)
        response["pdf_report"] = pdf_path
    except Exception:
        response["pdf_report"] = None

    return response

@app.get("/download/pdf")
def download_pdf():
    path = f"{REPORT_DIR}/election_report.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="PDF not generated yet")
    return FileResponse(path, filename="election_report.pdf")

@app.get("/download/shap")
def download_shap():
    path = f"{REPORT_DIR}/shap_summary.png"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="SHAP report not generated yet")
    return FileResponse(path, filename="shap_report.png")

@app.post("/reset")
def reset():
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    shutil.rmtree(REPORT_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    return {"status": "reset complete"}
