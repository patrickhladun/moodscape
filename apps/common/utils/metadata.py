import json

from constance import config
from django.templatetags.static import static


class MetadataHandler:
    """
    Base class for metadata generation. Each specific metadata type (like Open
    Graph, Twitter) will inherit from this class and implement the `generate`
    method.
    """

    def generate(self, request, page, site_name, default_description):
        raise NotImplementedError("Subclasses must implement this method")


class StandardMetadataHandler(MetadataHandler):
    """
    Handles standard metadata and canonical links.
    """

    def generate(self, request, page, site_name, default_description):
        url = request.build_absolute_uri()
        metadata = []

        title = (
            page.get("title", config.SITE_NAME) + " | " + site_name
            if "title" in page
            else config.SITE_NAME
        )
        metadata.append(f"<title>{title}</title>")

        if "meta" in page:
            robots_specified = False
            for key, value in page["meta"].items():
                if value:
                    metadata.append(f'<meta name="{key}" content="{value}">')
                if key == "robots":
                    robots_specified = True
            if not robots_specified:
                metadata.append(
                    '<meta name="robots" content="index, follow">'
                )

        if "link" in page:
            canonical = page["link"].get("canonical", url)
            metadata.append(f'<link rel="canonical" href="{canonical}">')

            for key, value in page["link"].items():
                if key != "canonical" and value:
                    metadata.append(f'<link rel="{key}" href="{value}">')
        else:
            metadata.append(f'<link rel="canonical" href="{url}">')

        return metadata


class OpenGraphHandler(MetadataHandler):
    """
    Handles Open Graph metadata.
    """

    def generate(self, request, page, site_name, default_description):
        url = request.build_absolute_uri()
        og_tags = []

        if "og" in page:
            og_data = page.get("og", {})
            og_tags.append(f"<!-- Open Graph data -->")
            og_title = og_data.get("title", page.get("title", site_name))
            og_description = og_data.get("description", default_description)
            og_type = og_data.get("type", "website")
            og_image = og_data.get(
                "image", static("images/moodscape-meta-default.webp")
            )

            og_tags.append(
                f'<meta property="og:title" content="{og_title}">'
            )
            og_tags.append(
                f'<meta property="og:description" content="{og_description}">'
            )
            og_tags.append(f'<meta property="og:type" content="{og_type}">')
            og_tags.append(
                f'<meta property="og:site_name" content="{site_name}">'
            )
            og_tags.append(
                f'<meta property="og:locale" content="{config.LOCALE}">'
            )
            og_tags.append(
                f'<meta property="og:image" content="{og_image}">'
            )
            og_tags.append(
                f'<meta property="og:url" content="{og_data.get("url", url)}">'
            )

        return og_tags


class TwitterHandler(MetadataHandler):
    """
    Handles Twitter Card metadata.
    """

    def generate(self, request, page, site_name, default_description):
        twitter_tags = []

        if "twitter" in page:
            twitter_data = page.get("twitter", {})
            twitter_tags.append(f"<!-- Twitter Card data -->")
            twitter_title = twitter_data.get(
                "title", page.get("title", site_name)
            )
            twitter_description = twitter_data.get(
                "description", default_description
            )
            twitter_image = twitter_data.get(
                "image", static("images/moodscape-meta-default.webp")
            )

            twitter_tags.append(
                f'<meta name="twitter:card" content="summary_large_image">'
            )
            twitter_tags.append(
                f'<meta name="twitter:site" content="{config.TWITTER}">'
            )
            twitter_tags.append(
                f'<meta name="twitter:title" content="{twitter_title}">'
            )
            twitter_tags.append(
                (
                    f'<meta name="twitter:description" '
                    f'content="{twitter_description}">'
                )
            )
            twitter_tags.append(
                f'<meta name="twitter:image" content="{twitter_image}">'
            )
            twitter_tags.append(
                (
                    f'<meta name="twitter:image:alt" content='
                    f'"{twitter_data.get("image_alt", twitter_title)}">'
                )
            )

        return twitter_tags


class ProductSchemaHandler(MetadataHandler):
    """
    Handles Product Schema using JSON-LD.
    """

    def generate(self, request, page, site_name, default_description):
        product_schema = []

        if "product" in page:
            url = request.build_absolute_uri()
            product_data = page["product"]
            schema_data = {
                "@context": "https://schema.org/",
                "@type": "Product",
                "name": product_data.get(
                    "name", page.get("title", site_name)
                ),
                "description": product_data.get(
                    "description", default_description
                ),
                "image": product_data.get(
                    "image", static("images/moodscape-meta-default.webp")
                ),
                "sku": product_data.get("sku", ""),
                "brand": {
                    "@type": "Brand",
                    "name": product_data.get("brand", site_name),
                },
                "offers": {
                    "@type": "Offer",
                    "url": url,
                    "priceCurrency": config.CURRENCY,
                    "price": str(product_data.get("price", "0.00")),
                    "priceValidUntil": product_data.get(
                        "priceValidUntil", ""
                    ),
                    "itemCondition": "https://schema.org/NewCondition",
                    "availability": "https://schema.org/"
                    + product_data.get("availability", "InStock"),
                    "seller": {"@type": "Organization", "name": site_name},
                },
            }
            schema_json = json.dumps(schema_data)
            product_schema.append(f"<!-- Product Schema -->")
            product_schema.append(
                f'<script type="application/ld+json">{schema_json}</script>'
            )

        return product_schema


class MetadataFactory:
    """
    The factory class that returns the appropriate metadata handler based on
    the type.
    """

    @staticmethod
    def get_handler(metadata_type):
        if metadata_type == "standard":
            return StandardMetadataHandler()
        elif metadata_type == "og":
            return OpenGraphHandler()
        elif metadata_type == "twitter":
            return TwitterHandler()
        elif metadata_type == "product_schema":
            return ProductSchemaHandler()
        else:
            raise ValueError(f"Unknown metadata type: {metadata_type}")


def make_metadata(request, page):
    """
    Main function to generate metadata using the factory pattern.
    """
    site_name = config.SITE_NAME
    default_description = page.get("meta", {}).get("description", "")

    all_metadata = []

    for metadata_type in ["standard", "og", "twitter", "product_schema"]:
        handler = MetadataFactory.get_handler(metadata_type)
        all_metadata.extend(
            handler.generate(request, page, site_name, default_description)
        )

    return all_metadata
