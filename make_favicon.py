#!/usr/bin/env python3
"""Draw favicon.ico — the same mark as the inline SVG icon in index.html.

The app's icon is an inline SVG data URI, which every current browser prefers.
favicon.ico is the fallback: it's what a browser fetches from the site root on
its own, what older ones use, and what a bookmark or a search result shows. The
two have to be the same picture, so this draws the SVG's geometry with Pillow
rather than hand-editing a binary nobody can review in a diff.

    python3 make_favicon.py

The mark is a flagstick on the green with a ball beside it — the ⛳ the header
used to wear, drawn properly. It sits on the family tile Money Map, PAPTrack,
Sprint Predictability and Flow Metrics all use: the midnight page as a rounded
square, the soft disc in the bottom-left corner, and the accent gradient.

Everything is drawn at 8x and reduced with Lanczos, which is what gives the
16px version clean edges. Keep the shapes here in step with the SVG in
index.html if that ever changes.
"""

from PIL import Image, ImageDraw

# The mark, in the SVG's own 64x64 coordinates.
BG = (10, 14, 26, 255)          # #0a0e1a — midnight, the default theme's page
GLOW = (20, 28, 51, 255)        # #141c33 — the darker disc in the corner
GRAD_FROM = (129, 140, 248)     # #818cf8 — midnight's accent
GRAD_TO = (165, 180, 252)       # #a5b4fc
GRAD_AXIS = ((10, 52), (54, 12))                  # where the gradient runs

STICK = (21, 16, 47)            # x, top, bottom
STICK_WIDTH = 5.5
FLAG = [(21, 17), (44, 25), (21, 33)]             # the pennant, filled
BALL = (41, 43, 5.5)            # x, y, radius

SCALE = 8                       # supersample, then reduce
SIZES = [16, 32, 48, 64, 128, 256]


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient_at(point):
    """Colour for a point, projected onto the gradient's axis."""
    (x0, y0), (x1, y1) = GRAD_AXIS
    dx, dy = x1 - x0, y1 - y0
    span = dx * dx + dy * dy
    t = ((point[0] - x0) * dx + (point[1] - y0) * dy) / span
    return lerp(GRAD_FROM, GRAD_TO, min(1.0, max(0.0, t)))


def stamp(d, pts, width):
    """A gradient stroke, drawn by stamping a circle at every step.

    Round caps come free that way, and a stroke drawn in coloured pieces would
    otherwise show a seam wherever two pieces meet.
    """
    r = width / 2
    for x, y in pts:
        d.ellipse([(x - r) * SCALE, (y - r) * SCALE,
                   (x + r) * SCALE, (y + r) * SCALE],
                  fill=gradient_at((x, y)) + (255,))


def line_points(a, b, steps=500):
    (ax, ay), (bx, by) = a, b
    return [(ax + (bx - ax) * s / steps, ay + (by - ay) * s / steps)
            for s in range(steps + 1)]


def gradient_polygon(img, pts):
    """Fill a polygon with the gradient.

    Pillow's polygon() takes one flat colour, so the shape is drawn into a mask
    and a full-size gradient is pasted through it — which also keeps the edge
    antialiasing the supersampling gives us.
    """
    n = img.size[0]
    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).polygon([(x * SCALE, y * SCALE) for x, y in pts],
                                 fill=255)
    fill = Image.new('RGBA', (n, n))
    fd = ImageDraw.Draw(fill)
    # One horizontal band per source pixel is plenty: the gradient's axis is
    # mostly diagonal, so banding is invisible once the whole thing is reduced.
    for px in range(0, n, SCALE):
        for py in range(0, n, SCALE):
            fd.rectangle([px, py, px + SCALE, py + SCALE],
                         fill=gradient_at((px / SCALE, py / SCALE)) + (255,))
    img.paste(fill, (0, 0), mask)


def build():
    n = 64 * SCALE
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, n, n], fill=BG)
    # the soft disc bottom-left, the way the SVG has it
    d.ellipse([(14 - 20) * SCALE, (52 - 20) * SCALE,
               (14 + 20) * SCALE, (52 + 20) * SCALE], fill=GLOW)

    x, top, bottom = STICK
    stamp(d, line_points((x, top), (x, bottom)), STICK_WIDTH)
    gradient_polygon(img, FLAG)

    bx, by, br = BALL
    d = ImageDraw.Draw(img)
    d.ellipse([(bx - br) * SCALE, (by - br) * SCALE,
               (bx + br) * SCALE, (by + br) * SCALE], fill=GRAD_TO + (255,))

    # Round the corners with an alpha mask. The SVG leaves the disc square at
    # the edges; an icon reads better rounded, and this is the file that ends
    # up on a bookmarks bar.
    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1],
                                           radius=14 * SCALE, fill=255)
    img.putalpha(mask)
    return img


def main():
    art = build()
    frames = [art.resize((s, s), Image.LANCZOS) for s in SIZES]
    frames[-1].save('favicon.ico', format='ICO',
                    sizes=[(s, s) for s in SIZES])
    print('favicon.ico written at ' + ', '.join(f'{s}px' for s in SIZES))
    print('Now bump the ?v= on every favicon.ico reference — index.html and '
          'privacy.html — browsers cache an icon for a long time and will keep '
          'showing the old one otherwise.')


if __name__ == '__main__':
    main()
