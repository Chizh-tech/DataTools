"""Image tools module – load images and draw bounding boxes."""

from typing import List, Optional, Tuple

from PIL import Image, ImageDraw


def load_image(source) -> Image.Image:
    """Load an image from a file path or file-like object.

    Args:
        source: A file path string or a file-like object (e.g. a Streamlit
            ``UploadedFile``).

    Returns:
        A :class:`PIL.Image.Image` in RGB mode.

    Raises:
        ValueError: If the source cannot be opened as an image.
    """
    try:
        img = Image.open(source)
        return img.convert("RGB")
    except Exception as exc:
        raise ValueError(f"Failed to load image: {exc}") from exc


def draw_bounding_boxes(
    image: Image.Image,
    boxes: List[Tuple[int, int, int, int]],
    labels: Optional[List[str]] = None,
    color: str = "red",
    width: int = 2,
) -> Image.Image:
    """Draw bounding boxes on an image.

    Each bounding box is defined as ``(x0, y0, x1, y1)`` in pixel
    coordinates where ``(x0, y0)`` is the top-left corner and
    ``(x1, y1)`` is the bottom-right corner.

    Args:
        image: The source image.  A copy is made so the original is not
            modified.
        boxes: A list of ``(x0, y0, x1, y1)`` tuples.
        labels: Optional list of label strings, one per box.  If
            provided it must have the same length as *boxes*.
        color: Box and label colour string accepted by Pillow (default
            ``"red"``).
        width: Line width in pixels (default ``2``).

    Returns:
        A new :class:`PIL.Image.Image` with the boxes drawn on it.

    Raises:
        ValueError: If *labels* is provided but its length does not match
            *boxes*.
    """
    if labels is not None and len(labels) != len(boxes):
        raise ValueError(
            f"Number of labels ({len(labels)}) must match number of boxes ({len(boxes)})"
        )

    result = image.copy()
    draw = ImageDraw.Draw(result)

    for idx, box in enumerate(boxes):
        draw.rectangle(box, outline=color, width=width)
        if labels is not None:
            draw.text((box[0], max(0, box[1] - 14)), labels[idx], fill=color)

    return result
