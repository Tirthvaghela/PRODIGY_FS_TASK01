"""
Custom Rate Limiting Middleware for Prodigy Auth
Implements IP-based rate limiting without decorator conflicts
"""

import time
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware that tracks requests by IP address
    """
    
    # Rate limit configurations
    RATE_LIMITS = {
        '/api/auth/login/': {'requests': 5, 'window': 300},  # 5 requests per 5 minutes
        '/api/auth/forgot-password/': {'requests': 3, 'window': 3600},  # 3 requests per hour
        '/api/auth/reset-password/': {'requests': 5, 'window': 3600},  # 5 requests per hour
        '/api/auth/register/': {'requests': 3, 'window': 3600},  # 3 requests per hour
    }
    
    def process_request(self, request):
        """Process incoming request for rate limiting"""
        
        # Skip rate limiting if disabled
        from django.conf import settings
        if not getattr(settings, 'RATELIMIT_ENABLE', True):
            return None
            
        # Get client IP
        ip_address = self.get_client_ip(request)
        
        # Check if this endpoint should be rate limited
        path = request.path
        if path not in self.RATE_LIMITS:
            return None
            
        # Only apply to specified methods
        if request.method not in ['POST']:
            return None
            
        # Get rate limit config for this endpoint
        config = self.RATE_LIMITS[path]
        
        # Create cache key
        cache_key = f"rate_limit:{ip_address}:{path}"
        
        # Get current request count
        current_requests = cache.get(cache_key, [])
        now = time.time()
        
        # Remove old requests outside the window
        window_start = now - config['window']
        current_requests = [req_time for req_time in current_requests if req_time > window_start]
        
        # Check if rate limit exceeded
        if len(current_requests) >= config['requests']:
            logger.warning(f"Rate limit exceeded for IP {ip_address} on {path}")
            return JsonResponse({
                'error': 'Rate limit exceeded. Please try again later.',
                'retry_after': int(config['window'] - (now - min(current_requests)))
            }, status=429)
        
        # Add current request
        current_requests.append(now)
        
        # Update cache
        cache.set(cache_key, current_requests, config['window'])
        
        return None
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip