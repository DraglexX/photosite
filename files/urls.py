from django.urls import path
from files import views

urlpatterns = [
    path('album/<int:alb_id>', views.album),
    path('album/<int:alb_id>/edit', views.edit_album),
    path('album/<int:alb_id>/delete', views.delete_album),
    path('album/<int:alb_id>/upload/', views.image_upload_view),
    path('album/<int:alb_id>/image/<int:img_id>/edit', views.edit_image),
    path('album/<int:alb_id>/image/<int:img_id>/delete', views.delete_image),
    path('post/', views.post),
    path('', views.home),
    path('register/', views.RegisterFormView.as_view()),
    path('login/', views.LoginFormView.as_view()),
    path('logout/', views.LogoutView.as_view())
]
