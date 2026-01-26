import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os

def generate_charts(predictions):
    os.makedirs("backend/app/reports", exist_ok=True)

    labels = [p["candidate_id"] for p in predictions]
    values = [p["win_probability"] * 100 for p in predictions]

    bar_path = "backend/app/reports/bar_chart.png"
    plt.figure(figsize=(7, 4))
    plt.bar(labels, values)
    plt.ylabel("Win Probability (%)")
    plt.title("Win Probability by Candidate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()

    pie_path = "backend/app/reports/pie_chart.png"
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Win Probability Distribution")
    plt.savefig(pie_path)
    plt.close()

    return bar_path, pie_path

