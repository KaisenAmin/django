# from django.core.mail import send_mail
# from .models import User
# from django.contrib.auth.hashers import check_password, make_password
# from django.conf import settings
# from django.contrib.auth import authenticate, logout, get_user_model, authenticate, login
# from django.http import JsonResponse, HttpResponseBadRequest
# from datetime import datetime, timedelta
# import jwt
# from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# from sqlalchemy import create_engine, exc
# from app.models import User
# from app.database import get_session
# from django.http import JsonResponse
# from django.views import View
# import random
# import string
# from django.db.models import Q
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi


# class RegisterAPIView(View):
#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['username', 'phone_number', 'first_name', 'last_name'],
#             properties={
#                 'username': openapi.Schema(type=openapi.TYPE_STRING),
#                 'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
#                 'first_name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'last_name': openapi.Schema(type=openapi.TYPE_STRING),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING),
#                 'email_address': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         responses={
#             201: 'Registration successful',
#             400: 'Bad request',
#             500: 'Error occurred while saving user',
#         },
#     )
#     def post(self, request):
#         data = request.data

#         # Validate required fields
#         required_fields = ['username',
#                            'phone_number', 'first_name', 'last_name']
#         missing_fields = [
#             field for field in required_fields if field not in data]
#         if missing_fields:
#             return JsonResponse(
#                 {"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

#         # Validate unique username
#         session = get_session()
#         if session.query(User).filter_by(username=data['username']).first():
#             return JsonResponse({"error": "Username is already taken"}, status=400)

#         if session.query(User).filter_by(username=data['phone_number']).first():
#             return JsonResponse({"error": "Phone number is already taken"}, status=400)

#         if session.query(User).filter_by(username=data['email_address']).first():
#             return JsonResponse({"error": "Email address is already taken"}, status=400)

#         # Generate a random verification code
#         verification_code = ''.join(random.choices(string.digits, k=6))

#         # TODO Verify phone number via SMS (implement your verification logic here)
#         # TODO Send the verification code to the user's phone number
#         print("verification_code: ", verification_code)

#         # Create a new user
#         hashed_password = make_password(data['password'])
#         new_user = User(
#             username=data['username'],
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             phone_number=data['phone_number'],
#             password=hashed_password,
#             phone_verified=False,
#             phone_verification_code=verification_code
#         )
#         session.add(new_user)

#         try:
#             session.commit()
#             return JsonResponse({"message": "Registration successful"}, status=201)
#         except exc.SQLAlchemyError:
#             session.rollback()
#             return JsonResponse({"error": "Error occurred while saving user"}, status=500)
#         finally:
#             session.close()


# class VerifyPhoneAPIView(View):
#     def post(self, request):
#         data = request.POST

#         # Retrieve the verification code and phone number from the request data
#         verification_code = data.get('verification_code')
#         phone_number = data.get('phone_number')

#         # Perform necessary checks and verification
#         if not verification_code or not phone_number:
#             return JsonResponse({'error': 'Verification code and phone number are required'}, status=400)

#         try:
#             user = User.objects.get(phone_number=phone_number)
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)

#         if user.phone_verified:
#             return JsonResponse({'message': 'Phone number already verified'}, status=200)

#         if user.phone_verification_code != verification_code:
#             return JsonResponse({'error': 'Invalid verification code'}, status=400)

#         # Update the user's phone_verified field to True
#         user.phone_verified = True
#         user.save()

#         return JsonResponse({'message': 'Phone number verified successfully'}, status=200)


# class OTPRequestAPIView(View):
#     def post(self, request):
#         data = request.data

#         # Validate required fields
#         required_fields = ['username', 'method']
#         missing_fields = [
#             field for field in required_fields if field not in data]
#         if missing_fields:
#             return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

#         # Validate username
#         try:
#             user = User.objects.get(username=data['username'])
#         except User.DoesNotExist:
#             return JsonResponse({"error": "User does not exist"}, status=404)

#         # Generate a new OTP
#         otp = ''.join(random.choices(string.digits, k=6))

#         # Update user's OTP based on the selected method
#         if data['method'] == 'sms':
#             # TODO: Send OTP via SMS (implement your SMS sending logic here)
#             print(f"Sending OTP to {user.phone_number}: {otp}")
#         elif data['method'] == 'email':
#             # TODO: Send OTP via Email (implement your email sending logic here)
#             subject = 'OTP Request'
#             message = f'Your OTP: {otp}'
#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [user.email_address]
#             send_mail(subject, message, from_email, recipient_list)
#         else:
#             return JsonResponse({"error": "Invalid method"}, status=400)

#         # Update user's OTP field in the database
#         user.otp = otp
#         user.save()

#         return JsonResponse({"message": "OTP request successful"})


# class LoginAPIView(View):
#     def post(self, request):
#         data = request.data

#         # Retrieve the username/phone number and password from the request data
#         username_or_phone = data.get('username_or_phone')
#         password = data.get('password')
#         otp = data.get('otp')

#         # Perform necessary checks
#         if not username_or_phone or not password or not otp:
#             return JsonResponse({"error": "Username/Phone number, password, and OTP are required"}, status=400)

#         # Retrieve the user from the database by username or phone number
#         try:
#             user = User.objects.get(username=username_or_phone)
#         except User.DoesNotExist:
#             try:
#                 user = User.objects.get(phone_number=username_or_phone)
#             except User.DoesNotExist:
#                 return JsonResponse({"error": "Invalid username/phone number or password"}, status=401)

#         if user.locked:
#             return JsonResponse({"error": "account is locked"}, status=401)

#         authenticated = False

#         # Verify the provided password with the hashed password in the database
#         if password != None:
#             if not check_password(password, user.password):
#                 return JsonResponse({"error": "Invalid username/phone number or password"}, status=401)
#             else:
#                 authenticated = True

#         # Verify the provided OTP
#         if not authenticated and otp != None and user.otp != None:
#             if otp != user.otp:
#                 return JsonResponse({"error": "Invalid OTP"}, status=401)
#             else:
#                 authenticated = True
#                 user.otp = None  # it is one time password ;)
#                 user.save()

#         if not authenticated:
#             return JsonResponse({"error": "not authenticated"}, status=401)

#         # Generate JWT token
#         token = self.generate_jwt_token(user)

#         # Return the JWT token in the response
#         return JsonResponse({"token": token}, status=200)

#     def generate_jwt_token(self, user):
#         # Define the payload for the JWT token
#         payload = {
#             'user_id': user.id,
#             'username': user.username,
#             # Token expiration time (e.g., 7 days)
#             'exp': datetime.utcnow() + timedelta(days=7)
#         }

#         # Read the secret key from settings.py
#         secret_key = settings.SECRET_KEY

#         # Generate the JWT token
#         token = jwt.encode(payload, secret_key,
#                            algorithm='HS256').decode('utf-8')

#         return token


# class LogoutAPIView(View):
#     def post(self, request):
#         logout(request)
#         return JsonResponse({"message": "Logout successful"})


# class PasswordResetViaSMSAPIView(View):
#     def post(self, request):
#         data = request.data

#         # Validate required fields
#         required_fields = ['phone_number']
#         missing_fields = [
#             field for field in required_fields if field not in data]
#         if missing_fields:
#             return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

#         try:
#             user = User.objects.get(phone_number=data['phone_number'])
#         except User.DoesNotExist:
#             return JsonResponse({"error": "User does not exist"}, status=404)

#         # Generate a new OTP
#         otp = ''.join(random.choices(string.digits, k=6))

#         # TODO: Send OTP via SMS (implement your SMS sending logic here)
#         print(f"Sending OTP to {user.phone_number}: {otp}")

#         # Update user's OTP field in the database
#         user.otp = otp
#         user.save()

#         return JsonResponse({"message": "OTP sent successfully"})


# class PasswordResetViaEmailAPIView(View):
#     def post(self, request):
#         data = request.data

#         # Validate required fields
#         required_fields = ['email_address']
#         missing_fields = [
#             field for field in required_fields if field not in data]
#         if missing_fields:
#             return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

#         try:
#             user = User.objects.get(email_address=data['email_address'])
#         except User.DoesNotExist:
#             return JsonResponse({"error": "User does not exist"}, status=404)

#         # Generate a new OTP
#         otp = ''.join(random.choices(string.digits, k=6))

#         # TODO: Send OTP via Email (implement your email sending logic here)
#         subject = 'Password Reset OTP'
#         message = f'Your OTP: {otp}'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [user.email_address]
#         send_mail(subject, message, from_email, recipient_list)

#         # Update user's OTP field in the database
#         user.otp = otp
#         user.save()

#         return JsonResponse({"message": "OTP sent successfully"})


# class PasswordResetConfirmAPIView(View):
#     def post(self, request):
#         data = request.data

#         # Validate required fields
#         required_fields = ['identifier', 'otp', 'new_password']
#         missing_fields = [
#             field for field in required_fields if field not in data]
#         if missing_fields:
#             return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

#         # Find the user by username, email, or phone number
#         try:
#             user = User.objects.get(Q(username=data['identifier']) | Q(
#                 email_address=data['identifier']) | Q(phone_number=data['identifier']))
#         except User.DoesNotExist:
#             return JsonResponse({"error": "User does not exist"}, status=404)

#         if data['otp'] != user.otp:
#             return JsonResponse({"error": "Invalid OTP"}, status=400)

#         # Set the new password for the user
#         user.password = make_password(data['new_password'])
#         user.otp = None  # Empty the OTP field
#         user.save()

#         return JsonResponse({"message": "Password reset successful"})
