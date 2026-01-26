from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(response, bar_chart_path, pie_chart_path):
    os.makedirs("backend/app/reports", exist_ok=True)

    path = "backend/app/reports/election_report.pdf"
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Election Prediction Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    pm = response["pm_prediction"]
    elements.append(Paragraph(
        f"Prime Minister Prediction: {pm['pm_party']} "
        f"(Seats: {pm['seats']}, Majority: {pm['majority']})",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        f"Model Accuracy: {response['model_accuracy']}%",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 20))
    elements.append(Image(bar_chart_path, width=400, height=250))
    elements.append(Spacer(1, 20))
    elements.append(Image(pie_chart_path, width=400, height=250))

    doc.build(elements)
    return path
