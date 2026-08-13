# app/services/image_extraction_service.py
import cv2
import numpy as np


def extract_photo_regions(image_bytes: bytes, max_regions: int = 3) -> list[bytes]:
    """
    Heuristically detects 'photo-like' regions within a screenshot/clipping,
    distinct from text blocks, and returns them as cropped JPEG bytes.
    This is an approximation, not perfect object detection.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return []

    h, w = img.shape[:2]
    total_area = h * w

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Merge nearby edges into solid blobs so we get whole regions, not scattered lines
    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        x, y, cw, ch = cv2.boundingRect(contour)
        area = cw * ch

        # Skip tiny noise and skip near-full-image blobs (that's just "the whole page")
        if area < total_area * 0.03 or area > total_area * 0.85:
            continue

        aspect_ratio = cw / ch if ch > 0 else 0
        # Text paragraphs tend to be very wide-and-short or narrow-and-tall; skip those
        if aspect_ratio > 6 or aspect_ratio < 0.15:
            continue

        region = img[y:y + ch, x:x + cw]

        # Photos have higher pixel-value variance than flat text/background blocks
        if np.std(region) < 20:
            continue

        candidates.append((area, region))

    # Prefer larger regions first — more likely to be "the photo" than incidental blobs
    candidates.sort(key=lambda c: c[0], reverse=True)

    results = []
    for _, region in candidates[:max_regions]:
        success, encoded = cv2.imencode(".jpg", region)
        if success:
            results.append(encoded.tobytes())

    return results