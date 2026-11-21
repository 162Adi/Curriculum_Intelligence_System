"""
Cython & Binary Fallback Importer for environments where binary .pyd C-extensions
are restricted by OS Application Control policies.
1. Intercepts all SQLAlchemy Cython modules and safely loads the pure-Python .py implementations.
2. Shims ormsgpack using standard msgpack for LangGraph checkpoint serialization.
"""

import sys
import os
import types
import importlib.util
from importlib.abc import MetaPathFinder

# 1. SQLAlchemy Cython fallback finder
class CythonFallbackFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if 'sqlalchemy' in fullname and (fullname.endswith('_cy') or '_cy' in fullname):
            name = fullname.split('.')[-1]
            parent_pkg = '.'.join(fullname.split('.')[:-1])
            search_dirs = list(path) if path else []
            if not search_dirs and parent_pkg in sys.modules:
                search_dirs = getattr(sys.modules[parent_pkg], '__path__', [])
            for d in search_dirs:
                py_path = os.path.join(d, name + '.py')
                if os.path.isfile(py_path):
                    return importlib.util.spec_from_file_location(fullname, py_path)
        return None


if not any(isinstance(finder, CythonFallbackFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, CythonFallbackFinder())


# 2. ormsgpack fallback shim for LangGraph
if "ormsgpack" not in sys.modules:
    try:
        import ormsgpack  # noqa: F401
    except Exception:
        import msgpack

        class OrmsgpackShim(types.ModuleType):
            OPT_NON_STR_KEYS = 1
            OPT_PASSTHROUGH_DATACLASS = 2
            OPT_PASSTHROUGH_DATETIME = 4
            OPT_PASSTHROUGH_ENUM = 8
            OPT_PASSTHROUGH_UUID = 16
            OPT_REPLACE_SURROGATES = 32
            OPT_SERIALIZE_NUMPY = 64

            MsgpackDecodeError = msgpack.UnpackException
            MsgpackEncodeError = msgpack.PackException

            Ext = msgpack.ExtType

            @staticmethod
            def packb(o, default=None, option=0):
                return msgpack.packb(o, default=default, use_bin_type=True)

            @staticmethod
            def unpackb(packed, ext_hook=None, option=0):
                return msgpack.unpackb(packed, ext_hook=ext_hook, raw=False)

        shim = OrmsgpackShim("ormsgpack")
        sys.modules["ormsgpack"] = shim
