from django.http import HttpResponse


def robots_txt(request):
    """
    Generates a robots.txt response.

    The response disallows access to certain paths
    (e.g., /admin/, /login/, /logout/) and provides the URL for the sitemap.
    """
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /login/",
        "Disallow: /logout/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
