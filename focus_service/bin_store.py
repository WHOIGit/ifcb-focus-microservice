"""IFCB bin store implementation."""

from ifcb import DataDirectory
from storage.config_builder import register_store
from storage.object import ObjectStore


@register_store
class IFCBBinStore(ObjectStore):
    """Store for accessing IFCB bin data."""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get(self, key):
        data_dir = DataDirectory(self.data_dir)
        ifcb_bin = data_dir[key]
        return ifcb_bin

    def exists(self, key):
        try:
            data_dir = DataDirectory(self.data_dir)
            return data_dir.has_key(key)
        except Exception:
            return False

    def put(self, key, value):
        raise NotImplementedError("IFCB stores are read-only")

    def delete(self, key):
        raise NotImplementedError("IFCB stores are read-only")
