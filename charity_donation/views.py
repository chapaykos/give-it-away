from django.shortcuts import render
from django.views import View


# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'charity_donation/index.html')


class AddDonation(View):
    def get(self, request):

        return render(request, 'charity_donation/form.html')


class Login(View):
    def get(self, request):

        return render(request, 'charity_donation/login.html')


class Register(View):
    def get(self, request):

        return render(request, 'charity_donation/register.html')
