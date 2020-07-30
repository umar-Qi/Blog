from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

# Create your views here.
#HTML pages
def index(request):
    return render(request, 'home/index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<5 or len(phone)<9 or len(content)<4:
            messages.error(request, "The value you entered is not valid")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent to the admin")
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>100:
        posts = Post.objects.none()
    else:
        poststitle = Post.objects.filter(title__icontains=query)
        postscontent = Post.objects.filter(content__icontains=query)
        posts = poststitle.union(postscontent)
    if posts.count() == 0:
        messages.warning(request, "No search results Found! please refine your query")
    param = {'posts': posts, 'query': query}
    return render(request, 'home/search.html', param)

#Authentication APIs
def handlesignup(request):
    if request.method == 'POST':
        #Get the post parameters
        userName = request.POST['userName']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        userEmail = request.POST['userEmail']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        #Check for Error inputs during submition
        if len(userName) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('home')
        if not userName.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, 'Password do not match')
            return redirect('home')
        #Create User
        myuser = User.objects.create_user(userName, userEmail, pass1)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        send_mail(userName, "Hi this is my django app", userEmail, ['umar66655@gmail.com'])
        #email_sender = "admin@gmail.com"
        #msg = f"""\
        #    Subject: SignUp Confirmation
        #    To: {userEmail}
        #    From: {email_sender}
        #    Password of your new account on BLOGGER: {pass1}
        #
        #    Keep this password save and never share it to others."""
        #context = ssl.create_default_context()
        #with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        #    server.login("admin@gmail.com", "admin")
        #    server.sendmail(email_sender, userEmail, msg)
        #    server.quit()
        messages.success(request, 'Your account has been created!')
        return redirect('home')

    else:
        return HttpResponse('404 - not found')

def handlelogin(request):
    if request.method == 'POST':
        #Get the post parameters
        loginUserName = request.POST['loginUserName']
        loginPass = request.POST['loginPass']
        user = authenticate(username=loginUserName, password=loginPass)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'username or password is incorrect! Try again')
            return redirect('home')

    return HttpResponse('404 - not found')

def handlelogout(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('home')