import importlib.util
from pathlib import Path


def load_module():
    module_path = Path(__file__).resolve().parents[0] / "package_figure1.py"
    spec = importlib.util.spec_from_file_location("package_figure1", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_right_side_label_postprocess_is_configured_for_larger_labels():
    mod = load_module()

    assert getattr(mod, "RIGHT_LABEL_FONT_SIZE", 0) >= 11.5
    assert getattr(mod, "FILE_TYPE_FONT_SIZE", 0) >= 18
    assert getattr(mod, "HEADER_FONT_SIZE", 0) >= 15
    assert hasattr(mod, "enlarge_right_side_labels")
