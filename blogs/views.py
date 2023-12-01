import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author, Blog
from .serializers import BlogSerializer
from django.shortcuts import render, HttpResponse, redirect, loader
from django.views.decorators.csrf import csrf_exempt

def homepage(request):
    if 'Username' in request.session.keys():
        context = { 'username' : request.session['Username']}
        template = loader.get_template('homePage.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/signin')
    
def signin(request):
    if request.method == "GET":
        if 'Username' in request.session.keys():
            return redirect('/')
        else:
            return render(request, "signin.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            author = Author.objects.get(Username=username, Password=password)
            request.session['Username'] = author.Username
            template = loader.get_template('homePage.html')
            context = { 'username' : request.session['Username']}
            return HttpResponse(template.render(context, request))
        
        
        except:
            template = loader.get_template('signin.html')
            context={'error_message': 'Unmatch user data'}
            return HttpResponse(template.render(context, request))

@csrf_exempt
def register(request):
    if request.method == "GET":
        template = loader.get_template('register.html')
        return HttpResponse(template.render())
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        surname = request.POST['surname']

        if len(Author.objects.filter(Username=username)) > 0:
            template = loader.get_template('register.html')
            error_message = "Username already exists"
            return HttpResponse(template.render({'error_message': error_message},request))

        new_author = Author(Username=username, Password=password,
                       Name=name, Surname=surname)
        new_author.save()
        
        return redirect('/signin')

def logout(request):
    if 'Username' in request.session.keys():
        del request.session['Username']
        request.session.modified = True
        return redirect('/signin')
    else:
        pass

@api_view(["GET", "POST"])
def blogs(request):
    if request.method == "GET":
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({"blogs": serializer.data})
    
    elif request.method == 'POST':
        blog_data = request.data
        author_username = request.session.get('Username')

        try:
            author = Author.objects.get(Username=author_username)
            blog_data['Author'] = author.id
            blog_data['Date'] = datetime.date.today()
            serializer = BlogSerializer(data=blog_data)

        except Author.DoesNotExist:
            return Response({'detail': 'Signed-in author not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PATCH", "DELETE"])
def blogId(request, id):
    try:
        blog_id = Blog.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BlogSerializer(blog_id)
        return Response(serializer.data)

    elif request.method == "PATCH":
        author = Author.objects.get(Username=request.session['Username'])
        if blog_id.Author == author.id:
            serializer = BlogSerializer(blog_id, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Not authorized, cant make an update"})

    elif request.method == "DELETE":
        author = Author.objects.get(Username=request.session['Username'])
        if blog_id.Author == author.id:
            blog_id.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response({"error": "Not authorized, cant delete"})
            
