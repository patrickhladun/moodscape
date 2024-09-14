from constance import config
from django.templatetags.static import static
from decimal import Decimal
import json

def make_metadata(request, page):
    """
    Generate metadata for a webpage, including title, meta tags, and link tags.

    Args:
        request (HttpRequest): The HTTP request object.
        page (dict): A dictionary containing page metadata information. It
        should include:
            - "title": The title of the page.
            - "meta": A dictionary of meta tags (e.g., description, keywords).
            - "link": A dictionary of link tags (e.g., canonical).

    Returns:
        list: A list of HTML metadata tags.
    """
    site_name = config.SITE_NAME
    locale = config.LOCALE
    url = request.build_absolute_uri()
    metadata = []

    # Handle the title
    title = page.get("title", config.SITE_NAME) + " | " + site_name if "title" in page else config.SITE_NAME
    metadata.append(f"<title>{title}</title>")

    if "meta" in page:
        robots_specified = False
        for key, value in page["meta"].items():
            if value:
                metadata.append(f'<meta name="{key}" content="{value}">')
            if key == "robots":
                robots_specified = True

        default_description = page["meta"].get("description", "") if "meta" in page else ""

        if not robots_specified:
            metadata.append('<meta name="robots" content="index, follow">')

    if "og" in page:
        og_data = page.get("og", {})
        metadata.append(f'<!-- Open Graph data -->')
        og_title = og_data.get("title", page.get("title", site_name))
        og_description = og_data.get("description", default_description)
        og_type = og_data.get("type", "website")
        og_image = og_data.get("image", static('images/moodscape-meta-default.webp'))

        metadata.append(f'<meta property="og:title" content="{og_title}">')
        metadata.append(f'<meta property="og:description" content="{og_description}">')
        metadata.append(f'<meta property="og:type" content="{og_type}">')
        metadata.append(f'<meta property="og:site_name" content="{site_name}">')
        metadata.append(f'<meta property="og:locale" content="{locale}">')
        metadata.append(f'<meta property="og:image" content="{og_image}">')
        metadata.append(f'<meta property="og:url" content="{og_data.get("url", url)}">')

    if "twitter" in page:
        twitter_data = page.get("twitter", {})
        metadata.append(f'<!-- Twitter Card data -->')
        twitter_title = twitter_data.get("title", page.get("title", site_name))
        twitter_description = twitter_data.get("description", default_description)
        twitter_image = twitter_data.get("image", static('images/moodscape-meta-default.webp'))

        metadata.append(f'<meta name="twitter:card" content="summary_large_image">')
        metadata.append(f'<meta name="twitter:title" content="{twitter_title}">')
        metadata.append(f'<meta name="twitter:description" content="{twitter_description}">')
        metadata.append(f'<meta name="twitter:image" content="{twitter_image}">')

    if "link" in page:
        canonical = page["link"].get("canonical", url)
        metadata.append(f'<link rel="canonical" href="{canonical}">')

        for key, value in page["link"].items():
            if key != "canonical" and value:
                metadata.append(f'<link rel="{key}" href="{value}">')
    else:
        metadata.append(f'<link rel="canonical" href="{url}">')

    return metadata