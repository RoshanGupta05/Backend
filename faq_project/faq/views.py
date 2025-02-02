from rest_framework import viewsets
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing FAQs.
    Supports language selection via the `lang` query parameter.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        """
        Override the default queryset to support caching and language-specific translations.
        """
        lang = self.request.query_params.get('lang', 'en')  # Default to English if no language is specified
        cache_key = f'faqs_{lang}'  # Unique cache key for each language

        # Check if data is already cached
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # If not cached, fetch data from the database
        queryset = super().get_queryset()

        # Cache the queryset for 15 minutes (900 seconds)
        cache.set(cache_key, queryset, timeout=900)
        return queryset