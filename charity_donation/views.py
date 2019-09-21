from django.shortcuts import render, redirect
from django.views import View
from charity_donation import models
from django.contrib.auth.models import User

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
        foundations = models.Institution.objects.filter(type='1')
        non_gov_org = models.Institution.objects.filter(type='2')
        local_charity = models.Institution.objects.filter(type='3')
        return render(request, 'charity_donation/index.html', {'worki': result,
                                                               'institutions': total_instituions,
                                                               'foundations': foundations,
                                                               'non_gov_org': non_gov_org,
                                                               'local_charity': local_charity})


class AddDonation(View):
    def get(self, request):

        return render(request, 'charity_donation/form.html')


class Login(View):
    def get(self, request):

        return render(request, 'charity_donation/login.html')


class Register(View):
    def get(self, request):
        return render(request, 'charity_donation/register.html')
    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            user = User.objects.create_user(username=email, password=password, first_name=name, last_name=surname)
            user.save()
        return redirect('login')
