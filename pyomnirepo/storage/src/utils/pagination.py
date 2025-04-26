
from typing import Optional

class Pagination:
    def __init__(self, query: Optional[str] = None, skip: int  = 0, limit: int = 100):
        self.query = query
        self.skip = skip
        self.limit = limit
