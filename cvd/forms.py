from django import forms
# from .models import Listing

class PredictionForm(forms.Form):
    # input2 = [('male', 'Male'), ('female', 'Female')]
    # input3 = [('1', 'Typical angina'), ('2', 'Atypical angina'), ('3', 'Non-angina pain'), ('4', 'Asymptomatic')]
    # input6 = [('true', 'True'), ('false', 'False')]
    # input9 = [('1', 'Yes'), ('0', 'No')]

    age = forms.IntegerField(label="Age", min_value=0, max_value=120, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your age'
    }))
    sex = forms.ChoiceField(choices=[(1, 'Male'), (0, 'Female')], label="Sex")
    cp = forms.ChoiceField(choices=[(1, 'Typical angina'), (2, 'Atypical angina'), (3, 'Non-angina pain'), (4, 'Asymptomatic')], label='Chest_pain')
    trestbps = forms.IntegerField(label="RBP", min_value=0, max_value=200, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Resting Blood Pressure'
    }))
    chol = forms.IntegerField(label="cholesterol", min_value=0, max_value=500, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Cholesterol'
    }))
    thalach = forms.IntegerField(label="HR", min_value=0, max_value=200, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Thalach'
    }))
    restecg = forms.ChoiceField(choices=[(1, 'True'), (0, 'False')], label="Abnormal ECG")
    fbs = forms.ChoiceField(choices=[(1, 'True'), (0, 'False')], label="Fasting Blood Sugar > 120 mg/dl")
    exang = forms.ChoiceField(choices=[('1', 'Yes'), ('0', 'No')], label='angina')
    oldpeak = forms.FloatField(label="oldpeak", min_value=0, max_value=10, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Oldpeak'
    }))
    slope = forms.ChoiceField(choices=[(1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')], label="Slope")
    bmi = forms.FloatField(label="oldpeak", min_value=13, max_value=35, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Body Mass Index'
    }))

    # class Meta:
    #     model = Listing
    #     fields = {'age', 'gender', 'Chest Pain', 'Resting BP',
    #               'Cholesterol', 'FBS', 'Resting ECG', 'Max Heart Rate', 'Exercise Angina'}
