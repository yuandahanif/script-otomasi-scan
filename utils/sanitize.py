import re
from urllib.parse import urlparse

def sanitize_target(url):
    # Remove protocol (http:// or https://)
    parsed = urlparse(url if '//' in url else f'http://{url}')
    domain = parsed.netloc if parsed.netloc else parsed.path
    
    # Remove port number if present
    domain = domain.split(':')[0]
    
    # Remove any remaining invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*.]', '-', domain)
    return sanitized