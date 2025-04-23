import hashlib
from urllib.parse import urlparse
from collections import Counter

class URLService:
    """
    Service layer for URL shortening functionality.

    Handles URL encoding, decoding, and in-memory storage of shortened URLs.
    Also tracks domain usage metrics.
    """

    def __init__(self):
        """
        Initializes the service with in-memory dictionaries for URL mapping
        and a counter to track domain usage.
        """
        self.url_map = {}           # Maps original URLs to short versions
        self.reverse_map = {}       # Maps short versions to original URLs
        self.domain_counter = Counter()  # Tracks count of domains

    def shorten(self, original_url):
        """
        Generates a shortened version of a given URL. If the URL was previously
        shortened, it returns the same shortened value.

        Args:
            original_url (str): The full URL to shorten.

        Returns:
            str: A 6-character hash representing the short URL.
        """
        if original_url in self.url_map:
            return self.url_map[original_url]

        # Generate a deterministic 6-character hash
        short = hashlib.md5(original_url.encode()).hexdigest()[:6]

        # Store mappings
        self.url_map[original_url] = short
        self.reverse_map[short] = original_url

        # Count domain
        domain = self.extract_domain(original_url)
        self.domain_counter[domain] += 1

        return short

    def get_original_url(self, short_url):
        """
        Retrieves the original URL from a shortened version.

        Args:
            short_url (str): The short key of the URL.

        Returns:
            str or None: The original URL if found, else None.
        """
        return self.reverse_map.get(short_url)

    def extract_domain(self, url):
        """
        Extracts and normalizes the domain from a URL, excluding 'www'.

        Args:
            url (str): The input URL.

        Returns:
            str: The domain part of the URL.
        """
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")

