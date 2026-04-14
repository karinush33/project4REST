from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
import ml_logic
from pydantic import BaseModel
from typing import List

"""
Router for handling Machine Learning operations: training and prediction.
"""

router = APIRouter(tags=["Run Prediction"])


class TrainData(BaseModel):
    x_hours: List[float]
    y_times: List[float]
    degree: int = 3


@router.post("/train")
def train_model(data: TrainData, current_user=Depends(get_current_user)):
    """
    Endpoint to train a personal model for the authenticated user.
    """
    user_name = current_user['user_name']
    ml_logic.train_and_save_model(data.x_hours, data.y_times, user_name, data.degree)
    return {"message": f"Model trained successfully for {user_name}"}


@router.get("/predict/{hours}")
def predict(hours: float, current_user=Depends(get_current_user)):
    """
    Endpoint to predict running time based on planned training hours.
    """
    user_name = current_user['user_name']
    prediction = ml_logic.predict_from_model(user_name, hours)

    if prediction is None:
        raise HTTPException(status_code=404, detail="Model not found. Please train first.")
    return {"predicted_time": prediction}