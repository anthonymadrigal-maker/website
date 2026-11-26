# anthonymadrigal.com

Personal engineering portfolio. Plain HTML, CSS and JS with no build step.

```
index.html                  Home page
projects/*.html             One "story" page per project
css/style.css               All styling
js/main.js                  Scroll effects, chapter tracker, galleries, lightbox, video
images/<project>/           Photos (resized to max 2000px)
```

## How the scaling works
On screens wider than 900px, everything is sized in `rem`, and the root font size
is tied to the window width (`html { font-size: clamp(13px, calc(100vw / 110), 26px) }`).
So a laptop shows the same layout as a big monitor, just proportionally smaller.
Phones get a stacked single-column layout.

## Editing
- Text: edit the HTML files directly.
- New gallery photo: add a `<figure style="--r:WIDTH/HEIGHT">` inside a `.gallery`
  (`--r` is the image's aspect ratio, e.g. `--r:0.75` for a 3:4 portrait photo).
- Placeholders to fill in are marked with the dashed "Write-up coming" boxes.

## Hosting
GitHub Pages: Settings → Pages → Deploy from branch → `main` / root.

## Regenerating pages
`tools/build.py` generates `index.html` and `projects/*.html` (needs Python + Pillow):
`python3 tools/build.py`. Editing the HTML directly also works, but rerunning the
script overwrites hand edits, so pick one approach.
