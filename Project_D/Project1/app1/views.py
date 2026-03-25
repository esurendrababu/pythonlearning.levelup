from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile,Student
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login as dj_login,logout
from django.views import View
from . forms import StudentRegistrationForm,StudentDetailsForm
import sys
# Create your views here.
def base(request):
    return render(request,'app1/base.html')
def index(request):
    return render(request,'app1/index.html')
def team(request):
    return render (request,'app1/team.html')
def contact(request):
    return render (request,'app1/Contact.html')
def innerpage(request):
    return render (request,'app1/innerpage.html')
def login(request):
    return render (request,'app1/login.html')
def signup(request):
    return render (request,'app1/signup.html')                    


def register_attempt(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is taken.')
                return redirect('/register')

            user_obj = User (username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')
        except Exception as e:
            print(e)
    return render (request,'app1/register.html')
def send_mail_after_registration(email,token):
    subject='Your accounts need to be verified'
    message=f'Hi paste the link to verify your accounts http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)


def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your accounts is allready verified')
                return redirect('/accounts/login')
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,'Your accounts has been verified')
            return redirect('/accounts/login')
        else:
            return redirect ('/error')
    except Exception as e:
        print(e)
        return redirect('/')
def login_attempt(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'User not found.')
            return redirect('/accounts/login')
        profile_obj=Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile is not verified check youe mail')
            return redirect('/accounts/login')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password')
            return redirect('/accounts/login')

        dj_login(request,user)
        return redirect('/details')   
    return render(request,'app1/login.html')

def user_logout(request):
    logout(request)
    return redirect('app1:login')
def success(request):
    return render(request,'app1/success.html')

def token_send(request):
    return render(request,'app1/token_send.html')

def error_page(request):
    return render(request,'app1/error.html')

class DetailView(View):
    def get(self,request):
        form=StudentDetailsForm()
        return render(request,'app1/details.html',{'form':form})
    def post(self,request):
        form=StudentDetailsForm(request.POST)
        if form.is_valid():
            usr=request.user
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone=form.cleaned_data['phone']
            reg=Student(user=usr,first_name=first_name,last_name=last_name,email=email,phone=phone)
            reg.save()
            messages.success(request,'Congratulations ! Profile updated Success')
            return redirect('/innerpage')
        return render(request,'app1/details.html',{'form':form,'active':'btn-primary'})


def user_logout(request):
    logout(request)
    return redirect('app1:login')

def runcode(request):
    code_part=''
    y=''
    output=''
    if request.method == 'POST':
        code_part = request.POST['code_area']
        input_part = request.POST['input_area']

        y = input_part
        input_part = input_part.replace("\n"," ").split(" ")
        def input(arg):
            a = input_part[0]
            del input_part[0]
            return a
        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code_part)
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = e
        print(output)

    res = render(request,'app1/innerpage.html',{"code":code_part,"input":y,"output":output})
    return res
































# def innerpage(request):
#     return render(request,'app/inerpage.html')

# def contact(request):
#     return render(request,'app/contact.html')


# def team(request):
#     return render(request,'app/team.html')

# def login(request):
#     return render(request,'app/login.html')

# def signup(request):
#     return render(request,'app/signup.html')
