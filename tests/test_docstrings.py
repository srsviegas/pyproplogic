import pkgutil
import importlib
import doctest
import pyproplogic

def test_docstrings():
    for _, module_name, _ in pkgutil.walk_packages(pyproplogic.__path__):
        module = importlib.import_module(f"{pyproplogic.__name__}.{module_name}")
        test = doctest.testmod(
            module, optionflags=doctest.NORMALIZE_WHITESPACE
        )
        assert not test.failed, f"DocTest failed for module {module.__name__}"