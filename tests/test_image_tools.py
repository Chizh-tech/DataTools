"""Unit tests for the image_tools module."""

import io

import pytest
from PIL import Image

from src.image_tools import draw_bounding_boxes, load_image


def _make_image_buffer(size=(200, 200), color=(100, 149, 237)) -> io.BytesIO:
    """Return a BytesIO buffer containing a small PNG image."""
    img = Image.new("RGB", size, color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


class TestLoadImage:
    def test_returns_pil_image(self):
        img = load_image(_make_image_buffer())
        assert isinstance(img, Image.Image)

    def test_mode_is_rgb(self):
        img = load_image(_make_image_buffer())
        assert img.mode == "RGB"

    def test_correct_size(self):
        img = load_image(_make_image_buffer(size=(64, 32)))
        assert img.size == (64, 32)

    def test_invalid_source_raises(self):
        with pytest.raises(ValueError):
            load_image(io.BytesIO(b"not an image"))


class TestDrawBoundingBoxes:
    @pytest.fixture()
    def base_image(self):
        return Image.new("RGB", (200, 200), (255, 255, 255))

    def test_returns_pil_image(self, base_image):
        result = draw_bounding_boxes(base_image, [(10, 10, 50, 50)])
        assert isinstance(result, Image.Image)

    def test_original_not_modified(self, base_image):
        original_pixels = list(base_image.getdata())
        draw_bounding_boxes(base_image, [(10, 10, 50, 50)])
        assert list(base_image.getdata()) == original_pixels

    def test_same_size_as_input(self, base_image):
        result = draw_bounding_boxes(base_image, [(10, 10, 50, 50)])
        assert result.size == base_image.size

    def test_multiple_boxes(self, base_image):
        boxes = [(10, 10, 50, 50), (60, 60, 100, 100)]
        result = draw_bounding_boxes(base_image, boxes)
        assert isinstance(result, Image.Image)

    def test_with_labels(self, base_image):
        result = draw_bounding_boxes(
            base_image, [(10, 10, 50, 50)], labels=["cat"]
        )
        assert isinstance(result, Image.Image)

    def test_mismatched_labels_raises(self, base_image):
        with pytest.raises(ValueError):
            draw_bounding_boxes(
                base_image, [(10, 10, 50, 50)], labels=["cat", "dog"]
            )

    def test_empty_boxes_list(self, base_image):
        result = draw_bounding_boxes(base_image, [])
        assert isinstance(result, Image.Image)
