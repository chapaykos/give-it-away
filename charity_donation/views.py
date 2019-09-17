from django.shortcuts import render
from django.views import View

# Create your views here.

class LandingPage(View):
    return render(request, 'charity_donation/index.html')
class AddDonation(View):

class Login(View):

class Register(View):
