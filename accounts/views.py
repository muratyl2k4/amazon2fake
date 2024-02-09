
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from .forms import CreateUserForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active=False
                user.save()
                messages.success(request, 'Hesabınız Başarıyla Oluşturuldu \n Lütfen Giriş Yapın')
                return redirect("/login")
            else:
                errors = [x for x in form.errors.as_data()]
                print(errors)
                if errors.count("password2") > 0 :
                    messages.error(request , "Lütfen İki şifreyi de aynı girin (Şifreler 10 karakterden fazla olmalıdır)")
                if errors.count("username") > 0:
                    messages.error(request , "Bu kullanıcı adı alınamaz")


        else :
            form = CreateUserForm()
    data = {"form" : form}
    return render(request , "register.html" , data)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request , username=username , password = password)

            if user is not None:
                login(request , user)
                return redirect("sshome")
    data = {}

    return render(request , "login.html" , data)


def logoutUser(request):
    logout(request)
    return redirect("sshome")