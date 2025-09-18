from django.http import JsonResponse
from version import get_version, get_commit


def health_check(request):
    """Health check endpoint that returns status, version, and commit."""
    return JsonResponse({
        'ok': True,
        'version': get_version(),
        'commit': get_commit()
    })