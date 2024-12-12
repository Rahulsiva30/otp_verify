from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PhoneNumberForm
import random
from twilio.rest import Client
from django.conf import settings

def send_otp(phone_number):
    otp = random.randint(1000, 9999)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f'Your OTP is {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp

def mobile_verification(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            otp = send_otp(phone_number)
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            messages.success(request, f"OTP sent to {phone_number}.")
            return redirect('verify_otp')
    else:
        form = PhoneNumberForm()
    return render(request, 'otp_app/enter_phone_number.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        correct_otp = request.session.get('otp')
        if str(entered_otp) == str(correct_otp):
            messages.success(request, "OTP verified successfully!")
            return redirect('success')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
    return render(request, 'otp_app/verify_otp.html')

def success_page(request):
    return render(request, 'otp_app/success.html')
