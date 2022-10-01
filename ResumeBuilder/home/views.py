from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from validate_email_address import validate_email

import controller.connection
from controller import UserOperation as Uo, Email_Sender as es
from random import randint


# Create your views here.
def index(request):
    return render(request, 'index.html')


def sign_up(request):
    return render(request, 'sign-up.html')


def sign_in(request):
    return render(request, 'sign-in.html')


def signup_con(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        isExists = validate_email('dhobaleprasad3@gmail.com', verify=True)
        if isExists == "True":
            passwd = request.POST.get('passwd')
            uid = randint(100, 999)
            token = randint(10000, 99999)
            chk = Uo.check_id_email(uid, email)
            if chk != 1:
                user = (uid, fname, lname, email, passwd, token)
                reg = Uo.reg_user(user)
                if reg == 1:
                    link = "http://localhost:8000/verification?id=" + str(uid) + "&token=" + str(token) + ""
                    es.Sender("Resume Builder Email Verification", email, "evs", link)
                    messages.success(request, "Thanks " + fname + "..! For Joining Our Portal..!!\nVerification Email "
                                                                  "sent to Your Email.")
                else:
                    messages.warning(request, "Something Went Wrong Please Try Again Later.")
            else:
                messages.warning(request, "ID Or Email Address Already Exist !! Please Try Once..")
        else:
            messages.warning(request, "The Entered Email ID Not Exist")
    return HttpResponseRedirect('/signup.html')


def signin_con(request):
    cred = {}
    if request.method == "POST":
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        chk = Uo.login(email, passwd)
        if chk == 1:
            evs = Uo.check_evs(email)
            uid, token = Uo.resend_credentials(email)
            cred = {
                "uid": uid,
                "token": token,
                "login_attempted": "true",
                "email": email
            }
            if evs != 0:
                messages.success(request, "Logged In successfully..!!")
                request.session['login_status'] = "true"
                profile = Uo.get_profile(email)
                profile = {
                    'uid' : profile[0],
                    'fname': profile[1],
                    'lname': profile[2],
                    'email': profile[3],
                    'passwd': profile[4],
                    'token': profile[5],
                    'evs': profile[6]
                }
                request.session['user'] = profile
                return HttpResponseRedirect('/dashboard')
            else:
                messages.warning(request, "Email Not Verified. Please Verify Your Email")
        else:
            messages.warning(request, "Invalid Credentials....")
    return render(request, 'sign-in.html', cred)


# Verify Email
def verification(request):
    if request.method == "GET":
        uid = request.GET.get('id')
        token = request.GET.get('token')
        ver = Uo.verify_email(uid, token)
        if ver == 1:
            messages.success(request, "Email Verified Successfully..!!")
        else:
            messages.warning(request, "Something Went Wrong..Try Again Later..!!")
    return HttpResponseRedirect("/signin.html")


# Resend Verification Email
def resend_ver_email(request):
    if request.method == "POST":
        uid = request.GET.get('id')
        token = request.GET.get('token')
        email = request.GET.get('email')
        link = "http://localhost:8000/verification?id=" + str(uid) + "&token=" + str(token) + ""
        es.Sender("Resume Builder Email Verification", email, "evs", link)
        messages.success(request, "Verification Email Sent to Your Email")
    return HttpResponseRedirect('/signin.html')


# Forgot Password
def fp(request):
    return render(request, 'forgot-password.html')


# Forgot Password Controller
def forgot_password(request):
    cred = {}
    if request.method == "POST":
        email = request.POST.get('email')
        check_email = Uo.check_email(email)
        if check_email == 1:
            check_evs = Uo.check_evs(email)
            if check_evs == 1:
                passwd = Uo.getPasswd(email)
                es.Sender("Resume Builder Forgot Password", email, "fg", str(passwd[0]))
                messages.success(request, "Password Sent to Your Submitted Email !!")
            else:
                messages.warning(request, "Email Not Verified. Please verify your Email!!")
                uid, token = Uo.resend_credentials(email)
                cred = {
                    "uid": uid,
                    "token": token,
                    "login_attempted": "true",
                    "email": email
                }

        else:
            messages.warning(request, "Email Not Registered With Us..Please Try Again")
    return render(request, 'forgot-password.html', cred)


# Dashboard
def dashboard(request):
    return render(request, 'dashboard.html')


# Logging Out
def logout(request):
    request.session['login_status'] = ""
    request.session['user'] = ""
    messages.info(request, "Logged Out Successfully..!!")
    print("Logged out")

    return HttpResponseRedirect("/signin.html")

# Update Profile
def update_profile(request, id):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        passwd = request.POST.get('passwd')
        up_details = (fname, lname, passwd, id)
        up = Uo.update_profile(up_details)
        print(up)
        if up == 1:
            profile = Uo.get_profile(id)
            profile = {
                'uid': profile[0],
                'fname': profile[1],
                'lname': profile[2],
                'email': profile[3],
                'passwd': profile[4],
                'token': profile[5],
                'evs': profile[6]
            }
            request.session['user'] = profile
            messages.success(request, "Profile Updated Successfully..!!")
        else:
            messages.warning(request, "Something Went Wrong..!!")
    return HttpResponseRedirect("/dashboard")

# Delete Profile
def delete_profile(request, id):
    del_status = Uo.delete_profile(id)
    if del_status == 1:
        messages.success(request, "Profile Deleted Successfully..!!")
    else:
        messages.success(request, "Something Went Wrong..!!")
    return HttpResponseRedirect("/signin")
