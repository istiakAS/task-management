from django.urls import path
from users.views import admin_dashboard, group_list, sign_up, sign_in, sign_out, assign_role, create_group, CustomLoginView, ProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView, EditProfileView
from users.views import activate_user
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView



urlpatterns = [
    path('sign_up/', sign_up, name='sign-up'),
    # path('sign_in/', sign_in, name='sign_in'),
    path('sign_in/', CustomLoginView.as_view(), name='sign_in'),
    # path('sign_out/', sign_out, name='logout'),
    path('sign_out/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign_role/', assign_role, name='assign-role'),
    path('admin/create_group/', create_group, name='create-group'),
    path('admin/group_list/', group_list, name='group_list'),
    path('profile/', ProfileView.as_view(template_name='accounts/profile.html'), name='profile'),
    path('password-change/', ChangePassword.as_view(), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reseet/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')
]
