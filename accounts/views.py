import json
from django.shortcuts import redirect, render
from main.utils import get_template_path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout 
from .models import User , UserProfile
# Create your views here.



@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone')
        password = data.get('password')
        language = request.COOKIES.get('language', 'ar').split('-')[0]
        
        # Check if both phone number and password are provided
        if not phone_number or not password:
            error_message = 'رقم الهاتف وكلمة المرور مطلوبين.' if language == 'ar' else 'Phone number and password are required.'
            return JsonResponse({'error': error_message}, status=400)

        # Find user by phone number
        try:
            user = User.objects.get(phone_number=phone_number)
            print(user)
        except User.DoesNotExist:
            error_message = 'رقم الهاتف أو كلمة المرور غير صحيحة.' if language == 'ar' else 'Invalid phone number or password.'
            return JsonResponse({'error': error_message}, status=400)

        # Authenticate user
        if user.check_password(password):
            # Log the user in
            login(request, user)
            success_message = 'تم تسجيل الدخول بنجاح.' if language == 'ar' else 'User logged in successfully.'
            return JsonResponse({'success': success_message})
        else:
            error_message = 'رقم الهاتف أو كلمة المرور غير صحيحة.' if language == 'ar' else 'Invalid phone number or password.'
            return JsonResponse({'error': error_message}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone')
        password = data.get('password')
        invitation_code = data.get('invitation_code')
        ip_address = request.META.get('REMOTE_ADDR')  # Get the IP address from the request

        # Check if all required fields are provided
        if not phone_number or not password:
            language = request.COOKIES.get('language', 'ar').split('-')[0]
            error_message = 'رقم الهاتف وكلمة المرور مطلوبين.' if language == 'ar' else 'Phone number and password are required.'
            return JsonResponse({'error': error_message}, status=400)
        
        if User.objects.filter(phone_number=phone_number).exists():
            language = request.COOKIES.get('language', 'ar').split('-')[0]
            error_message = 'رقم الهاتف موجود بالفعل.' if language == 'ar' else 'Phone number already exists.'
            return JsonResponse({'error': error_message}, status=400)

        # Create the user
        user = User.objects.create_user(username=phone_number, password=password, phone_number=phone_number)
        user.ip_address = ip_address  # Save the IP address
        user.unhashed_password = password  # Store unhashed password temporarily (not recommended)

        # If invitation code is provided, validate it and assign the user to the inviter
        if invitation_code:
            try:
                invited_user_profile = UserProfile.objects.get(invitation_code=invitation_code)
                user_profile = UserProfile.objects.create(user=user, inviter=invited_user_profile.user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user) # You may choose to handle invalid invitation codes here
        else :
            user_profile = UserProfile.objects.create(user=user)
        user.save()
        # Log the user in
        login(request  , user)

        success_message = 'تم التسجيل بنجاح.'
        return JsonResponse({'success': success_message})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
def login_views(request):
    template = get_template_path(request, 'page-signin-1.html')
    return render(request, template)

def register_views(request):
    template = get_template_path(request, 'page-signup-1.html')
    return render(request, template)

def logout_view(request):
    logout(request)
    return redirect('login')