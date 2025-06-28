from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
import redis
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint de vérification de la santé des services
    """
    health_status = {
        'status': 'healthy',
        'services': {},
        'timestamp': None
    }
    
    # Vérifier la base de données
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['services']['database'] = {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
    except Exception as e:
        health_status['services']['database'] = {
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}'
        }
        health_status['status'] = 'unhealthy'
    
    # Vérifier Redis
    try:
        redis_client = redis.from_url(os.getenv('REDIS_URL', 'redis://redis:6379/0'))
        redis_client.ping()
        health_status['services']['redis'] = {
            'status': 'healthy',
            'message': 'Redis connection successful'
        }
    except Exception as e:
        health_status['services']['redis'] = {
            'status': 'unhealthy',
            'message': f'Redis connection failed: {str(e)}'
        }
        health_status['status'] = 'unhealthy'
    
    # Vérifier le cache Django
    try:
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        if cache_result == 'ok':
            health_status['services']['cache'] = {
                'status': 'healthy',
                'message': 'Django cache working'
            }
        else:
            raise Exception("Cache test failed")
    except Exception as e:
        health_status['services']['cache'] = {
            'status': 'unhealthy',
            'message': f'Django cache failed: {str(e)}'
        }
        health_status['status'] = 'unhealthy'
    
    # Informations système
    health_status['system'] = {
        'debug': os.getenv('DEBUG', 'False'),
        'environment': os.getenv('ENVIRONMENT', 'development')
    }
    
    # Déterminer le code de statut HTTP
    http_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(health_status, status=http_status) 