from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),

	path('login/', views.loginPage, name="login"),
	#path('register/', views.registerPage, name="register"),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.registerPage, name="logout"),

	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_items/', views.updateItems, name="update_items"),
	path('process_order/', views.processOrder, name="process_order"),


	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
	path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
	path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
	path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
	path('adm-producto/', views.adm_productos, name="adm-producto"),
	path('agregar-producto/', views.agregar_producto, name="agregar-producto"),
	path('admin/listado_usuarios/',views.listUser, name='listado_usuarios'),
	path("admin/users/edit/<pk>" ,views.editUser, name='edit_user'),
	path("admin/users/delete/<pk>",views.deleteUser, name='delete_user'),

	path("admin/users/registerclient",views.registerClient, name='register_client'),
	path("admin/users/registerseller",views.registerSeller, name='register_seller'),
	path("admin/users/registersupplier",views.registerSupplier, name='register_supplier'),
	path("admin/users/registeremployee",views.registerEmployee, name='register_employee'),
]