from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Slider, Service, Doctor, Faq, Gallery
from django.views.generic import ListView, DetailView, TemplateView

from django.contrib.auth.models import User
# from .forms import RegisterForm # type: ignore

from django.contrib.auth import authenticate, login
# from .forms import LoginForm # type: ignore
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import logout

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             # Check if email already exists
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, "Email already registered.")
#             else:
#                 user = User.objects.create_user(username=email, email=email, password=password)
#                 user.save()
#                 messages.success(request, "Registration successful!")
#                 return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'hospital/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
            
#             # Authenticate using email instead of username
#             try:
#                 user = User.objects.get(email=email)
#                 user = authenticate(request, username=user.username, password=password)
#             except User.DoesNotExist:
#                 user = None

#             if user is not None:
#                 login(request, user)
#                 return redirect('index')  # Redirect to a 'home' page after successful login
#             else:
#                 messages.error(request, 'Invalid email or password.')
#     elif request.user.is_authenticated:
#         return redirect('index')
#     else:
#         form = LoginForm()
#     return render(request, 'hospital/login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')

class HomeView(ListView):
    template_name = 'hospital/index.html'
    queryset = Service.objects.all()
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.all()
        context['experts'] = Doctor.objects.all()
        return context


class ServiceListView(ListView):
    queryset = Service.objects.all()
    template_name = "hospital/services.html"


class ServiceDetailView(DetailView):
    queryset = Service.objects.all()
    template_name = "hospital/service_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.all()
        return context


class DoctorListView(ListView):
    template_name = 'hospital/team.html'
    queryset = Doctor.objects.all()
    paginate_by = 8


class DoctorDetailView(DetailView):
    template_name = 'hospital/team-details.html'
    queryset = Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class FaqListView(ListView):
    template_name = 'hospital/faqs.html'
    queryset = Faq.objects.all()


class GalleryListView(ListView):
    template_name = 'hospital/gallery.html'
    queryset = Gallery.objects.all()
    paginate_by = 9


class ContactView(TemplateView):
    template_name = "hospital/contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject == '':
            subject = "Heartcare Contact"

        if name and message and email and phone:
            send_mail(
                subject+"-"+phone,
                message,
                email,
                ['expelmahmud@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, " Email hasbeen sent successfully...")

        return redirect('contact')
    
# class LoginView(TemplateView):
#     template_name = "hospital/login.html"

#     def post(self, request, *args, **kwargs):
#         Name = request.POST.get('name')
#         phone_number = request.POST.get('phone')
#         return redirect('login')
