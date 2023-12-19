from django.http import JsonResponse
from rest_framework import renderers, status

RESPONSE_MESSAGE = {
    status.HTTP_200_OK: "Data",
    status.HTTP_201_CREATED: "Created",
    status.HTTP_204_NO_CONTENT: "No Content",
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    status.HTTP_401_UNAUTHORIZED: "Unauthorized",
    status.HTTP_403_FORBIDDEN: "Forbidden",
    status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Found",
    status.HTTP_404_NOT_FOUND: "Not Found",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    status.HTTP_501_NOT_IMPLEMENTED: "Method not Implemented",
}


class CustomRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code

        api_response_message = None

        if isinstance(data, dict):
            api_response_message = data.pop("message", None)

        if data and "response_data" in data:
            data = data.pop("response_data", None)
            data.pop("response_message", None)

        if status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_204_NO_CONTENT,
        ]:
            response = {
                "success": True,
                "message": api_response_message,
                "status": status_code,
            }
            if data and "additional_info" in data:
                response["additional_info"] = data.get("additional_info")

            if data is not None:
                if "results" in data:
                    response.update(
                        {
                            "count": data["count"],
                            "next": data["next"],
                            "previous": data["previous"],
                            "results": data["results"],
                        }
                    )
                else:
                    response.update({"results": data})
        else:
            response = {
                "success": False,
                "error": data,  # Remove the extra "error" key here
                "message": api_response_message,
                "status": status_code,
            }
            if "detail" in data:
                response["error"]["non_field_errors"] = [data["detail"]]
            elif "non_field_errors" in data:
                response["error"]["non_field_errors"] = data["non_field_errors"]

        return JsonResponse(data=response)
