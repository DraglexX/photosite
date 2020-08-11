from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from files.models import Album, Image
from .forms import ImageForm
from django.core.paginator import Paginator


def image_upload_view(request, alb_id):
    try:
        album = Album.objects.get(id=alb_id)
    except Album.DoesNotExist:
        return redirect('/')
    if request.user.is_authenticated and request.user.username == album.author:
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/album/' + str(alb_id))
        else:
            form = ImageForm()
            return render(request, 'upload.html', {'form': form, 'album': album, 'alb_id': alb_id})

    else:
        return redirect('/')


def post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            author = request.POST.get('author')
            Album.objects.create(
                title=title,
                description=description,
                author=author
            )
            return redirect('/')
        return render(request, 'post.html')
    else:
        return redirect('/')


def edit_image(request, img_id, alb_id):
    try:
        album = Album.objects.get(id=alb_id)
        image = Image.objects.get(id=img_id)
    except Image.DoesNotExist:
        return redirect('/')
    if request.user.username == album.author:
        if request.method == "POST":
            image.title = request.POST.get('title')
            image.save()
            return redirect('/album/' + str(alb_id))
        else:
            return render(request, "edit_image.html", {'image': image, 'album': album})
    else:
        return redirect('/')
    return render(request, 'edit_image.html')


def edit_album(request, alb_id):
    try:
        album = Album.objects.get(id=alb_id)
    except Album.DoesNotExist:
        return redirect('/')
    if request.user.username == album.author:
        if request.method == "POST":
            album.title = request.POST.get('title')
            album.description = request.POST.get('description')
            album.save()
            return redirect('/album/' + str(alb_id))
        else:
            return render(request, "edit_album.html", {"album": album})
    else:
        return redirect('/')
    return render(request, 'edit_album.html')


def delete_album(request, alb_id):
    try:
        album = Album.objects.get(id=alb_id)
        if request.user.username == album.author:
            album.delete()
            return redirect('/')
        else:
            return redirect('/')
    except Album.DoesNotExist:
        return redirect('/')


def delete_image(request, img_id, alb_id):
    try:
        album = Album.objects.get(id=alb_id)
        image = Image.objects.get(id=img_id)
    except Album.DoesNotExist:
        return redirect('/')
    if request.user.username == album.author:
        image.delete()
        return redirect('/album/' + str(alb_id))
    else:
        return redirect('/')


def album(request, alb_id):
    try:
        album = Album.objects.get(id=alb_id)
    except Album.DoesNotExist:
        return redirect('/')

    images = Image.objects.filter(album_id=alb_id)
    paginator = Paginator(images, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    return render(request, 'album.html', context={
        'album': album,
        'images': page,
        'alb_id': alb_id,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    })


def home(request):
    albums = Album.objects.all()
    return render(request, 'index.html', {
        'albums': albums
    })


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
