from django.shortcuts import render
from django.contrib import messages
import numpy as np
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
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

def attribute_pie_chart(patient_values, attributes, filename):
    attributes = ["Age", "Sex", "Chest Pain Type", "Resting BP", "Cholesterol"]
    plt.figure(figsize=(8, 8))
    colors = ['#99ccff', '#80bfff', '#66b3ff', '#4da6ff', '#3399ff', '#1a8cff', '#007acc', '#006bb3', '#005c99', '#004d80', '#003366']
    plt.pie(patient_values, labels=attributes, autopct='%1.1f%%', startangle=140, colors=colors[:len(attributes)])
    plt.title('Contribution of Attributes to Heart Health', fontsize=16)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(filename)
    plt.close()


def predict(request):
    result = None
    images = []  # Initialize images as an empty list
    chart_url = None  # Define the variable here

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
             # Get form data and convert to numpy array
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
            # Predict using the loaded model
            result = model.predict(data)[0]
            result = r if result == 1 else l

            # images = show_visualizations(data)'images': images
            # Define the full path to the chart
            patient_values = data[0][:5]
            attributes = ["Age", "Sex", "Chest Pain Type", "Resting BP", "Cholesterol"]

            chart_path = os.path.join('heartcare', 'static', 'heartcare', 'chart.png')  # Correct path
            print(f"Saving chart at: {chart_path}")  # Debugging line
            os.makedirs(os.path.dirname(chart_path), exist_ok=True)
            attribute_pie_chart(patient_values, attributes, chart_path)

            # The relative path for use in the template
            chart_url = 'heartcare/chart.png'  # Corrected path
            return render(request, 'cvd/result.html', {'result': result, 'chart_url': chart_url})
            
    else:
        form = PredictionForm()

    return render(request, 'cvd/index.html', {'form': form, 'result': result, 'chart_url': chart_url})
