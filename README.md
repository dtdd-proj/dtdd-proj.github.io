# DTDD project page

Project URL: https://dtdd-proj.github.io/

## Editing and previewing

Edit `page.html` for content, `static/site.css` for layout, and `static/site.js`
for figure viewing and citation copying. Figure metadata and resource URLs live
in `build.py`. Run `python3 build.py` to regenerate `index.html` and the ignored
local `preview.html`. The build uses only the Python standard library.

Run `python3 build.py --check` to check that the generated page is current.
For a local preview, run `python3 -m http.server 8000` and open
http://localhost:8000/ . Commit both the source changes and `index.html`.

Set `ARXIV` / `CODE` in `build.py` when public links are available. Empty values
render non-clickable “Coming soon” labels; do not substitute placeholder URLs.

## GitHub Pages

This is the user site for the `dtdd-proj` account. Publish from `main`, `/ (root)`.
The `.nojekyll` file enables direct static-file publishing. All local asset paths
are relative, so local previews and GitHub Pages use the same files.

The previous project site was at `Qijia-He/dtdd`. After verifying the new site,
unpublish that repository's Pages deployment; retain its source and history.
