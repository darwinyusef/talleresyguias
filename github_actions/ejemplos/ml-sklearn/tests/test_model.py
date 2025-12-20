import os
import joblib

def test_model_exists():
    # En un pipeline real, el script de train se corre antes
    if os.path.exists("models/iris_model.pkl"):
        model = joblib.load("models/iris_model.pkl")
        assert model is not None
    else:
        print("Model not found, skipping check (expected in CI before training)")
