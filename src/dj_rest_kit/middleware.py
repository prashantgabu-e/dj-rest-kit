from django.middleware.csrf import CsrfViewMiddleware


class CsrfExemptAdminMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith("/api/admin/"):
            return None
        else:
            return super().process_view(
                request, callback, callback_args, callback_kwargs
            )
