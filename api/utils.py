from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    """
    Handles and formats common API responses for consistency and readability.
    """
    def __init__(self, resource: str, action: str, additional_message: str = None, data: dict = None):
        """
        Initializes a `CustomResponse` instance.

        Args:
            resource (str): The type of resource involved in the action (e.g., "invoice", "invoice detail").
            action (str): The action performed on the resource (e.g., "creation", "updation", "deletion").
            additional_message (str, optional): An optional additional message to include in the response.
            data (dict, optional): A dictionary of data to include in the response. Defaults to an empty dictionary.
        """
        self.resource = resource
        self.action = action
        self.additional_message = additional_message
        self.data = data or {}

    def generate_response(self, error: bool, general_message: str, status_code: status) -> Response:
        """
        Generates a response dictionary based on provided arguments.

        Args:
            error (bool): Indicates whether the response is an error response.
            general_message (str): The main message for the response.
            status_code (status): The HTTP status code for the response.

        Returns:
            Response: A Django REST framework Response object.
        """
        self.error = error
        self.status_code = status_code
        self.message = {
            "general_message": general_message,
            "additional_message": self.additional_message
        } if self.additional_message else general_message

        return Response({
            "error": self.error,
            "resource": self.resource,
            "action": self.action,
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code
        }, status=self.status_code)

    def success_response(self, message: str = None):
        """
        Returns a successful response with a default message based on the action and resource.
        The message can be overridden with a custom message.
        """
        return self.generate_response(
            error=False, 
            general_message=f"Successful {self.action} of {self.resource} object(s)" if not message else message,
            status_code=status.HTTP_200_OK
            )

    def created_response(self, message: str = None):
        """
        Returns a created response with a default message indicating successful resource creation.
        The message can be overridden with a custom message.
        """
        return self.generate_response(
            error=False, 
            general_message=f"Successfully created new object" if not message else message,
            status_code=status.HTTP_201_CREATED
            )

    def failure_response(self, message: str = None):
        """
        Returns a failure response with a default message based on the action and resource,
        The message can be overridden with a custom message.

        Args:
            additional_message (str, optional): An additional message to include in the response.

        Returns:
            Response: A failure Django REST framework Response object.
        """
        return self.generate_response(
            error=True, 
            general_message=f"Failure in {self.action} of object" if not message else message,
            status_code=status.HTTP_400_BAD_REQUEST
            )

    def not_found_response(self, message: str = None):
        """
        Returns a not found response with a default message indicating the resource was not found.
        The message can be overridden with a custom message.
        """
        return self.generate_response(
            error=True, 
            general_message=f"{self.resource} object not found" if not message else message, 
            status_code=status.HTTP_404_NOT_FOUND
            )