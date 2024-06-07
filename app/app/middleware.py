import time
from django.utils.deprecation import MiddlewareMixin


class ResponseTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Сохраняем время начала обработки запроса."""
        request.start_time = time.time()

    def process_response(self, request, response):
        """Вычисляем и добавляем время обработки в заголовки ответа."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = str(duration)
        return response
