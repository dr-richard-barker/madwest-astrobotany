"""
Cover faces with a drawn smiley for privacy before public release.

Uses OpenCV Haar cascades (frontal alt2 + default + profile, both orientations).
Detection is imperfect, so this script is run and then EVERY output is eyeballed;
misses are patched with manual boxes (see manual_patches.py).
"""
import cv2
import numpy as np

_D = cv2.data.haarcascades
_CASCADES = [
    cv2.CascadeClassifier(_D + "haarcascade_frontalface_alt2.xml"),
    cv2.CascadeClassifier(_D + "haarcascade_frontalface_default.xml"),
    cv2.CascadeClassifier(_D + "haarcascade_profileface.xml"),
]


def _iou(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    x1, y1 = max(ax, bx), max(ay, by)
    x2, y2 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    if inter == 0:
        return 0.0
    return inter / (aw * ah + bw * bh - inter)


def detect_faces(bgr, min_frac=0.012):
    """Return list of (x,y,w,h). min_frac = min face size as fraction of width."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    h, w = gray.shape
    minsz = max(24, int(w * min_frac))
    found = []
    variants = [gray, cv2.flip(gray, 1)]  # normal + mirror (for profile both ways)
    for vi, g in enumerate(variants):
        for cas in _CASCADES:
            rects = cas.detectMultiScale(g, scaleFactor=1.08, minNeighbors=5,
                                         minSize=(minsz, minsz))
            for (x, y, ww, hh) in rects:
                if vi == 1:  # mirror back
                    x = w - x - ww
                found.append((int(x), int(y), int(ww), int(hh)))
    # de-duplicate overlapping detections
    merged = []
    for f in sorted(found, key=lambda r: -r[2] * r[3]):
        if all(_iou(f, m) < 0.3 for m in merged):
            merged.append(f)
    return merged


def draw_smiley(bgr, box, expand=1.5):
    """Draw an opaque yellow smiley covering (and over-covering) a face box."""
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    r = int(max(w, h) * expand / 2)
    cx, cy = int(cx), int(cy)
    yellow = (60, 200, 250)   # BGR warm yellow
    dark = (30, 30, 30)
    cv2.circle(bgr, (cx, cy), r, yellow, -1, cv2.LINE_AA)
    cv2.circle(bgr, (cx, cy), r, (20, 120, 160), max(2, r // 18), cv2.LINE_AA)
    # eyes
    ex = int(r * 0.38); ey = int(r * 0.28); er = max(2, int(r * 0.12))
    cv2.circle(bgr, (cx - ex, cy - ey), er, dark, -1, cv2.LINE_AA)
    cv2.circle(bgr, (cx + ex, cy - ey), er, dark, -1, cv2.LINE_AA)
    # smile (lower arc of an ellipse)
    cv2.ellipse(bgr, (cx, cy + int(r * 0.05)), (int(r * 0.55), int(r * 0.5)),
                0, 20, 160, dark, max(2, r // 12), cv2.LINE_AA)
    return bgr


def redact(path, out=None, min_frac=0.012, extra_boxes=None):
    bgr = cv2.imread(path)
    if bgr is None:
        return -1
    boxes = detect_faces(bgr, min_frac)
    for b in boxes:
        draw_smiley(bgr, b)
    for b in (extra_boxes or []):        # manual patches, in pixel coords
        draw_smiley(bgr, b)
    cv2.imwrite(out or path, bgr)
    return len(boxes)


if __name__ == "__main__":
    import sys, glob
    for pat in sys.argv[1:]:
        for p in glob.glob(pat):
            n = redact(p)
            print(f"{n:3d} faces  {p}")
