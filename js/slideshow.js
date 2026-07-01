// Lightweight image slideshow. Usage:
//   <div class="slideshow" id="x"></div>
//   <script>initSlideshow("x", { base: "assets/slides/foo/", count: 4,
//                                 pad: 2, captions: {1:"...", 2:"..."},
//                                 thumbs: true });</script>
function initSlideshow(id, cfg) {
  var root = document.getElementById(id);
  if (!root) return;
  var n = cfg.count, i = 0, pad = cfg.pad || 2, caps = cfg.captions || {};
  var src = function (k) {
    var num = String(k + 1).padStart(pad, "0");
    return cfg.base + "slide_" + num + ".jpg";
  };

  var stage = document.createElement("div"); stage.className = "ss-stage";
  var img = document.createElement("img"); img.alt = "slide";
  img.loading = "lazy";
  var prev = document.createElement("button");
  prev.className = "ss-btn ss-prev"; prev.innerHTML = "‹"; prev.setAttribute("aria-label", "Previous slide");
  var next = document.createElement("button");
  next.className = "ss-btn ss-next"; next.innerHTML = "›"; next.setAttribute("aria-label", "Next slide");
  stage.appendChild(img); stage.appendChild(prev); stage.appendChild(next);

  var bar = document.createElement("div"); bar.className = "ss-bar";
  var caption = document.createElement("div"); caption.className = "ss-caption";
  var count = document.createElement("div"); count.className = "ss-count";
  bar.appendChild(caption); bar.appendChild(count);

  root.appendChild(stage); root.appendChild(bar);

  var thumbs = null;
  if (cfg.thumbs) {
    thumbs = document.createElement("div"); thumbs.className = "ss-thumbs";
    for (var t = 0; t < n; t++) {
      var ti = document.createElement("img");
      ti.src = src(t); ti.loading = "lazy"; ti.dataset.k = t;
      ti.addEventListener("click", function (e) { go(+e.target.dataset.k); });
      thumbs.appendChild(ti);
    }
    root.appendChild(thumbs);
  }

  function render() {
    img.src = src(i);
    count.textContent = (i + 1) + " / " + n;
    caption.textContent = caps[i + 1] || "";
    if (thumbs) {
      var kids = thumbs.children;
      for (var k = 0; k < kids.length; k++) kids[k].classList.toggle("active", k === i);
      if (kids[i]) kids[i].scrollIntoView({ block: "nearest", inline: "center" });
    }
  }
  function go(k) { i = (k + n) % n; render(); }
  prev.addEventListener("click", function () { go(i - 1); });
  next.addEventListener("click", function () { go(i + 1); });

  // keyboard when the slideshow is in view / focused
  root.tabIndex = 0;
  root.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { go(i - 1); e.preventDefault(); }
    if (e.key === "ArrowRight") { go(i + 1); e.preventDefault(); }
  });

  render();
}
