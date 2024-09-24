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