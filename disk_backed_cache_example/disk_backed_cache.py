from typing import Optional, Type

from pydantic import BaseModel


class CacheableModel(BaseModel):
    schema_version: str


class DiskBackedCache:
    """
    SQLite-backed storage for cache objects.

    Stores serialized objects with metadata (timestamp, schema_version, size)
    and provides LRU eviction support.
    """

    def __init__(
        self,
        db_path: str,
        model: Type[CacheableModel],
        max_memory_items: int,
        max_memory_size_bytes: int,
        max_disk_items: int,
        max_disk_size_bytes: int,
        memory_ttl_seconds: float,
        disk_ttl_seconds: float,
        max_item_size_bytes: int,  # items larger than this are disk-only
    ) -> None:
        # Step 1: Simple in-memory cache storage
        self._memory_cache: dict[str, CacheableModel] = {}

    def get(self, key: str, timestamp: Optional[float] = None) -> Optional[CacheableModel]:
        # Step 1: Simple retrieval from memory cache
        return self._memory_cache.get(key)

    def put(self, key: str, value: CacheableModel, timestamp: Optional[float] = None) -> None:
        # Step 1: Simple storage in memory cache
        self._memory_cache[key] = value

    def delete(self, key: str) -> None:
        raise NotImplementedError()

    def get_total_size(self) -> int:
        raise NotImplementedError()

    def get_count(self) -> int:
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()

    def exists(self, key: str, timestamp: Optional[float] = None) -> bool:
        raise NotImplementedError()

    def close(self) -> None:
        raise NotImplementedError()
