import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

def generate_shap(model, X):
    os.makedirs("backend/app/reports", exist_ok=True)

    if len(X) > 30:
        X = X.sample(30, random_state=42)

    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    path = "backend/app/reports/shap_summary.png"
    shap.plots.beeswarm(shap_values, show=False)
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    return path


