from ninja import Router
from .schema import UserSchema, ApiResponseSchema
from typing import List
from users.models import User
from .utils import api_response
from .auth import CustomJWTAuth


# ============================
# User Management Endpoints
# ============================
router = Router(tags=['users'])


@router.get("/", response=List[UserSchema],auth=CustomJWTAuth())
def get_all_users(request):
    """
    Retrieve all users from the database. Only accessible by superusers.

    Args:
        request: The HTTP request object.

    Returns:
        ApiResponseSchema: A schema containing a list of users and a success message.
    """
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


@router.get("/{user_id}", response=UserSchema,auth=CustomJWTAuth())
def get_user(request, user_id: int):
    """
    Retrieve a specific user by their ID. Accessible by superusers or the user themselves.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user to retrieve.

    Returns:
        ApiResponseSchema: A schema containing user details and a success message.
        ApiResponseSchema: A schema indicating failure if the user is not found.
    """
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

@router.put("/{user_id}", response={200: UserSchema, 404: str},auth=CustomJWTAuth())
def update_user(request, user_id: int, payload: UserSchema):
    """
    Update user details for a specific user. Only the user themselves or superusers can perform updates.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user to update.
        payload (UserSchema): The data to update for the user.

    Returns:
        ApiResponseSchema: A schema containing updated user details and a success message.
        ApiResponseSchema: A schema indicating failure if the user is not found or update fails.
    """
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

@router.delete("/{user_id}", response=ApiResponseSchema,auth=CustomJWTAuth())
def delete_user(request, user_id: int):
    """
    Delete a specific user by their ID. Only accessible by superusers or user themselves.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user to delete.

    Returns:
        ApiResponseSchema: A schema indicating success or failure of the delete operation.
    """
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser or user == request.user:
            user.delete()
            return api_response(
                success=True,
                message="User deleted successfully.",
                status_code=200
            )
        else:
            return api_response(
                success=False,
                message="You don't have the premission to delete this user.",
                status_code=403
            )
    except User.DoesNotExist:
        return api_response(
                success=False,
                message="User not found.",
                error="No user with this user id exists.",
                status_code=404
            )
