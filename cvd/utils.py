# utils.py
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
# from .models import Scaler, best_rf_model

def show_visualizations(patients_data):
    # Normal ranges for reference
    # reshaped_data = np.array(data).reshape(1, -1)
    # std_data = Scaler.transform(data)
    # prediction = best_rf_model.predict(std_data)
    normal_ranges = {
        "Age": (20, 80),
        "Resting BP": (90, 120),
        "Cholesterol": (150, 200),
        "Max Heart Rate": (70, 200),
        "Oldpeak": (0, 2),
        "Chest Pain Type": ('Asymptomatic'),
        "Fasting Blood Sugar": ('False'),
        "Resting ECG": ('False'),
        "Exercise Angina": ('No'),
        "ST Slope": ('Upsloping')
    }
    attribute_names = ["Age", "Gender", "Chest Pain Type", "Resting BP", "Cholesterol",
                       "Fasting Blood Sugar", "Resting ECG", "Max Heart Rate",
                       "Exercise Angina", "Oldpeak", "ST Slope"]
    
    # Function to save plot as base64 image
    def save_plot_as_base64():
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.clf()  # Clear the plot
        return image_base64

    images = []

    # Plot 1: Patient Attributes vs. Normal Ranges
    plt.figure(figsize=(10, 6))
    for idx, name in enumerate(normal_ranges.keys()):
        plt.bar(name, patients_data[idx], color='orange', label="Patient Value")
        plt.plot([name, name], normal_ranges[name], color='green', linewidth=5, alpha=0.5, label="Normal Range")
    plt.xlabel("Attributes")
    plt.ylabel("Values")
    plt.title("Patient Attributes Compared to Normal Ranges")
    plt.legend()
    images.append(save_plot_as_base64())

    # Plot 2: Risk Factor Radar Chart
    plt.figure(figsize=(6, 6))
    categories = list(normal_ranges.keys())
    values = [patients_data[idx + 1] for idx, _ in enumerate(categories)]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    plt.polar(angles, values, color="blue", marker="o")
    plt.fill(angles, values, color="blue", alpha=0.25)
    plt.title("Risk Factor Radar Chart")
    images.append(save_plot_as_base64())

    return images
