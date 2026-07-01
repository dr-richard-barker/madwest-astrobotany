"""Save segmentation overlays for a few sample frames so we can eyeball them."""
import sys, glob, os
import cv2
from segment_lib import segment_canopy, overlay

OUT = sys.argv[1] if len(sys.argv) > 1 else "qa"
os.makedirs(OUT, exist_ok=True)

# one early + one late frame from each treatment's first plant folder
roots = sorted(glob.glob("../data/trees/*/"))
for tr in roots:
    plants = sorted(glob.glob(tr + "*/"))
    if not plants:
        continue
    frames = sorted(glob.glob(plants[0] + "*.jpg"))
    if not frames:
        continue
    picks = {"early": frames[0], "late": frames[-1], "mid": frames[len(frames)//2]}
    tname = os.path.basename(os.path.normpath(tr))
    for label, fp in picks.items():
        bgr = cv2.imread(fp)
        if bgr is None:
            continue
        mask, count = segment_canopy(bgr)
        ov = overlay(bgr, mask)
        # shrink for quick viewing
        h, w = ov.shape[:2]
        scale = 600 / w
        ov = cv2.resize(ov, (600, int(h * scale)))
        out = f"{OUT}/{tname}__{label}.jpg"
        cv2.imwrite(out, ov)
        print(f"{tname:32s} {label:5s} canopy_px={count:8d}  {os.path.basename(fp)}")
