"""
Build timelapse MP4s (H.264 via imageio-ffmpeg) from TREES frames.

Outputs to ../assets/timelapse/:
  <treatment>.mp4          one representative plant per treatment
  comparison_2x2.mp4       all four treatments synced side-by-side

Each plant's frames are time-ordered; the 2x2 montage resamples every plant
to the same number of output frames so they "grow together" on screen.
A label and an elapsed-day counter are burned into each frame.
"""
import os, re, glob
import cv2
import numpy as np
import imageio.v2 as imageio
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "raw", "trees_timelapse")
OUT = os.path.join(HERE, "..", "assets", "timelapse")
os.makedirs(OUT, exist_ok=True)

TS = re.compile(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})_(\d{2})_(\d{2})")
FPS = 15
TILE_W = 460          # per-plant tile width in montage
SINGLE_W = 720        # standalone video width
N_SYNC = 220          # frames in synced montage

# representative plant per treatment (chosen for frame count + clear growth),
# with friendly label + accent color (BGR)
REP = {
    "MR_plusMicrobe_flight":  dict(plant="mr1-1 jpegs", label="+ECM . Flight",  bgr=(127, 201, 54)),
    "R_minusMicrobe_flight":  dict(plant="R3-3 jpegs",  label="-ECM . Flight",  bgr=(255, 169, 90)),
    "M_plusMicrobe_control":  dict(plant="m2-3 jpegs",  label="+ECM . Ground",  bgr=(77, 122, 31)),
    "X_minusMicrobe_control": dict(plant="X4-1 jpegs",  label="-ECM . Ground",  bgr=(143, 95, 47)),
}
ORDER = ["MR_plusMicrobe_flight", "R_minusMicrobe_flight",
         "M_plusMicrobe_control", "X_minusMicrobe_control"]


def dt(fname):
    m = TS.search(fname)
    if not m:
        return None
    y, mo, d, H, M, S = map(int, m.groups())
    return datetime(y, mo, d, H, M, S)


def frames_for(tkey):
    """Return time-sorted (datetime, path) for the representative plant."""
    pdir = os.path.join(DATA, tkey, REP[tkey]["plant"])
    fs = []
    for fp in glob.glob(pdir + "/**/*.jpg", recursive=True):
        d = dt(os.path.basename(fp))
        if d:
            fs.append((d, fp))
    fs.sort()
    # dedupe identical timestamps
    seen, out = set(), []
    for d, fp in fs:
        if d in seen:
            continue
        seen.add(d); out.append((d, fp))
    return out


def label_tile(img, text, days, bgr):
    h, w = img.shape[:2]
    cv2.rectangle(img, (0, 0), (w, 34), (12, 14, 20), -1)
    cv2.rectangle(img, (0, 0), (6, 34), bgr, -1)
    cv2.putText(img, text, (14, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (236, 237, 232), 1, cv2.LINE_AA)
    tag = f"day {days:4.1f}"
    cv2.putText(img, tag, (w - 96, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 230, 200), 1, cv2.LINE_AA)
    return img


def load_resized(fp, width):
    img = cv2.imread(fp)
    if img is None:
        return None
    h, w = img.shape[:2]
    return cv2.resize(img, (width, int(h * width / w)))


def make_single(tkey):
    info = REP[tkey]
    fs = frames_for(tkey)
    if not fs:
        print("no frames for", tkey); return None
    t0 = fs[0][0]
    out_path = os.path.join(OUT, tkey + ".mp4")
    w = imageio.get_writer(out_path, fps=FPS, codec="libx264", quality=7,
                           macro_block_size=8, output_params=["-pix_fmt", "yuv420p"])
    for d, fp in fs:
        img = load_resized(fp, SINGLE_W)
        if img is None:
            continue
        days = (d - t0).total_seconds() / 86400
        label_tile(img, info["label"], days, info["bgr"])
        w.append_data(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    w.close()
    print("wrote", out_path, f"({len(fs)} frames)")
    return out_path


def resample(seq, n):
    """Pick n items evenly across a sequence by index."""
    if len(seq) <= n:
        return seq
    idx = np.linspace(0, len(seq) - 1, n).round().astype(int)
    return [seq[i] for i in idx]


def make_montage():
    series = {}
    tile_h = None
    for tkey in ORDER:
        fs = frames_for(tkey)
        series[tkey] = fs
        if fs and tile_h is None:
            probe = load_resized(fs[0][1], TILE_W)
            tile_h = probe.shape[0]
    sampled = {k: resample(v, N_SYNC) for k, v in series.items()}
    out_path = os.path.join(OUT, "comparison_2x2.mp4")
    w = imageio.get_writer(out_path, fps=FPS, codec="libx264", quality=7,
                           macro_block_size=8, output_params=["-pix_fmt", "yuv420p"])
    for i in range(N_SYNC):
        tiles = []
        for tkey in ORDER:
            fs = sampled[tkey]
            info = REP[tkey]
            if fs:
                j = min(i, len(fs) - 1)
                d, fp = fs[j]
                img = load_resized(fp, TILE_W)
                days = (d - series[tkey][0][0]).total_seconds() / 86400
            else:
                img = np.zeros((tile_h, TILE_W, 3), np.uint8)
                days = 0
            img = cv2.resize(img, (TILE_W, tile_h))
            label_tile(img, info["label"], days, info["bgr"])
            tiles.append(img)
        top = np.hstack(tiles[:2]); bot = np.hstack(tiles[2:])
        frame = np.vstack([top, bot])
        w.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    w.close()
    print("wrote", out_path)
    return out_path


if __name__ == "__main__":
    for tkey in ORDER:
        make_single(tkey)
    make_montage()
    print("done")
