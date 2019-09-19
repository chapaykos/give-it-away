from django.shortcuts import render
from django.views import View
from charity_donation import models
from django.contrib.auth.models import User


# Create your views here.

class LandingPage(View):
    def get(self, request):
        total_worki = models.Donation.objects.all()
        result = 0
        total_instituions = 0
        for worek in total_worki:
            result += worek.quantity
        institutions_supported = models.Donation.objects.values('institution').distinct()
        for institution in institutions_supported:
            total_instituions += 1
        return render(request, 'charity_donation/index.html', {'worki': result,
                                                               'institutions': total_instituions})


class AddDonation(View):
    def get(self, request):

        return render(request, 'charity_donation/form.html')


class Login(View):
    def get(self, request):

        return render(request, 'charity_donation/login.html')


class Register(View):
    def get(self, request):

        return render(request, 'charity_donation/register.html')
