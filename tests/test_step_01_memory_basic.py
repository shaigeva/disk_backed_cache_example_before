"""Step 1: Tests for basic in-memory cache put/get operations."""

from disk_backed_cache_example.disk_backed_cache import CacheableModel, DiskBackedCache


class SimpleModel(CacheableModel):
    """Simple test model for cache testing."""

    schema_version: str = "1.0.0"
    name: str
    value: int


def test_after_put_get_returns_the_object() -> None:
    """After putting an object, get should return the same object."""
    cache = DiskBackedCache(
        db_path=":memory:",
        model=SimpleModel,
        max_memory_items=10,
        max_memory_size_bytes=1024,
        max_disk_items=100,
        max_disk_size_bytes=10240,
        memory_ttl_seconds=60.0,
        disk_ttl_seconds=3600.0,
        max_item_size_bytes=512,
    )

    test_obj = SimpleModel(name="test", value=42)
    cache.put("key1", test_obj)

    retrieved = cache.get("key1")
    assert retrieved is not None
    assert isinstance(retrieved, SimpleModel)
    assert retrieved.name == "test"
    assert retrieved.value == 42


def test_get_nonexistent_key_returns_none() -> None:
    """Getting a key that doesn't exist should return None."""
    cache = DiskBackedCache(
        db_path=":memory:",
        model=SimpleModel,
        max_memory_items=10,
        max_memory_size_bytes=1024,
        max_disk_items=100,
        max_disk_size_bytes=10240,
        memory_ttl_seconds=60.0,
        disk_ttl_seconds=3600.0,
        max_item_size_bytes=512,
    )

    result = cache.get("nonexistent")
    assert result is None
