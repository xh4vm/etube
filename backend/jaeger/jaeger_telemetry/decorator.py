from functools import wraps
from typing import Optional

from .tracer import tracer


def traced(span: str, request_id: Optional[str] = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            with tracer.start_as_current_span(span) as _span:
                _span.set_attribute(key='http.request_id', value=request_id or '')
                return f(*args, **kwargs)

        return decorated_function
    return decorator
