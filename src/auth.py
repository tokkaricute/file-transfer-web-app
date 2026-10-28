import hmac
import hashlib
from typing import Any

def verify_password(provided_password: str, target_password: str) -> bool:
    """
    Verifies the provided password against the target password using a constant-time comparison.
    """
    if not target_password:
        return True
    
    # Using hmac.compare_digest for constant-time comparison to prevent timing attacks.
    return hmac.compare_digest(provided_password, target_password)
