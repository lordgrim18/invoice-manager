from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    def __init__(self, resource, action , additional_message=None, data=None):
        self.additional_message = additional_message
        self.resource = resource
        self.action = action
        self.data = data if data else {}

    def generate_response(self, error, general_message, status_code):
        self.error = error
        self.status_code = status_code
        self.message = {
            "general_message": general_message, 
            "additional_message": self.additional_message
            } if self.additional_message else general_message
        
        return Response(
            {
                "error": self.error, 
                "message": self.message, 
                "data": self.data, 
                "status_code": self.status_code
                }, status=self.status_code
            )

    def success_response(self):
        return self.generate_response(
            error=False,
            general_message = "successful {} of {} objects".format(self.action, self.resource),
            status_code=status.HTTP_200_OK,
        )

    def created_response(self):
        return self.generate_response(
            error=False,
            general_message = "successful creation of {} object".format(self.resource),
            status_code=status.HTTP_201_CREATED
            )
    
    def failure_response(self):
        return self.generate_response(
            error=True, 
            general_message="failure in {} of {} object".format(self.action, self.resource),
            status_code=status.HTTP_400_BAD_REQUEST
            )

    def not_found_response(self):
        return self.generate_response(
            error=True, 
            general_message="{} object not found".format(self.resource),
            status_code=status.HTTP_404_NOT_FOUND
            )

