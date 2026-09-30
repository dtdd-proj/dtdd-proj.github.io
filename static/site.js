"use strict";
const viewer = document.getElementById("figure-viewer");
const viewerImage = document.getElementById("viewer-image");
const canvas = viewer.querySelector(".viewer-canvas");
const zoomButton = document.getElementById("zoom-figure");
let opener = null;
let previousOverflow = "";

document.querySelectorAll("[data-lightbox]").forEach(link => {
  link.addEventListener("click", event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof viewer.showModal !== "function") return;
    event.preventDefault();
    opener = link;
    const sourceImage = link.querySelector("img");
    const alt = sourceImage ? sourceImage.alt : link.dataset.alt;
    viewerImage.src = link.href;
    viewerImage.alt = alt || "Enlarged experiment figure";
    document.getElementById("original-figure").href = link.href;
    document.getElementById("viewer-description").textContent = alt || "";
    canvas.classList.remove("zoomed");
    zoomButton.textContent = "Zoom in";
    zoomButton.setAttribute("aria-pressed", "false");
    previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    viewer.showModal();
    canvas.scrollTo(0, 0);
  });
});

zoomButton.addEventListener("click", () => {
  const zoomed = canvas.classList.toggle("zoomed");
  canvas.style.setProperty("--zoom-width", Math.max(viewerImage.naturalWidth, canvas.clientWidth * 1.6) + "px");
  zoomButton.textContent = zoomed ? "Fit to width" : "Zoom in";
  zoomButton.setAttribute("aria-pressed", String(zoomed));
  if (!zoomed) canvas.scrollTo(0, 0);
});
document.getElementById("close-viewer").addEventListener("click", () => viewer.close());
viewer.addEventListener("click", event => {
  if (event.target !== viewer) return;
  const rect = viewer.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) viewer.close();
});
viewer.addEventListener("close", () => {
  document.body.style.overflow = previousOverflow;
  if (opener) opener.focus({preventScroll: true});
});

document.getElementById("copybib")?.addEventListener("click", async function () {
  const bib = document.getElementById("bib");
  const status = document.getElementById("copy-status");
  try {
    await navigator.clipboard.writeText(bib.textContent);
    this.textContent = "Copied";
    status.textContent = "BibTeX copied to clipboard.";
    setTimeout(() => { this.textContent = "Copy BibTeX"; }, 1800);
  } catch {
    const range = document.createRange();
    range.selectNodeContents(bib);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    this.textContent = "Press Ctrl/Cmd+C";
    status.textContent = "BibTeX selected. Press Control or Command C to copy.";
  }
});
