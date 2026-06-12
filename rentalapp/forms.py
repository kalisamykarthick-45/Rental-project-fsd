from django import forms
from .models import BikeBooking, LaptopBooking, CameraBooking






# 🏍 BIKE BOOKING FORM

class BikeBookingForm(forms.ModelForm):

    class Meta:
        model = BikeBooking
        exclude = [
            'user',
            'bike',
            'total_price',
            'status',
            'payment_status',
            'created_at',
            'returned_date',
            'security_deposit',   
            'late_fees', 
            'rent_amount', 
            'returned_amount'         
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control','rows':3}),

            'start_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),

            'end_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if end <= start:
                raise forms.ValidationError("End date must be after start date")

        return cleaned_data



# 💻 LAPTOP BOOKING FORM

class LaptopBookingForm(forms.ModelForm):

    class Meta:
        model = LaptopBooking
        exclude = [
            'user',
            'laptop',
            'total_price',
            'status',
            'payment_status',
            'created_at',
            'returned_date',
            'security_deposit',   
            'late_fees',
            'rent_amount',
            'returned_amount'           
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control','rows':3}),

            'start_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),

            'end_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if end <= start:
                raise forms.ValidationError("End date must be after start date")

        return cleaned_data



# 📷 CAMERA BOOKING FORM

class CameraBookingForm(forms.ModelForm):

    class Meta:
        model = CameraBooking
        exclude = [
            'user',
            'camera',
            'total_price',
            'status',
            'payment_status',
            'created_at',
            'returned_date',
            'security_deposit',   
            'late_fees',
            'rent_amount',
            'returned_amount'           
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control','rows':3}),

            'start_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),

            'end_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if end <= start:
                raise forms.ValidationError("End date must be after start date")

        return cleaned_data


  