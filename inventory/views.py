from rest_framework.views import APIView
from utils.utilities import custom_response, CustomAuth
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import inventory.services as services
import logging

logger = logging.getLogger("django")


class HealthCheck(APIView):
    def get(self, request):
        try:
            logger.info("Server is running")
            return custom_response(
                success=True,
                message="Server running :)",
                status=200,
            )
        except Exception as err:
            logger.error(f"Error in healthCheck: {str(err)}")
            return custom_response(message=str(err))


class RegisterUserView(APIView):
    def post(self, request):
        try:
            services.register_user_service(request.data)
            logger.info(f"User: {request.data["name"]} added successfully")
            return custom_response(
                success=True,
                message="User added successfully",
                status=200,
            )
        except Exception as e:
            logger.error(f"Error in registering user {request.data["name"]}: {str(e)}")
            return custom_response(message=str(e))


class UserLoginView(APIView):
    def post(self, request):
        try:
            email, password = (request.data.get(key) for key in ("email", "password"))
            token = services.user_login_service(email, password)
            logger.info("Successfully logged In")
            return custom_response(
                success=True,
                message="Successfully logged In",
                data=token,
                status=200,
            )
        except Exception as e:
            logger.error(f"Error in user login: {str(e)}")
            return custom_response(message=str(e))


class CreateItemView(APIView):
    permission_classes = [CustomAuth]

    def post(self, request):
        try:
            item_name, description, quantity, category = (
                request.data.get(key)
                for key in (
                    "item_name",
                    "description",
                    "quantity",
                    "category",
                )
            )
            item = services.create_item_service(
                item_name,
                description,
                quantity,
                category,
                request.token_data.get("user_id"),
            )
            logger.info(f"Item: {item_name} added Successfully")
            return custom_response(
                success=True,
                message="Item added Successfully",
                data=item,
                status=200,
            )
        except Exception as e:
            logger.error(f"Error in creating Item {item_name}: {str(e)}")
            return custom_response(message=str(e))


class ItemView(APIView):
    permission_classes = [CustomAuth]

    @method_decorator(cache_page(60 * 15))
    def get(self, request, item_id):
        try:
            item = services.read_item_service(item_id)
            logger.info(f"Item: {item_id} details retrieved successfully")
            return custom_response(
                success=True,
                message="Item details retrieved successfully",
                data=item,
                status=200,
            )
        except Exception as e:
            logger.error(f"Error in reading item {item_id}: {str(e)}")
            return custom_response(message=str(e))

    def put(self, request, item_id):
        try:
            updated_item = services.update_item_service(item_id, request.data)
            logger.info(f"Item: {item_id} details updated successfully")
            return custom_response(
                success=True,
                message="Item details updated successfully",
                data=updated_item,
                status=200,
            )
        except Exception as e:
            logger.error(f"Error in updating item {item_id} details: {str(e)}")
            return custom_response(message=str(e))

    def delete(self, request, item_id):
        try:
            services.delete_item_service(item_id)
            logger.info(f"Item: {item_id} deleted successfully")
            return custom_response(
                success=True,
                message="Item deleted successfully",
                status=200,
            )
        except Exception as e:
            logger.error(f"Error in deleting item {item_id}: {str(e)}")
            return custom_response(message=str(e))
