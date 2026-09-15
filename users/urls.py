from django.urls import path
from users.views import sign_up, sign_in, sign_out
from users.views import activate_user


urlpatterns = [
    path('sign_up/', sign_up, name='sign-up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),
]
