import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def train_and_save_model(training_hours, running_times, model_name, degree=3):
    """
    Trains a polynomial regression model based on user data and saves it to a pkl file.
    """
    try:
        X = np.array(training_hours).reshape(-1, 1)
        y = np.array(running_times)
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        joblib.dump((model, poly), f"{model_name}.pkl")
        return model
    except Exception as e:
        print(f"Error during training: {e}")
        return None

def predict_from_model(model_name, hours_value):
    """
    Loads a saved model from a pkl file and predicts the running time for a given input.
    """
    try:
        model, poly = joblib.load(f"{model_name}.pkl")
        x_input = np.array([[hours_value]])
        x_poly = poly.transform(x_input)
        prediction = model.predict(x_poly)
        return float(prediction[0])
    except FileNotFoundError:
        return None
    except Exception as e:
        return None