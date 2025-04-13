from django.shortcuts import render
from django.contrib import messages
import numpy as np
import pandas as pd
import pickle
import os

import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image

from sklearn.ensemble import RandomForestClassifier

from HeartBitz.settings import BASE_DIR
from .forms import PredictionForm
from .utils import show_visualizations
from django.conf import settings
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
# Load the pre-trained model from the file
# Define the path to your model.pkl file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

def cholesterol_bp_analysis(chol, bp, filename):
    categories = ['Cholesterol', 'Resting BP']
    patient_values = [chol, bp]
    normal_values = [200, 120]  # Healthy reference values
    risk_values = [250, 140]    # High-risk thresholds
    x = np.arange(len(categories))  # Label positions
    width = 0.25  # Bar width
    plt.figure(figsize=(8, 5))  # Larger figure for better spacing
    # Create bars
    plt.bar(x - width, normal_values, width, color='green', label="Healthy Avg", alpha=0.7)
    plt.bar(x, patient_values, width, color='blue', label="Patient", alpha=0.7)
    plt.bar(x + width, risk_values, width, color='red', label="Risk Threshold", alpha=0.7)
    # Formatting
    plt.xticks(x, categories, rotation=15, ha="right")  # Rotate labels for clarity
    plt.xlabel("Health Parameters", fontsize=12)
    plt.ylabel("Values", fontsize=12)
    plt.title("Cholesterol & Blood Pressure Analysis", fontsize=14)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Light grid for better readability
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def heart_rate_oldpeak_chart(hr, oldpeak, filename):
    plt.figure(figsize=(7, 5))  # Increased figure size for better visibility
    # Scatter plot for patient's data point
    plt.scatter(hr, oldpeak, color='red', marker='o', s=100, edgecolors='black', label="Patient Data")
    # Reference lines for normal & risk levels
    plt.axhline(y=1.5, color='green', linestyle='--', linewidth=2, label="Normal Oldpeak (<1.5)")
    plt.axhline(y=2.5, color='orange', linestyle='--', linewidth=2, label="Moderate Risk (1.5 - 2.5)")
    plt.axhline(y=3.5, color='red', linestyle='--', linewidth=2, label="High Risk (>2.5)")
    plt.axvline(x=150, color='blue', linestyle='--', linewidth=2, label="Normal Heart Rate (≈150)")
    # Labels & title
    plt.xlabel("Max Heart Rate (Thalach)", fontsize=12)
    plt.ylabel("ST Depression (Oldpeak)", fontsize=12)
    plt.title("Heart Rate vs Oldpeak Analysis", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)  # Light grid for better readability
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def comparison_bar_chart(patient_values, normal_values, attributes, filename):
    x = np.arange(len(attributes))  # the label locations
    width = 0.35  # the width of the bars

    plt.figure(figsize=(10, 5))
    plt.bar(x - width/2, patient_values, width, label='Patient Values', color='blue')
    plt.bar(x + width/2, normal_values, width, label='Normal Values', color='green')

    plt.xlabel('Attributes')
    plt.ylabel('Values')
    plt.title('Comparison of Patient Values with Normal Values')
    plt.xticks(x, attributes, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Light grid for better readability
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def risk_gauge_chart(risk_score, filename):
    fig, ax = plt.subplots(figsize=(6, 3))
    # Define gauge colors & risk levels
    categories = ["Normal", "Low", "Moderate", "High", "Extreme"]  # Now 5 labels
    colors = ["green", "blue", "orange", "red", "darkred"]
    values = [0, 25, 50, 75, 100]  # Now matches 5 labels
    # Draw risk meter
    for i in range(4):
        ax.barh(y=1, width=values[i+1] - values[i], left=values[i], color=colors[i], height=1)
    # Plot risk score as arrow
    ax.axvline(x=risk_score, color="black", linewidth=3, linestyle="dashed")
    ax.text(risk_score + 1, 1.2, f"Risk: {int(risk_score)}%", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_xticks(values)
    ax.set_xticklabels(categories, fontsize=10, fontweight="bold")
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_title("Heart Disease Risk Level", fontsize=14, fontweight="bold")
    plt.savefig(filename)
    plt.close()

def prv_rec(age, gender, chest_pain, bp, cholesterol, fasting_bs, ecg, max_hr, angina, oldpeak, st_slope,result,):
    recommendations = []
    
    # Age-Based Recommendations
    if age > 50:
        recommendations.append("✅ Regular heart check-ups and ECG screening recommended for patients above 50.")
        recommendations.append("🩺 Monitor cholesterol and blood pressure frequently.")
    if age > 65:
        recommendations.append("⚠ Elderly patients should be cautious of high blood pressure and cholesterol levels.")
        recommendations.append("💊 Consult a doctor about medications for heart disease prevention.")
    
    # Cholesterol-Based Recommendations
    if cholesterol > 200:
        recommendations.append("⚠ High cholesterol detected. Reduce intake of saturated fats and increase fiber.")
    if cholesterol > 250:
        recommendations.append("🚨 Very high cholesterol levels. Medication and strict dietary control needed.")
    if cholesterol > 300:
        recommendations.append("🏥 Immediate medical intervention required. Consider lipid-lowering drugs.")
    
    # Blood Pressure-Based Recommendations
    if bp > 130:
        recommendations.append("⚠ Elevated blood pressure. Reduce salt intake and maintain hydration.")
    if bp > 140:
        recommendations.append("🚨 High BP detected. Monitor regularly and follow a low-sodium diet.")
    if bp > 160:
        recommendations.append("🏥 Severe hypertension. Consult a cardiologist and consider medication.")
    
    # Heart Rate-Based Recommendations
    if max_hr < 100:
        recommendations.append("⚠ Low heart rate. Engage in mild exercises like walking or yoga.")
    if max_hr > 180:
        recommendations.append("🚨 High heart rate. Avoid strenuous activities and seek medical advice.")
    
    # Chest Pain Type-Based Recommendations
    if chest_pain == 0:
        recommendations.append("✅ Typical Angina. Monitor symptoms and manage with lifestyle changes.")
    if chest_pain == 1:
        recommendations.append("⚠ Atypical Angina detected. Consider stress test for further evaluation.")
    if chest_pain == 2:
        recommendations.append("🚨 Non-Anginal Pain. Maintain cardiac health through diet and exercise.")
    if chest_pain == 3:
        recommendations.append("🏥 Asymptomatic condition. Immediate cardiologist consultation recommended.")
    
    # Exercise Angina-Based Recommendations
    if angina == 1:
        recommendations.append("🚨 Exercise-induced angina detected. Avoid heavy exertion and consult a doctor.")
        recommendations.append("💊 Discuss medication options for symptom relief.")
    
    # Oldpeak-Based Recommendations
    if oldpeak > 1:
        recommendations.append("⚠ Slight ST depression detected. Maintain a heart-healthy lifestyle.")
    if oldpeak > 2:
        recommendations.append("🚨 High ST depression level. Further cardiac tests required.")
    if oldpeak > 3:
        recommendations.append("🏥 Immediate stress test and cardiologist consultation advised.")
    
    # ST Slope-Based Recommendations
    if st_slope == 0:
        recommendations.append("✅ Upward slope. Generally considered normal but monitor closely.")
    if st_slope == 1:
        recommendations.append("⚠ Flat slope detected. Can indicate potential heart issues, consider testing.")
    if st_slope == 2:
        recommendations.append("🚨 Downward ST slope detected. High risk of severe heart disease, seek immediate medical advice.")
    
    if not recommendations or result == 0:
        recommendations.append("\n\n✅ Your heart health looks good. Maintain a healthy lifestyle!")
        recommendations.append("🚴 Keep engaging in physical activity and balanced nutrition.")
    
    return recommendations


def predict(request):
    result = None
    chart_urls = {}

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = np.array([
                form.cleaned_data['age'],
                form.cleaned_data['sex'],
                form.cleaned_data['cp'],
                form.cleaned_data['trestbps'],
                form.cleaned_data['chol'],
                form.cleaned_data['fbs'],
                form.cleaned_data['restecg'],
                form.cleaned_data['thalach'],
                form.cleaned_data['exang'],
                form.cleaned_data['oldpeak'],
                form.cleaned_data['slope'],
            ]).reshape(1, -1)

            r = "Heart Disease Detected !! \n Get your appointment today."
            l = "No Heart Disease !"
            result = model.predict(data)[0]
            result = r if result == 1 else l

            # Risk Level Calculation
            risk_score = calculate_risk_score(data)

            # Save images in media folder
            base_path = os.path.join(settings.MEDIA_ROOT, 'charts')
            os.makedirs(base_path, exist_ok=True)

            # Generate and save charts
            chol_bp_chart_path = os.path.join(base_path, 'chol_bp_chart.png')
            cholesterol_bp_analysis(int(data[0][4]), int(data[0][3]), chol_bp_chart_path)
            chart_urls['chol_bp_chart'] = settings.MEDIA_URL + 'charts/chol_bp_chart.png'

            hr_oldpeak_chart_path = os.path.join(base_path, 'hr_oldpeak_chart.png')
            heart_rate_oldpeak_chart(int(data[0][7]), float(data[0][9]), hr_oldpeak_chart_path)
            chart_urls['hr_oldpeak_chart'] = settings.MEDIA_URL + 'charts/hr_oldpeak_chart.png'

            attributes = ["Resting BP", "Cholesterol", "Heart Rate"]
            normal_values = [120, 200, 150]  # Normal values for a healthy person
            patient_values = [
                int(data[0][3]),  # Resting BP
                int(data[0][4]),  # Cholesterol
                int(data[0][7])   # Heart Rate
            ]
            comparison_chart_path = os.path.join(base_path, 'comparison_bar.png')
            comparison_bar_chart(patient_values, normal_values, attributes, comparison_chart_path)
            chart_urls['comparison_bar'] = settings.MEDIA_URL + 'charts/comparison_bar.png'

            risk_chart_path = os.path.join(base_path, 'risk_gauge.png')
            risk_gauge_chart(risk_score, risk_chart_path)
            chart_urls['risk_gauge'] = settings.MEDIA_URL + 'charts/risk_gauge.png'
            
            recommendations = prv_rec(
                int(data[0][0]), int(data[0][1]), int(data[0][2]), int(data[0][3]), int(data[0][4]), int(data[0][5]),
                int(data[0][6]), int(data[0][7]), int(data[0][8]), float(data[0][9]), int(data[0][10]), result
            )

            return render(request, 'cvd/result.html', {
                
                'result': result, 
                'recommendations': recommendations,
                'chart_urls': chart_urls
            })

    else:
        form = PredictionForm()

    return render(request, 'cvd/index.html', {'form': form, 'result': result})

def calculate_risk_score(data):
    age = int(data[0][0])  
    trestbps = int(data[0][3])  
    chol = int(data[0][4])  
    thalach = int(data[0][7])  
    oldpeak = float(data[0][9])  
    risk_score = 0
    # Age Factor
    if age > 50:
        risk_score += 15
    if age > 60:
        risk_score += 10
    # Blood Pressure Factor
    if trestbps > 130:
        risk_score += 15
    if trestbps > 140:
        risk_score += 10
    # Cholesterol Factor
    if chol > 200:
        risk_score += 15
    if chol > 250:
        risk_score += 10
    # Heart Rate Factor
    if thalach < 120:
        risk_score += 15
    elif thalach < 140:
        risk_score += 10
    # Oldpeak Factor
    if oldpeak > 1.5:
        risk_score += 15
    if oldpeak > 2.5:
        risk_score += 10
    # Normalize the risk score to a percentage (0-100)
    risk_percentage = min(risk_score, 100)
    return risk_percentage
  
import tensorflow as tf
import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Load the trained model
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
model_path = os.path.join(BASE_DIR, 'model.h5')

mod = tf.keras.models.load_model(model_path)


# Define the labels
labels = ['cataract', 'diabetic_retinopathy', 'glaucoma', 'normal']  # Update with actual class names

def preprocess_image(image_path):
    """Preprocess the image to fit the model input requirements."""
    img = load_img(image_path, target_size=(224, 224))  # Resize image to match model input size
    img = img_to_array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def get_heart_disease_probability(class_label):
    """Estimate heart disease probability based on the predicted eye condition."""
    probabilities = {
        'diabetic_retinopathy': 35,
        'glaucoma': 20,
        'cataract': 7,
        'normal': 1
    }
    return probabilities.get(class_label, 0)

def pred(image_path):
    """Predict the class of the given eye fundus image and estimate heart disease probability."""
    img = preprocess_image(image_path)
    predictions = mod.predict(img)
    predicted_class = np.argmax(predictions, axis=1)[0]  # Get index of max confidence
    confidence = np.max(predictions) * 100  # Convert to percentage
    predicted_label = labels[predicted_class]
    heart_disease_probability = get_heart_disease_probability(predicted_label)
    return predicted_label, confidence, heart_disease_probability

def upl(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        image_path = default_storage.save(image.name, image)
        full_path = default_storage.path(image_path)
        predicted_label, confidence, heart_disease_probability = pred(full_path)
        return render(request, 'cvd/res.html', {
            'label': predicted_label,
            'confidence': confidence,
            'heart_disease_probability': heart_disease_probability
        })
    return render(request, 'cvd/res.html')
