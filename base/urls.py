from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('network/', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('network/profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('contact/', views.contactPage, name="contact"),

    path('tutorials/', views.tutorialsPage, name="tutorials"),
    path('like-tutorial/<str:pk>/', views.like_tutorial, name="like-tutorial"),
    path('terms/', views.termsPage, name="terms"),
    path('shop/', views.shopPage, name="shop"),
    path('shop/team/<str:team_id>/', views.team_shop, name="team-shop"),
    path('shop/team/<str:team_id>/product/<str:product_id>/', views.product_detail, name="product-detail"),
    
    path('join-team/', views.join_team, name='join-team'),
    path('profile/', views.fullProfile, name='profile'),
    path('profile/<str:pk>/', views.fullProfile, name='view-profile'),
    path('edit-profile/', views.edit_profile, name="edit-profile"),

    path('manage-competitions/', views.manage_competitions, name='manage-competitions'),
    path('edit-competition/<str:pk>/', views.edit_competition, name='edit-competition'),
    path('delete-competition/<str:pk>/', views.delete_competition, name='delete-competition'),
    path('get-competition/<str:pk>/', views.get_competition, name='get-competition'),
]