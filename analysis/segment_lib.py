"""
Canopy segmentation for MadWest TREES timelapse frames.

Each frame is a backlit agar plate: green shoot/canopy (what we measure),
reddish roots, a reference grid, and a bright yellow backlight glow we must
NOT count. We isolate the green canopy with a combination of:
  - Excess-Green index (ExG = 2G - R - B), the classic vegetation index, and
  - an HSV hue gate that keeps true greens and rejects the yellow backlight,
then clean up with morphology and keep only sizeable blobs.
"""
import cv2
import numpy as np


def segment_canopy(bgr):
    """Return (mask uint8 0/255, canopy_pixel_count) for a BGR image.

    Plates vary from deep-green to brightly-backlit yellow-green, so a fixed
    hue gate fails. The Excess-Green index captures the canopy completely;
    we then drop near-white backlight glare (blown-out pixels are bright in
    ALL channels, whereas even yellow leaves keep a low blue channel).
    """
    img = bgr.astype(np.float32)
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    exg = 2 * g - r - b                     # vegetation index
    is_green = exg > 20
    min_ch = np.minimum(np.minimum(r, g), b)
    glare = min_ch > 170                    # near-white backlight / frost glare
    mask = is_green & (~glare)
    mask = (mask.astype(np.uint8)) * 255

    # Clean: close small gaps, open away speckle.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)

    # Drop tiny connected components (noise, grid speckle).
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    clean = np.zeros_like(mask)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 80:
            clean[lab == i] = 255

    return clean, int(np.count_nonzero(clean))


def overlay(bgr, mask, color=(0, 0, 255)):
    """Tint segmented canopy for visual QA."""
    out = bgr.copy()
    out[mask > 0] = (0.45 * np.array(color) + 0.55 * out[mask > 0]).astype(np.uint8)
    return out
