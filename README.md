# ❤️ Heartbitz – Heart Disease Prediction using ML & Eye Retina Analysis using DL

**Heartbitz** is a final year capstone project developed to predict the risk of heart disease by analyzing both structured patient medical data and eye retina images. It leverages a hybrid approach that combines **Machine Learning** algorithms for tabular data and **Deep Learning** techniques (CNN with transfer learning) for image-based diagnosis.

---

## 🧠 Project Objective

To assist in early detection of heart disease by:

- Predicting heart disease risk using **clinical parameters**
- Detecting cardiovascular symptoms via **eye retina image analysis**

---

## 🔍 Features

- 🩺 Input medical data to assess heart health risk
- 👁 Upload retina images to analyze visible signs of cardiovascular conditions
- 🤖 Uses ML (Random Forest, KNN, SVM, Decision Tree) for structured data
- 🧠 Uses CNN with transfer learning for retina image classification
- 📈 Displays prediction results and graphs for better insight

## 🚀 Installation Guide

To run this project locally, follow these steps:

### 1. Clone the Repository
    git clone https://github.com/SahilRM7/Heartbitz.git
### 2. Navigate to the project directory: cd Heartbitz
### 3. (Optional) Create and activate a virtual environment: python3 -m venv venv and source venv/bin/activate
### 4. Install the required dependencies: pip install -r requirements.txt
### 5. Set up the database by running migrations: python manage.py migrate
### 6. Create a superuser for accessing the admin panel: python manage.py createsuperuser
### 7. Start the development server: python manage.py runserver
### 8. Open a web browser and access the application at http://localhost:8000
