# views.py
import pickle
from django.shortcuts import render
from .forms import FertilizerForm
import numpy as np
import os

# Load the machine learning model
# with open('C:/Users/SPECTRE/Documents/KALRO/Fertilizer/frcode\kfrs/kfrs_backend/kfrs_api/model.pkl', 'rb') as model_file:
fileDir = os.path.dirname(os.path.realpath('__file__'))
model = os.path.join(fileDir, 'kfrs_api/model.pkl')
with open(model, 'rb') as model_file:
    loaded_model = pickle.load(model_file)


# Mapping for categorical data (this should match how the data was encoded during training)
CROP_TYPE_ENCODING = {
    'maize': [1, 0],  # maize is encoded as [1, 0], rice will be [0, 1], and wheat (dropped category) as [0, 0]
    'rice': [0, 1],
    'wheat': [0, 0]
}

SOIL_TYPE_ENCODING = {
    'clay': [1, 0],  # clay is encoded as [1, 0], loam as [0, 1], and sandy (dropped category) as [0, 0]
    'loam': [0, 1],
    'sandy': [0, 0]
}



def fertilizer_recommendation(request):
    recommendation = None
    if request.method == "POST":
        form = FertilizerForm(request.POST)
        if form.is_valid():
            # Get input data from the form
            crop_type = form.cleaned_data['crop_type']
            soil_type = form.cleaned_data['soil_type']
            nitrogen_level = form.cleaned_data['nitrogen_level']
            phosphorus_level = form.cleaned_data['phosphorus_level']
            potassium_level = form.cleaned_data['potassium_level']

            # Prepare the data for the model (e.g., assuming the model expects these features)
            # input_data = [[nitrogen_level, phosphorus_level, potassium_level]]

            # Encode categorical variables using the same encoding as the model
            crop_encoded = CROP_TYPE_ENCODING.get(crop_type, [0, 0])  # Default to [0, 0] if crop_type not found
            soil_encoded = SOIL_TYPE_ENCODING.get(soil_type, [0, 0])  # Default to [0, 0] if soil_type not found

            # Combine all the features into a single input array
            input_data = np.array([nitrogen_level, phosphorus_level, potassium_level] + crop_encoded + soil_encoded).reshape(1, -1)


            # Make predictions using the loaded model
            predicted_fertilizer = loaded_model.predict(input_data)

            # Assuming the model predicts fertilizer amounts in the form [N, P, K]
            recommendation = {
                'crop_type': crop_type,
                'soil_type': soil_type,
                'recommended_nitrogen': predicted_fertilizer[0][0],
                'recommended_phosphorus': predicted_fertilizer[0][1],
                'recommended_potassium': predicted_fertilizer[0][2]
            }
    else:
        form = FertilizerForm()

    context = {
        'form': form,
        'recommendation': recommendation
    }

    return render(request, 'kfrs_ui/index.html', context)



from django.shortcuts import render, redirect
from .forms import UIModelForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . models import approvals
from . serializers import approvalsSerializers
import pickle
#from sklearn.externals import joblib
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd


class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers
      

# def kfrs_form(request):
#     if request.method == "POST":
#         kfrs_form = MyForm(request.POST)
#         if kfrs_form.is_valid():  
#             kfrs_form = kfrs_form.save(commit=False)  # Corrected 'form.save()' to 'kfrs_form.save()'
#     else:
#         kfrs_form = MyForm()
    
#     context = {
#         "kfrs_form": kfrs_form
#     }

#     return render(request, 'kfrs_ui/index.html', context)


def kfrs_form(request):
    msg="Enter fields"
    if request.method == "POST":
        form = UIModelForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            msg="Successfully Submitted"
            return redirect('kfrs_form')  # Redirect to a success page after submission
    else:
        form = UIModelForm()

    context = {
        'form': form,
        'msg': msg
    }
    
    return render(request, 'kfrs_ui/index.html', context)

def advisories(request):
    msg="Enter fields"
    if request.method == "POST":
        form = UIModelForm(request.POST)
        if form.is_valid():
            Firstname = form.cleaned_data.get('firstname')
            Lastname = form.cleaned_data.get('lastname')
            Dependants=form.cleaned_data.get('dependants')
            ApplicantIncome=form.cleaned_data.get('applicantincome')
            CoapplicatIncome=form.cleaned_data.get('coapplicatincome')
            LoanAmount=form.cleaned_data.get('loanamt')
            Loan_Amount_Term=form.cleaned_data.get('loanterm')
            Credit_History=form.cleaned_data.get('credithistory')
            Gender=form.cleaned_data.get('gender')
            Married=form.cleaned_data.get('married')
            Education=form.cleaned_data.get('graduatededucation')
            Self_Employed=form.cleaned_data.get('selfemployed')
            Property_Area=form.cleaned_data.get('area')
            myDict=(request.POST).dict()
            df=pd.DataFrame(myDict, index=[0])

            print(approvereject(ohevalue(df)))

            # form.save()  # Save the form data to the database
            msg="Successfully Submitted"
            return redirect('kfrs_form')  # Redirect to a success page after submission
    else:
        form = UIModelForm()

    context = {
        'form': form,
        'msg': msg
    }
    
    return render(request, 'kfrs_ui/index.html', context)


@api_view(["POST"])
def approvereject(request):
	try:
		mdl=joblib.load("C:/Users/SPECTRE/Documents/KALRO/Fertilizer/frcode\kfrs/kfrs_backend/kfrs_api/loan_model.pkl")
		#mydata=pd.read_excel('/Users/sahityasehgal/Documents/Coding/bankloan/test.xlsx')
		mydata=request.data
		unit=np.array(list(mydata.values()))
		unit=unit.reshape(1,-1)
		scalers=joblib.load("C:/Users/SPECTRE/Documents/KALRO/Fertilizer/frcode\kfrs/kfrs_backend/kfrs_api/scalers.pkl")
		X=scalers.transform(unit)
		y_pred=mdl .predict(X)
		y_pred=(y_pred>0.58)
		newdf=pd.DataFrame(y_pred, columns=['Status'])
		newdf=newdf.replace({True:'Approved', False:'Rejected'})
		return JsonResponse('Your Status is {}'.format(newdf), safe=False)
	except ValueError as e:
		return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
