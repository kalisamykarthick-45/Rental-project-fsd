from django.contrib import admin
from django.urls import path
from rentalapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home_page'),

   

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
    path('bike/', views.bike_list, name='bike'),
    path('laptop/', views.laptop_list, name='laptop'),
    path('camera/', views.camera_list, name='camera'),

    path('book-bike/<int:id>/',views.book_bike,name="book_bike"),
    path('book-laptop/<int:id>/',views.book_laptop,name="book_laptop"),
    path('book-camera/<int:id>/',views.book_camera,name="book_camera"),
    
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    
    path('update/<str:item_type>/<int:id>/<str:action>/', views.update_status, name='update_status'),
    path('payment/<str:type>/<int:booking_id>/', views.payment_view, name='payment'),

    path('profile/', views.profile, name='profile'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/revenue/', views.admin_revenue, name='admin_revenue'),
    path('dashboard/active/', views.admin_active, name='admin_active'),

    path('dashboard/delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('toggle-user/<int:user_id>/', views.toggle_user, name='toggle_user'),
    path('make-admin/<int:user_id>/', views.make_admin, name='make_admin'),

    path('late-fees/<str:type>/<int:id>/', views.late_fees, name='late_fees'),

    path('refund/<str:item_type>/<int:id>/', views.refund_deposit, name='refund_deposit'),
    path('verify-payment/<str:type>/<int:id>/', views.verify_payment, name='verify_payment'),
    path('contact/', views.contact_view, name='contact'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
