from django.contrib.auth import authenticate
from inventory.models import User, Items
from inventory.serializers import ItemsSerializer
from utils.utilities import generate_token


def register_user_service(data: dict) -> None:
    """Registers the user into the database

    Args:
        data (dict): contains name, email and password of the user
    """

    if User.objects.filter(email=data["email"]).exists():
        raise Exception(f'The email: {data["email"]} is already registered.')
    user = User.objects.create(**data)
    user.set_password(data["password"])
    user.save()


def user_login_service(email: str, password: str) -> str:
    """Logs the user into the server

    Args:
        email (str): email address of the user
        password (str): password

    Returns:
        str: jwt token for the specific user
    """
    user = authenticate(email=email, password=password)
    if user is not None:
        token = generate_token(user)
        return token
    else:
        raise Exception("Email or password incorrect!")


def create_item_service(
    item_name: str, description: str, quantity: int, category: str, added_by: str
) -> dict:
    """Creates a record for an item in the database

    Args:
        item_name (str): name of the item
        description (str): description of the item
        quantity (int): quantity of the item
        category (str): category the item falls in
        added_by (str): the user id who added the item

    Returns:
        dict: details of the added item
    """
    item = Items.objects.create(
        item_name=item_name,
        description=description,
        quantity=quantity,
        category=category,
        added_by_id=added_by,
    )
    return ItemsSerializer(item).data


def read_item_service(item_id: str) -> dict:
    """Gets the details of the item

    Args:
        item_id (str): Id of the item

    Returns:
        dict: details of the item
    """
    item = Items.objects.get(id=item_id)
    return ItemsSerializer(item).data


def update_item_service(item_id: str, updated_data: dict) -> dict:
    """Updates the metadata of the item

    Args:
        item_id (str): id of the item
        updated_data (dict): the keys to be updated under that item

    Returns:
        dict: Details of the updated item
    """
    Items.objects.filter(id=item_id).update(**updated_data)
    updated_item = Items.objects.get(id=item_id)
    return ItemsSerializer(updated_item).data


def delete_item_service(item_id: str) -> None:
    """Deletes an item from the database

    Args:
        item_id (str): id of the item
    """
    Items.objects.get(id=item_id).delete()
