from ninja import Router
from ninja.security import django_auth
from .schema import UserSchema, ApiResponseSchema
from typing import List
from users.models import User
from .utils import api_response

router = Router(tags=['users'])




@router.get("/", response=List[UserSchema],auth=django_auth)
def get_all_users(request):
    if request.user.is_superuser:
        users = User.objects.all()

        # users_data = List[UserSchema].from_orm(users)
        users_data = [UserSchema.from_orm(user) for user in users ]


        return api_response(
            success=True,
            message="User fetched successfully.",
            payload=users_data,
            status_code=200
        )
    else:
        return api_response(
            success=False,
            message="Access Denied.",
            error="Only Admins can access all users",
            status_code=403
        )
        

@router.get("/{user_id}", response=UserSchema,auth=django_auth)
def get_user(request, user_id: int):
    if request.user.is_superuser or request.user.id == user_id:
        try:
            # user = get_object_or_404(User, id=id)
            user = User.objects.get(id=user_id)
            user_data = UserSchema.from_orm(user)
            return api_response(
                success=True,
                message="User fetched successfully.",
                payload=user_data.dict(),
                status_code=200
            )
        except User.DoesNotExist:
            return api_response(
                success=False,
                message="User not found.",
                error="No user with this user id exists.",
                status_code=404
            )
        
@router.put("/{user_id}", response={200: UserSchema, 404: str},auth=django_auth)
def update_user(request, user_id: int, payload: UserSchema):
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            if payload.first_name is not None:
                user.first_name = payload.first_name
            if payload.last_name is not None:
                user.last_name = payload.last_name
            if payload.email is not None:
                user.email = payload.email
            if payload.is_superuser is not None:
                user.is_superuser = payload.is_superuser
            if payload.is_verified is not None:
                user.is_verified = payload.is_verified
            user.save()
            user_data = UserSchema.from_orm(user)
            return api_response(
                success=True,
                message="User updated successfully.",
                payload=user_data.dict(),
                status_code=200
            )
        elif user == request.user:
            if payload.first_name is not None:
                user.first_name = payload.first_name
            if payload.last_name is not None:
                user.last_name = payload.last_name
            # TODO: add email verification if user changed their email
            if payload.email is not None:
                user.email = payload.email
            user.save()
            user_data = UserSchema.from_orm(user)
            return api_response(
                success=True,
                message="User updated successfully.",
                payload=user_data.dict(),
                status_code=200
            )
    except User.DoesNotExist:
        return api_response(
                success=False,
                message="User not found.",
                error="No user with this user id exists.",
                status_code=404
            )

@router.delete("/{user_id}", response=ApiResponseSchema,auth=django_auth)
def delete_user(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return api_response(
                success=True,
                message="User deleted successfully.",
                status_code=200
            )
    except User.DoesNotExist:
        return api_response(
                success=False,
                message="User not found.",
                error="No user with this user id exists.",
                status_code=404
            )