from ninja import Router
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from .utils import api_response
from .schema import (
    ApiResponseSchema,
    SignInSchema,
    ChangePasswordSchema,
    PasswordResetRequestSchema,
    PasswordResetConfirmSchema,
    EmailVerificationSchema,
)
from .auth import CustomJWTAuth
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

router = Router(tags=['auth'])


@router.get("/set-csrf-token", response=ApiResponseSchema)
def get_csrf_token(request):
    return api_response(
        success=True,
        message="csrf fetched successfully.",
        payload={"csrftoken": get_token(request)},
        status_code=200
    )

@router.post("/login", response=ApiResponseSchema)
def login_view(request, payload: SignInSchema):
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None:
        login(request, user)
        return api_response(
            success=True,
            message="You are logged in.",
            payload=None,
            status_code=200
        )
    return api_response(
        success=False,
        message="Invalid credentials.",
        payload=None,
        status_code=401
    )

@router.post("/logout",response=ApiResponseSchema, auth=CustomJWTAuth())
def logout_view(request):
    logout(request)
    return api_response(
        success=True,
        message="You are logged out.",
        payload=None,
        status_code=200
    )


@router.post("/register", response=ApiResponseSchema)
def register(request, payload: SignInSchema):
    try:
        # Create the user
        user = User.objects.create_user(username=payload.email, email=payload.email, password=payload.password)
        user.is_active = False  # Mark the user as inactive until email verification
        user.save()

        # Generate email verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct the email verification URL
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

        # Send verification email
        send_mail(
            subject="Email Verification",
            message=f"Click the link to verify your email: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return api_response(
            success=True,
            message="User registered successfully. Please check your email to verify your account.",
            payload=None,
            status_code=200
        )
    except Exception as e:
        return api_response(
            success=False,
            message=str(e),
            payload=None,
            status_code=503
        )
    
@router.post("/verify-email", response=ApiResponseSchema)
def verify_email(request, payload: EmailVerificationSchema):
    try:
        # Decode the user ID from the uid
        user_id = force_str(urlsafe_base64_decode(payload.user_id))
        user = User.objects.get(pk=user_id)

        # Verify the token
        if not default_token_generator.check_token(user, payload.token):
            return {"success": False, "message": "Invalid token"}

        # Activate the user's account
        user.is_active = True
        user.save()

        return api_response(
            success=True,
            message="Email verified successfully.",
            payload=None,
            status_code=200
        )
    except User.DoesNotExist:
        return api_response(
            success=False,
            message="User not found.",
            payload=None,
            status_code=404
        )
    except Exception as e:
        return api_response(
            success=False,
            message=str(e),
            payload=None,
            status_code=503
        )
    
@router.post("/change-password", response=ApiResponseSchema, auth=CustomJWTAuth())
def change_password(request, data: ChangePasswordSchema):
    user = request.user

    # Check if current password is correct
    if not user.check_password(data.current_password):
        return api_response(
            success=False,
            message="Current password is incorrect.",
            payload=None,
            status_code=401
        )

    # Check if new passwords match
    if data.new_password != data.confirm_new_password:
        return api_response(
            success=False,
            message="New passwords do not match.",
            payload=None,
            status_code=401
        )


    # Validate the new password (using Django's built-in validators)
    try:
        validate_password(data.new_password, user=user)
    except ValidationError as e:
        return api_response(
            success=False,
            message=str(e),
            payload=None,
            status_code=403
        )
    # Change the user's password
    user.set_password(data.new_password)
    user.save()

    return api_response(
        success=True,
        message="Password changed successfully.",
        payload=None,
        status_code=200
    )


@router.post("/reset-password", response=ApiResponseSchema)
def request_password_reset(request, data: PasswordResetRequestSchema):
    try:
        user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        return api_response(
            success=False,
            message="User with this email does not exist.",
            payload=None,
            status_code=404
        )
    # Generate token
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk))  # Encode the user's ID

    # Construct the password reset URL
    password_reset_url = f"{settings.FRONTEND_URL}/reset-password-confirm/{user_id}/{token}/"

    # Send email with the reset URL
    send_mail(
        subject="Password Reset",
        message=f"Click the link to reset your password: {password_reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return api_response(
        success=True,
        message="Password reset link has been sent to your email.",
        payload=None,
        status_code=200
    )

@router.post("/reset-password-confirm", response=ApiResponseSchema)
def password_reset_confirm(request, data: PasswordResetConfirmSchema):
    # Decode the user ID from the uid
    try:
        user_id = force_str(urlsafe_base64_decode(data.user_id))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return api_response(
            success=False,
            message="Invalid user.",
            payload=None,
            status_code=401
        )

    # Verify the token
    if not default_token_generator.check_token(user, data.token):
        return api_response(
            success=False,
            message="Token is either invalid or has expired.",
            payload=None,
            status_code=403
        )
    # Check if the passwords match
    if data.new_password != data.confirm_new_password:
        return api_response(
            success=False,
            message="Passwords do not match.",
            payload=None,
            status_code=401
        )
    # Validate the new password (using Django's validators)
    try:
        validate_password(data.new_password, user=user)
    except ValidationError as e:
        return api_response(
            success=False,
            message=str(e),
            payload=None,
            status_code=403
        )
    # Set the new password
    user.set_password(data.new_password)
    user.save()

    return api_response(
        success=True,
        message="Password has been reset successfully.",
        payload=None,
        status_code=200
    )