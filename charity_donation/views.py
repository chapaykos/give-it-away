from django.shortcuts import render, redirect
from django.views import View
from charity_donation import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator


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
        paginator_foundations = Paginator(foundations, 5)
        non_gov_org = models.Institution.objects.filter(type='2')
        paginator_non_gov_org = Paginator(non_gov_org, 5)
        local_charity = models.Institution.objects.filter(type='3')
        paginator_local_charity = Paginator(local_charity, 5)
        page_f = request.GET.get('page')
        return render(request, 'charity_donation/index.html', {'worki': result,
                                                               'institutions': total_instituions,
                                                               'foundations': foundations,
                                                               'non_gov_org': non_gov_org,
                                                               'local_charity': local_charity})


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        categories = models.Category.objects.all()
        institutions = models.Institution.objects.all()
        in_cat_ids = []
        for institution in institutions:
            in_cat_ids.append(institution.category_ids())
        return render(request, 'charity_donation/form.html', {'categories': categories,
                                                              'institutions': institutions,
                                                              'in_cat_ids': in_cat_ids})

    def post(self, request):
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        data = request.POST.get('data')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')
        bags = request.POST.get('bags')
        categories = request.POST.getlist('categories')
        institution_id = int(request.POST.get('organization'))
        institution = models.Institution.objects.get(pk=institution_id)
        donation = models.Donation.objects.create(quantity=bags, institution=institution,
                                                  address=address, phone_number=phone, city=city, zip_code=postcode,
                                                  pick_up_date=data, pick_up_time=time, pick_up_comment=more_info,
                                                  user=request.user)
        donation.categories.set(categories)

        return redirect('donation_success')


class DonationSuccess(View):
    def get(self, request):
        return render(request, 'charity_donation/form-confirmation.html')


class Login(View):
    def get(self, request):
        return render(request, 'charity_donation/login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('register')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')


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
            user = User.objects.create_user(username=email, password=password,
                                            first_name=name, last_name=surname)
            user.save()
        return redirect('login')


class Profile(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        donations_taken = models.Donation.objects.filter(user=request.user, is_taken=True)
        donations_not_taken = models.Donation.objects.filter(user=request.user, is_taken=False)
        return render(request, 'charity_donation/profile.html', {'donations_taken': donations_taken,
                                                                 'donations_not_taken': donations_not_taken})

    def post(self, request):
        donation_id = request.POST.get('donation_id')
        donation = models.Donation.objects.get(pk=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect('profile')


class ProfileSettings(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'charity_donation/profile_settings.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        password_old = request.POST.get('password_old')
        password_new1 = request.POST.get('password_new1')
        password_new2 = request.POST.get('password_new2')
        if 'update_profile' in request.POST:
            # check for password
            user = authenticate(request, username=request.user.username, password=password)
            # update user data
            if user is not None:
                request.user.username = username
                request.user.email = email
                request.user.first_name = name
                request.user.last_name = surname
                request.user.save()
                return redirect("profile")
        elif 'change_password' in request.POST:
            # new password
            user = authenticate(request, username=request.user.username, password=password_old)
            if user is not None and password_new1 == password_new2:
                request.user.set_password(f'{password_new1}')
                request.user.save()
                return redirect('profile')
            else:
                return redirect("profile_settings")
