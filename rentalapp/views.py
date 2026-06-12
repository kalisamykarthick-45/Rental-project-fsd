from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from datetime import date, datetime
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render
import matplotlib.pyplot as plt
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from .models import Bike, Laptop, Camera
from .models import BikeBooking, LaptopBooking, CameraBooking
from .forms import BikeBookingForm, LaptopBookingForm, CameraBookingForm
import os
import matplotlib
matplotlib.use('Agg')
from collections import defaultdict
from itertools import chain
from django.contrib.auth.decorators import user_passes_test
from itertools import chain
import matplotlib.pyplot as plt
from .models import Contact







#  HOME 
def home(request):  
    return render(request, 'home.html')


#  REGISTER 

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

       

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, "Registered Successfully! Please login")
        return redirect('login')

   
    return render(request, 'register.html')


#  LOGIN 

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')

            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


#  LOGOUT 

def user_logout(request):
    logout(request)
    return redirect('login')

#  PRODUCT LIST 

def bike_list(request):
    bikes = Bike.objects.filter(available=True)
    return render(request, 'bike.html', {'products': bikes})


def laptop_list(request):
    laptops = Laptop.objects.filter(available=True)
    return render(request, 'laptop.html', {'products': laptops})


def camera_list(request):
    cameras = Camera.objects.filter(available=True)
    return render(request, 'camera.html', {'products': cameras})





# BOOK BIKE

@login_required
def book_bike(request, id):
    bike = get_object_or_404(Bike, id=id)

    if request.method == "POST":
        form = BikeBookingForm(request.POST, request.FILES)

        if form.is_valid():
            booking = form.save(commit=False)

           
            booking.security_deposit = 1500

            booking.user = request.user
            booking.bike = bike
            booking.status = "Pending"

           
            if booking.end_date < booking.start_date:
                messages.error(request, "End date must be after start date!")
                return redirect(request.path)

            
            

            
            booking.save()

           
            bike.available = False
            bike.save()

            return redirect('payment', type='bike', booking_id=booking.id)

        else:
            print("FORM ERROR:", form.errors)
            messages.error(request, "Form invalid! Check inputs")

    else:
        form = BikeBookingForm()

    return render(request, 'booking_form.html', {'form': form, 'item': bike})

# BOOK LAPTOP

@login_required
def book_laptop(request, id):
    laptop = get_object_or_404(Laptop, id=id)

    if request.method == "POST":
        form = LaptopBookingForm(request.POST, request.FILES)

        if form.is_valid():
            booking = form.save(commit=False)

           
            booking.security_deposit = 2000

            booking.user = request.user
            booking.laptop = laptop
            booking.status = "Pending"

           
            if booking.end_date < booking.start_date:
                messages.error(request, "End date must be after start date!")
                return redirect(request.path)

           
            

         
            booking.save()

           
            laptop.available = False
            laptop.save()

            return redirect('payment', type='laptop', booking_id=booking.id)

        else:
            print("FORM ERROR:", form.errors)
            messages.error(request, "Form invalid!")

    else:
        form = LaptopBookingForm()

    return render(request, 'booking_form.html', {'form': form, 'item': laptop})


# BOOK CAMERA


@login_required
def book_camera(request, id):
    camera = get_object_or_404(Camera, id=id)

    if request.method == "POST":
        form = CameraBookingForm(request.POST, request.FILES)

        if form.is_valid():
            booking = form.save(commit=False)

           
            booking.security_deposit = 2500

            booking.user = request.user
            booking.camera = camera
            booking.status = "Pending"

           
            if booking.end_date < booking.start_date:
                messages.error(request, "End date must be after start date!")
                return redirect(request.path)

           
            

         
            booking.save()

          
            camera.available = False
            camera.save()

            return redirect('payment', type='camera', booking_id=booking.id)

        else:
            print("FORM ERROR:", form.errors)
            messages.error(request, "Form invalid!")

    else:
        form = CameraBookingForm()

    return render(request, 'booking_form.html', {'form': form, 'item': camera})

#  USER BOOKINGS 

@login_required
def my_bookings(request):

    if request.user.is_staff:
        bike_bookings = BikeBooking.objects.all()
        laptop_bookings = LaptopBooking.objects.all()
        camera_bookings = CameraBooking.objects.all()
    else:
        bike_bookings = BikeBooking.objects.filter(user=request.user)
        laptop_bookings = LaptopBooking.objects.filter(user=request.user)
        camera_bookings = CameraBooking.objects.filter(user=request.user)

    return render(request, "my_bookings.html", {
        "bike_bookings": bike_bookings,
        "laptop_bookings": laptop_bookings,
        "camera_bookings": camera_bookings
    })



@staff_member_required
def update_status(request, item_type, id, action):

    if item_type == "bike":
        booking = get_object_or_404(BikeBooking, id=id)
        item = booking.bike

    elif item_type == "laptop":
        booking = get_object_or_404(LaptopBooking, id=id)
        item = booking.laptop

    elif item_type == "camera":
        booking = get_object_or_404(CameraBooking, id=id)
        item = booking.camera

    else:
        messages.error(request, "Invalid type")
        return redirect('admin_dashboard')

    if action == "return":
        booking.status = "Returned"
        booking.returned_date = date.today()
        item.available = True

    elif action == "reject":
        booking.status = "Rejected"

    booking.save()
    item.save()

    return redirect('admin_dashboard')



@login_required
def payment_view(request, type, booking_id):

    if type == "bike":
        booking = get_object_or_404(BikeBooking, id=booking_id, user=request.user)

    elif type == "laptop":
        booking = get_object_or_404(LaptopBooking, id=booking_id, user=request.user)

    elif type == "camera":
        booking = get_object_or_404(CameraBooking, id=booking_id, user=request.user)

    else:
        messages.error(request, "Invalid booking ❌")
        return redirect('home')

    if request.method == "POST":
        method = request.POST.get('payment')
        screenshot = request.FILES.get('payment_proof')

        booking.payment_method = method

        
        if screenshot:
            booking.payment_proof = screenshot

        
        booking.payment_status = "Pending"
        booking.status = "Pending"

        booking.save()

        messages.success(request, "Payment Submitted. Waiting for admin approval ✅")
        return redirect('my_bookings')

    return render(request, 'payment.html', {'booking': booking})


@staff_member_required
def verify_payment(request, type, id):

    if type == "bike":
        booking = BikeBooking.objects.get(id=id)
    elif type == "laptop":
        booking = LaptopBooking.objects.get(id=id)
    else:
        booking = CameraBooking.objects.get(id=id)

    booking.status = "Approved"
    booking.payment_status = "Paid"
    booking.save()

    return redirect('admin_dashboard')




@login_required
def profile(request):
    user = request.user

    context = {
        'user': user,
        'is_admin': user.is_staff   
    }

    return render(request, 'profile.html', context)





@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()

    bike_revenue = BikeBooking.objects.filter(
        payment_status="Paid",
        status__in=["Approved", "Returned"]
    ).aggregate(total=Sum('total_price'))['total'] or 0

    laptop_revenue = LaptopBooking.objects.filter(
        payment_status="Paid",
        status__in=["Approved", "Returned"]
    ).aggregate(total=Sum('total_price'))['total'] or 0

    camera_revenue = CameraBooking.objects.filter(
        payment_status="Paid",
        status__in=["Approved", "Returned"]
    ).aggregate(total=Sum('total_price'))['total'] or 0

    total_revenue = bike_revenue + laptop_revenue + camera_revenue

    active_rentals = (
        BikeBooking.objects.filter(status="Approved").count() +
        LaptopBooking.objects.filter(status="Approved").count() +
        CameraBooking.objects.filter(status="Approved").count()
    )

   
    bike_bookings = BikeBooking.objects.all()
    laptop_bookings = LaptopBooking.objects.all()
    camera_bookings = CameraBooking.objects.all()

    return render(request, "admin_dashboard.html", {
        "total_users": total_users,
        "total_revenue": total_revenue,
        "active_rentals": active_rentals,

     
        "bike_bookings": bike_bookings,
        "laptop_bookings": laptop_bookings,
        "camera_bookings": camera_bookings,
    })




@staff_member_required
def admin_users(request):
    users = User.objects.all().order_by('-id')
    return render(request, "admin_users.html", {"users": users})


@staff_member_required
def admin_active(request):

    bike = BikeBooking.objects.filter(status="Approved")
    laptop = LaptopBooking.objects.filter(status="Approved")
    camera = CameraBooking.objects.filter(status="Approved")

    return render(request, "admin_active.html", {
        "bike": bike,
        "laptop": laptop,
        "camera": camera
    })


def generate_charts(daily, monthly, yearly, bike, laptop, camera):

    charts_path = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_path, exist_ok=True)

    plt.style.use('dark_background')

    # DAILY
    plt.figure()
    plt.plot(list(daily.keys()), list(daily.values()))
    plt.title("Daily Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_path, "daily.png"))
    plt.close()

    # MONTHLY
    plt.figure()
    plt.plot(list(monthly.keys()), list(monthly.values()))
    plt.title("Monthly Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_path, "monthly.png"))
    plt.close()

    # YEARLY
    plt.figure()
    plt.bar(list(yearly.keys()), list(yearly.values()))
    plt.title("Yearly Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_path, "yearly.png"))
    plt.close()

    # PIE
    plt.figure()
    values = [bike, laptop, camera]

    if sum(values) == 0:
        values = [1,1,1]

    plt.pie(values, labels=['Bike','Laptop','Camera'], autopct='%1.1f%%')
    plt.title("Category Split")
    plt.savefig(os.path.join(charts_path, "pie.png"))
    plt.close()

    return {
        "daily_chart": f"{settings.MEDIA_URL}charts/daily.png",
        "monthly_chart": f"{settings.MEDIA_URL}charts/monthly.png",
        "yearly_chart": f"{settings.MEDIA_URL}charts/yearly.png",
        "pie_chart": f"{settings.MEDIA_URL}charts/pie.png",
    }



@staff_member_required
def admin_revenue(request):

    bikes = BikeBooking.objects.filter(
        payment_status="Paid",
        status__in=["Approved", "Returned"]
    )

    laptops = LaptopBooking.objects.filter(
        payment_status="Paid",
        status__in=["Approved", "Returned"]
    )

    cameras = CameraBooking.objects.filter(
        payment_status="Paid",
        status__in=["Approved", "Returned"]
    )

    # 💰 TOTAL
    bike_total = bikes.aggregate(total=Sum('total_price'))['total'] or 0
    laptop_total = laptops.aggregate(total=Sum('total_price'))['total'] or 0
    camera_total = cameras.aggregate(total=Sum('total_price'))['total'] or 0

    total_revenue = bike_total + laptop_total + camera_total

    # 🔥 MERGE
    all_bookings = list(chain(bikes, laptops, cameras))

    daily = defaultdict(int)
    monthly = defaultdict(int)
    yearly = defaultdict(int)

    for b in all_bookings:
        if b.start_date and b.total_price:

            # DAILY
            key_day = b.start_date.strftime("%Y-%m-%d")
            daily[key_day] += float(b.total_price)

            # MONTHLY
            key_month = b.start_date.strftime("%Y-%m")
            monthly[key_month] += float(b.total_price)

            # YEARLY
            key_year = b.start_date.strftime("%Y")
            yearly[key_year] += float(b.total_price)

    # EMPTY FIX
    if not daily:
        daily = {"No Data": 0}
    if not monthly:
        monthly = {"No Data": 0}
    if not yearly:
        yearly = {"No Data": 0}

    charts = generate_charts(
        daily, monthly, yearly,
        float(bike_total), float(laptop_total), float(camera_total)
    )

    return render(request, "admin_revenue.html", {
        "bike_total": bike_total,
        "laptop_total": laptop_total,
        "camera_total": camera_total,
        "total_revenue": total_revenue,

        "bike_bookings": bikes,
        "laptop_bookings": laptops,
        "camera_bookings": cameras,

        **charts
    })








def refund_deposit(request, item_type, id):

    if item_type == "bike":
        booking = BikeBooking.objects.get(id=id)
    elif item_type == "laptop":
        booking = LaptopBooking.objects.get(id=id)
    else:
        booking = CameraBooking.objects.get(id=id)

    damage = 0  

  
    total_deduction = booking.late_fees + damage

    refund = booking.security_deposit - total_deduction
    if refund < 0:
        refund = 0

  
    revenue = booking.rent_amount + booking.late_fees + damage

    booking.returned_amount = refund
    booking.revenue_amount = revenue
    booking.deposit_refunded = True
    booking.status = "Completed"
    booking.save()

    return redirect("admin_dashboard")




def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if not user.is_staff:
        user.delete()
    return redirect('admin_users')



@staff_member_required
def toggle_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    
    user.is_active = not user.is_active
    user.save()

    return redirect('admin_users')



def make_admin(request, id):
    user = get_object_or_404(User, id=id)
    user.is_staff = True
    user.save()
    return redirect('admin_users')


def is_admin(user):
    return user.is_staff





@user_passes_test(is_admin)
def late_fees(request, type, id):

    if type == "bike":
        booking = get_object_or_404(BikeBooking, id=id)

    elif type == "laptop":
        booking = get_object_or_404(LaptopBooking, id=id)

    elif type == "camera":
        booking = get_object_or_404(CameraBooking, id=id)

    else:
        messages.error(request, "Invalid booking type ❌")
        return redirect('admin_dashboard')


    if request.method == "POST":
        late_fee_value = request.POST.get("late_fees")

        if late_fee_value:
            try:
                booking.late_fees = int(late_fee_value)
                booking.save()
                messages.success(request, "Late fee added successfully ✅")
            except ValueError:
                messages.error(request, "Enter valid number ❌")

        return redirect('admin_dashboard')

    return render(request, "late_fees.html", {"booking": booking})



def contact_view(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        category = request.POST.get("category")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            category=category,
            message=message
        )

        messages.success(request, "Message sent successfully ✅")
        return redirect("contact")

    return render(request, "home.html")