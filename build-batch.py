#!/usr/bin/env python3
"""US Turf — Phase 2 creative batch builder.

Generates 6 ad variants from the May 2026 competitor teardown:
1. 472 Vegas Families  — stat-shock w/ photo background
2. $5 + $2 = $7/sq.ft  — math layout
3. Vegas Yards from $166/mo — fullbleed payment anchor
4. 22 Years. One Family — fullbleed longevity
5. B2 · C3 · C4 · C10 — 4-license grid
6. Lifetime. Not 10 Years — warranty comparison

Output: 6 variants × {1:1, 9:16} = 12 PNGs in renders/ad-batch/may2026/
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

POPPINS_BLACK = "/tmp/ad-fonts/Poppins-Black.ttf"
POPPINS_BOLD = "/tmp/ad-fonts/Poppins-Bold.ttf"
POPPINS_SEMI = "/tmp/ad-fonts/Poppins-SemiBold.ttf"
POPPINS_REG = "/tmp/ad-fonts/Poppins-Regular.ttf"
POPPINS_MED = "/tmp/ad-fonts/Poppins-Medium.ttf"


def draw_polygon_star(draw, cx, cy, r, fill):
    """5-pointed star drawn as polygon. Use anywhere a ★ glyph is needed —
    Poppins lacks U+2605 and Arial Bold's metrics lie about it too."""
    pts = []
    for j in range(10):
        ang = math.radians(-90 + j * 36)
        rr = r if j % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)

REPO_ROOT = Path(__file__).parent
PHOTO_ROOT = Path("/Users/kylesimmons/.claude/skills/product-visual-generator/brands/usturf/competitor-assets")
OUT = REPO_ROOT / "renders" / "ad-batch" / "may2026"
(OUT / "1x1").mkdir(parents=True, exist_ok=True)
(OUT / "9x16").mkdir(parents=True, exist_ok=True)

USTURF_GREEN = (79, 174, 69)
USTURF_GREEN_DARK = (54, 125, 47)
USTURF_BLUE = (91, 182, 232)
ORANGE_CTA = (242, 107, 31)
CREAM = (250, 250, 246)
LIGHT_GREY = (240, 240, 240)
BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
DIM_GREY = (140, 140, 140)
GOLD = (255, 196, 49)
RED = (220, 50, 47)
DARK_NAVY = (28, 36, 48)


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, text, font, y, w, color):
    line_w = int(font.getlength(text))
    bbox = font.getbbox(text)
    draw.text(((w - line_w) // 2, y - bbox[1]), text, font=font, fill=color)


def fit_cover(img, target_w, target_h):
    iw, ih = img.size
    s = max(target_w / iw, target_h / ih)
    nw, nh = int(iw * s), int(ih * s)
    img = img.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - target_w) // 2
    y0 = (nh - target_h) // 2
    return img.crop((x0, y0, x0 + target_w, y0 + target_h))


def _draw_arrow(canvas, cx, cy, length, color):
    SCALE = 4
    L = length * SCALE
    pad = 12 * SCALE
    cw = L + pad * 2
    ch = int(L * 0.7) + pad * 2
    layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    cyl = ch // 2
    shaft_w = max(2, int(L * 0.075))
    head_size = int(L * 0.30)
    d.rectangle([(pad, cyl - shaft_w // 2),
                 (pad + L - head_size // 2, cyl + shaft_w // 2)], fill=color)
    tip_x = pad + L
    base_x = pad + L - head_size
    d.polygon([(tip_x, cyl), (base_x, cyl - head_size),
               (base_x, cyl + head_size)], fill=color)
    small = layer.resize((cw // SCALE, ch // SCALE), Image.LANCZOS)
    pos = (cx - small.width // 2, cy - small.height // 2)
    if canvas.mode == "RGBA":
        canvas.alpha_composite(small, pos)
    else:
        canvas.paste(small, pos, small)


def draw_cta_pill(canvas, x, y, w, h, text, fill_color, text_color, font):
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([(x + 4, y + 8), (x + w + 4, y + h + 8)],
                         radius=h // 2, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    if canvas.mode == "RGBA":
        canvas.alpha_composite(shadow)
    else:
        canvas.paste(shadow, (0, 0), shadow)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=h // 2,
                           fill=fill_color)
    text_w = int(font.getlength(text))
    bbox = font.getbbox(text)
    text_h_ = bbox[3] - bbox[1]
    arrow_len = int(h * 0.45)
    gap = int(h * 0.30)
    block_w = text_w + gap + arrow_len
    tx = x + (w - block_w) // 2
    ty = y + (h - text_h_) // 2 - bbox[1]
    draw.text((tx, ty), text, font=font, fill=text_color)
    arrow_cx = tx + text_w + gap + arrow_len // 2
    arrow_cy = y + h // 2
    _draw_arrow(canvas, arrow_cx, arrow_cy, arrow_len, text_color)


def add_top_scrim(canvas, height_frac=0.45, max_alpha=200):
    W, H = canvas.size
    grad = Image.new("RGBA", (W, int(H * height_frac)), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for i in range(grad.height):
        a = int(max_alpha * (1 - i / grad.height) ** 1.3)
        gd.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    if canvas.mode != "RGBA":
        canvas = canvas.convert("RGBA")
    canvas.alpha_composite(grad, (0, 0))
    return canvas


def add_bottom_scrim(canvas, height_frac=0.40, max_alpha=215):
    W, H = canvas.size
    grad = Image.new("RGBA", (W, int(H * height_frac)), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for i in range(grad.height):
        a = int(max_alpha * (i / grad.height) ** 1.3)
        gd.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    if canvas.mode != "RGBA":
        canvas = canvas.convert("RGBA")
    canvas.alpha_composite(grad, (0, H - grad.height))
    return canvas


def build_fullbleed(W, H, photo_path, headline, sub, cta_text, out,
                    eyebrow=None, headline_color=WHITE, accent_words=None,
                    accent_color=GOLD, cta_fill=USTURF_GREEN, cta_text_color=WHITE):
    photo = Image.open(photo_path).convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    canvas = add_top_scrim(canvas, 0.50)
    canvas = add_bottom_scrim(canvas, 0.42)
    draw = ImageDraw.Draw(canvas, "RGBA")
    pad_x = int(W * 0.07)

    if eyebrow:
        eb_size = max(24, int(W * 0.030))
        eb_font = load_font(POPPINS_BOLD, eb_size)
        draw_centered(draw, eyebrow.upper(), eb_font, int(H * 0.05), W,
                      (*GOLD, 240))

    headline_size = int(W * 0.10) if H > W * 1.5 else int(W * 0.095)
    h_font = load_font(POPPINS_BLACK, headline_size)
    upper = headline.upper()
    lines = wrap(upper, h_font, W - pad_x * 2)
    while len(lines) > 3 and headline_size > 50:
        headline_size -= 6
        h_font = load_font(POPPINS_BLACK, headline_size)
        lines = wrap(upper, h_font, W - pad_x * 2)
    ascent, descent = h_font.getmetrics()
    line_h = ascent + descent
    headline_y = int(H * 0.10) if not eyebrow else int(H * 0.13)
    y = headline_y
    accent_words = accent_words or set()
    for line in lines:
        if accent_words and any(aw in line.upper() for aw in accent_words):
            tokens = line.split()
            spaced = [t + (" " if i < len(tokens) - 1 else "")
                      for i, t in enumerate(tokens)]
            line_w = int(h_font.getlength("".join(spaced)))
            x = (W - line_w) // 2
            for tok in spaced:
                clean = tok.strip().rstrip(".!?,;").upper()
                color = accent_color if clean in accent_words else headline_color
                draw.text((x, y - h_font.getbbox(line)[1]), tok,
                          font=h_font, fill=color)
                x += int(h_font.getlength(tok))
        else:
            draw_centered(draw, line, h_font, y, W, headline_color)
        y += int(line_h * 0.95)

    cta_h = int(H * 0.06) if H > W * 1.5 else int(H * 0.085)
    cta_h = max(80, cta_h)
    cta_w = min(int(W * 0.62), 720)
    cta_size = max(28, int(cta_h * 0.36))
    cta_font = load_font(POPPINS_BOLD, cta_size)
    cta_x = (W - cta_w) // 2
    cta_y = H - cta_h - int(H * 0.06)

    if sub:
        sub_size = max(22, int(W * 0.028))
        sub_font = load_font(POPPINS_MED, sub_size)
        sub_lines = wrap(sub, sub_font, W - pad_x * 2)
        sub_block_h = (sub_font.size + 12) * len(sub_lines)
        sub_y_start = cta_y - sub_block_h - int(H * 0.025)
        sy = sub_y_start
        for sl in sub_lines:
            draw_centered(draw, sl, sub_font, sy, W, (255, 255, 255, 230))
            sy += sub_font.size + 12

    draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, cta_text,
                  cta_fill, cta_text_color, cta_font)

    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# V1: Stat-shock — photo background + big number overlay
# -----------------------------------------------------------------------------

def build_v1_stat_shock_472(W, H, out):
    photo = Image.open(PHOTO_ROOT / "lush-vegas-backyard.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0  # clear Meta Reels/Stories top safe zone
    # On 9:16, content shifts down 8% — extend top scrim so tag region stays legible
    canvas = add_top_scrim(canvas, 0.70 if is_vertical else 0.55, max_alpha=225 if is_vertical else 215)
    canvas = add_bottom_scrim(canvas, 0.35, max_alpha=200)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Eyebrow
    eb_size = max(24, int(W * 0.030))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "VEGAS HOMEOWNERS, MEET YOUR NEW YARD",
                  eb_font, int(H * 0.05) + top_shift, W, (*GOLD, 240))

    # Big "472"
    big_size = int(W * 0.40)
    big_font = load_font(POPPINS_BLACK, big_size)
    big_y = int(H * 0.13) + top_shift
    draw_centered(draw, "472", big_font, big_y, W, WHITE)
    big_bottom = big_y + big_size

    # Sub line "VEGAS FAMILIES."
    sub_size = int(W * 0.072)
    sub_font = load_font(POPPINS_BLACK, sub_size)
    sub_y = big_bottom + int(H * 0.005)
    draw_centered(draw, "VEGAS FAMILIES.", sub_font, sub_y, W, WHITE)

    # 5 stars
    star_y = sub_y + sub_size + int(H * 0.025)
    star_size = int(W * 0.025)
    star_spacing = int(W * 0.06)
    star_total_w = star_spacing * 4
    star_x_start = (W - star_total_w) // 2
    for i in range(5):
        sx = star_x_start + i * star_spacing
        pts = []
        for j in range(10):
            ang = math.radians(-90 + j * 36)
            r = star_size if j % 2 == 0 else star_size * 0.4
            px = sx + r * math.cos(ang)
            py = star_y + star_size + r * math.sin(ang)
            pts.append((px, py))
        draw.polygon(pts, fill=GOLD)

    # Tag below stars — "[★] 4.7 on Google." with polygon star (Poppins lacks U+2605 glyph)
    tag_size = max(24, int(W * 0.034))
    tag_font = load_font(POPPINS_SEMI, tag_size)
    tag_y = star_y + star_size * 2 + int(H * 0.025)
    tag_color = (255, 255, 255, 230)
    rest_text = "4.7 on Google."
    rest_w = int(tag_font.getlength(rest_text))
    rest_bbox = tag_font.getbbox(rest_text)
    inline_star_r = int(tag_size * 0.42)
    star_gap = int(tag_size * 0.32)
    block_w = inline_star_r * 2 + star_gap + rest_w
    block_x = (W - block_w) // 2
    # Vertically center the polygon star with the text x-height (cap area)
    text_top_y = tag_y - rest_bbox[1]
    text_baseline = text_top_y + tag_font.getmetrics()[0]
    star_cy = text_top_y + (text_baseline - text_top_y) // 2 + int(tag_size * 0.05)
    draw_polygon_star(draw, block_x + inline_star_r, star_cy, inline_star_r, tag_color)
    draw.text((block_x + inline_star_r * 2 + star_gap, tag_y - rest_bbox[1]),
              rest_text, font=tag_font, fill=tag_color)
    draw_centered(draw, "Family-owned Vegas turf since 2003.",
                  tag_font, tag_y + tag_size + 8, W, tag_color)

    # CTA — only on square (1:1). Skip on 9:16 because Reels/Stories serve a native CTA sticker
    # that overlaps and competes with creative-baked CTAs (Meta safe-zone guidance).
    if not is_vertical:
        cta_h = max(80, int(H * 0.085))
        cta_w = min(int(W * 0.62), 720)
        cta_size = max(28, int(cta_h * 0.36))
        cta_font = load_font(POPPINS_BOLD, cta_size)
        cta_x = (W - cta_w) // 2
        cta_y = H - cta_h - int(H * 0.06)
        draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, "GET A FREE ESTIMATE",
                      USTURF_GREEN, WHITE, cta_font)

    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# V2: Rebate math equation — clean white card on photo background
# -----------------------------------------------------------------------------

def build_v2_rebate_math(W, H, out):
    photo = Image.open(PHOTO_ROOT / "lush-vegas-backyard.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=12))
    overlay = Image.new("RGBA", (W, H), (255, 255, 255, 80))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas, "RGBA")

    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    # Eyebrow
    eb_size = max(22, int(W * 0.028))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "VEGAS WATER REBATES",
                  eb_font, int(H * 0.06) + top_shift, W, USTURF_GREEN_DARK)

    # Main equation: $5 + $2 = $7/SQ.FT BACK
    # Layout: rows of [number] [+/=] [number] etc, with labels below
    eq_y = int(H * 0.18) + top_shift

    # Big "$5 + $2 = $7" centered
    main_size = int(W * 0.18)
    main_font = load_font(POPPINS_BLACK, main_size)
    eq_text = "$5 + $2 = $7"
    eq_w = int(main_font.getlength(eq_text))
    eq_x = (W - eq_w) // 2

    # Build piece by piece for color treatment
    pieces = [("$5", USTURF_GREEN_DARK), (" + ", BLACK),
              ("$2", USTURF_BLUE), (" = ", BLACK),
              ("$7", ORANGE_CTA)]
    cx = eq_x
    for txt, color in pieces:
        draw.text((cx, eq_y - main_font.getbbox(txt)[1]),
                  txt, font=main_font, fill=color)
        cx += int(main_font.getlength(txt))

    # Sub line below
    label_size = max(28, int(W * 0.042))
    label_font = load_font(POPPINS_BLACK, label_size)
    label_y = eq_y + main_size + int(H * 0.04)
    draw_centered(draw, "PER SQ.FT BACK.",
                  label_font, label_y, W, BLACK)

    # Detail rows
    detail_size = max(22, int(W * 0.030))
    detail_font = load_font(POPPINS_SEMI, detail_size)
    detail_y = label_y + label_size + int(H * 0.04)
    rows = [
        ("$5/sq.ft", "SNWA Water Smart Rebate"),
        ("$2/sq.ft", "LVVWD top-up (qualified areas)"),
    ]
    for amt, desc in rows:
        # Pill amount on left
        pill_w = int(detail_font.getlength(amt)) + 32
        pill_h = detail_size + 18
        pill_x = int(W * 0.10)
        draw.rounded_rectangle([(pill_x, detail_y),
                                (pill_x + pill_w, detail_y + pill_h)],
                               radius=pill_h // 2, fill=USTURF_GREEN)
        draw.text((pill_x + 16, detail_y + 8),
                  amt, font=detail_font, fill=WHITE)
        # Desc to right
        draw.text((pill_x + pill_w + 18, detail_y + 8),
                  desc, font=detail_font, fill=BLACK)
        detail_y += pill_h + 14

    # Reassurance
    reas_size = max(20, int(W * 0.026))
    reas_font = load_font(POPPINS_MED, reas_size)
    reas_y = detail_y + int(H * 0.02)
    draw_centered(draw, "We handle all the paperwork.",
                  reas_font, reas_y, W, (60, 60, 60))

    # CTA — only on square. Skip on 9:16 (Meta serves native CTA sticker for Reels/Stories)
    if not is_vertical:
        cta_h = max(90, int(H * 0.10))
        cta_w = min(int(W * 0.66), 760)
        cta_size = max(28, int(cta_h * 0.36))
        cta_font = load_font(POPPINS_BOLD, cta_size)
        cta_x = (W - cta_w) // 2
        cta_y = H - cta_h - int(H * 0.06)
        draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, "CLAIM YOUR REBATE",
                      USTURF_GREEN, WHITE, cta_font)

    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# V3: Payment Anchor — fullbleed photo + big $/mo callout
# -----------------------------------------------------------------------------

def build_v3_payment_anchor(W, H, out):
    photo = Image.open(PHOTO_ROOT / "lush-vegas-backyard.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    canvas = add_top_scrim(canvas, 0.55, max_alpha=215)
    canvas = add_bottom_scrim(canvas, 0.42, max_alpha=215)
    draw = ImageDraw.Draw(canvas, "RGBA")

    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    # Eyebrow
    eb_size = max(24, int(W * 0.030))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "0% INTEREST · 18 MONTHS",
                  eb_font, int(H * 0.05) + top_shift, W, (*GOLD, 240))

    # Top headline
    head_size = int(W * 0.072)
    head_font = load_font(POPPINS_BLACK, head_size)
    head_y = int(H * 0.12) + top_shift
    draw_centered(draw, "VEGAS YARDS FROM",
                  head_font, head_y, W, WHITE)

    # Big $166/mo
    big_size = int(W * 0.20)
    big_font = load_font(POPPINS_BLACK, big_size)
    big_y = head_y + head_size + int(H * 0.015)
    draw_centered(draw, "$166/MO", big_font, big_y, W, GOLD)

    # Math breakdown
    detail_size = max(22, int(W * 0.030))
    detail_font = load_font(POPPINS_SEMI, detail_size)
    detail_y = big_y + big_size + int(H * 0.025)
    draw_centered(draw, "Typical 600 sq.ft yard at $4.99/sq.ft",
                  detail_font, detail_y, W, (255, 255, 255, 230))
    draw_centered(draw, "= $2,994 ÷ 18 months",
                  detail_font, detail_y + detail_size + 12, W,
                  (255, 255, 255, 200))

    # CTA — only on square. Skip on 9:16 (Meta serves native CTA sticker for Reels/Stories)
    if not is_vertical:
        cta_h = max(90, int(H * 0.085))
        cta_w = min(int(W * 0.62), 720)
        cta_size = max(28, int(cta_h * 0.36))
        cta_font = load_font(POPPINS_BOLD, cta_size)
        cta_x = (W - cta_w) // 2
        cta_y = H - cta_h - int(H * 0.06)
        draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, "GET A FREE ESTIMATE",
                      USTURF_GREEN, WHITE, cta_font)

    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# V4: Longevity — fullbleed photo + 22 YEARS callout + EST 2003 stamp
# -----------------------------------------------------------------------------

def build_v4_longevity(W, H, out):
    photo = Image.open(PHOTO_ROOT / "family-on-turf.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    canvas = add_top_scrim(canvas, 0.55, max_alpha=220)
    canvas = add_bottom_scrim(canvas, 0.40, max_alpha=210)
    draw = ImageDraw.Draw(canvas, "RGBA")

    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    # Top: EST 2003 stamp (centered)
    stamp_size = max(22, int(W * 0.028))
    stamp_font = load_font(POPPINS_BOLD, stamp_size)
    draw_centered(draw, "EST. 2003 · LAS VEGAS, NV",
                  stamp_font, int(H * 0.05) + top_shift, W, (*GOLD, 240))

    # Big "22 YEARS."
    big_size = int(W * 0.155)
    big_font = load_font(POPPINS_BLACK, big_size)
    big_y = int(H * 0.13) + top_shift
    draw_centered(draw, "22 YEARS.", big_font, big_y, W, WHITE)

    # Mid: ONE FAMILY. ALL VEGAS.
    sub_size = int(W * 0.072)
    sub_font = load_font(POPPINS_BLACK, sub_size)
    sub_y = big_y + big_size + int(H * 0.005)
    draw_centered(draw, "ONE FAMILY.", sub_font, sub_y, W, WHITE)
    sub_y2 = sub_y + sub_size + 6
    draw_centered(draw, "ALL VEGAS.", sub_font, sub_y2, W, GOLD)

    # Sub-line
    detail_size = max(22, int(W * 0.030))
    detail_font = load_font(POPPINS_SEMI, detail_size)
    detail_y = sub_y2 + sub_size + int(H * 0.04)
    draw_centered(draw, "Installing artificial turf in the Mojave since 2003.",
                  detail_font, detail_y, W, (255, 255, 255, 230))
    draw_centered(draw, "Built for the desert. Built to last.",
                  detail_font, detail_y + detail_size + 12, W,
                  (255, 255, 255, 230))

    # CTA — only on square. Skip on 9:16 (Meta serves native CTA sticker for Reels/Stories)
    if not is_vertical:
        cta_h = max(90, int(H * 0.085))
        cta_w = min(int(W * 0.62), 720)
        cta_size = max(28, int(cta_h * 0.36))
        cta_font = load_font(POPPINS_BOLD, cta_size)
        cta_x = (W - cta_w) // 2
        cta_y = H - cta_h - int(H * 0.06)
        draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, "GET A FREE ESTIMATE",
                      USTURF_GREEN, WHITE, cta_font)

    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# V5: License Trust Block — 4-cell grid on cream background
# -----------------------------------------------------------------------------

def build_v5_licenses(W, H, out):
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas, "RGBA")

    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    pad_x = int(W * 0.07)

    # Top eyebrow
    eb_size = max(22, int(W * 0.028))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "FULLY LICENSED. FULLY VETTED.",
                  eb_font, int(H * 0.05) + top_shift, W, USTURF_GREEN_DARK)

    # Headline
    head_size = int(W * 0.083)
    head_font = load_font(POPPINS_BLACK, head_size)
    head_y = int(H * 0.10) + top_shift
    draw_centered(draw, "B2 · C3 · C4 · C10.",
                  head_font, head_y, W, BLACK)

    # Sub
    sub_size = max(22, int(W * 0.030))
    sub_font = load_font(POPPINS_SEMI, sub_size)
    sub_y = head_y + head_size + int(H * 0.02)
    draw_centered(draw, "4 Nevada contractor licenses.",
                  sub_font, sub_y, W, (60, 60, 60))
    draw_centered(draw, "Most turf companies have one.",
                  sub_font, sub_y + sub_size + 8, W, (60, 60, 60))

    # 4 license cards in a 2x2 grid
    grid_y_start = sub_y + (sub_size + 8) * 2 + int(H * 0.04)
    grid_h_total = int(H * 0.40)
    cell_pad = int(W * 0.025)
    if H > W * 1.5:
        # 2x2 vertical
        cell_w = (W - pad_x * 2 - cell_pad) // 2
        cell_h = (grid_h_total - cell_pad) // 2
        coords = [
            (pad_x, grid_y_start),
            (pad_x + cell_w + cell_pad, grid_y_start),
            (pad_x, grid_y_start + cell_h + cell_pad),
            (pad_x + cell_w + cell_pad, grid_y_start + cell_h + cell_pad),
        ]
    else:
        # 2x2 square
        cell_w = (W - pad_x * 2 - cell_pad) // 2
        cell_h = (grid_h_total - cell_pad) // 2
        coords = [
            (pad_x, grid_y_start),
            (pad_x + cell_w + cell_pad, grid_y_start),
            (pad_x, grid_y_start + cell_h + cell_pad),
            (pad_x + cell_w + cell_pad, grid_y_start + cell_h + cell_pad),
        ]

    licenses = [
        ("B2", "0081302"),
        ("C3", "0081384"),
        ("C4", "0081385"),
        ("C10", "0089330"),
    ]

    cls_size = int(W * 0.075)
    cls_font = load_font(POPPINS_BLACK, cls_size)
    num_size = max(22, int(W * 0.034))
    num_font = load_font(POPPINS_SEMI, num_size)

    for (cls, num), (cx, cy) in zip(licenses, coords):
        # Card with shadow
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle([(cx + 4, cy + 6),
                              (cx + cell_w + 4, cy + cell_h + 6)],
                             radius=18, fill=(0, 0, 0, 80))
        shadow = shadow.filter(ImageFilter.GaussianBlur(8))
        canvas_rgba = canvas.convert("RGBA")
        canvas_rgba.alpha_composite(shadow)
        canvas = canvas_rgba.convert("RGB")
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rounded_rectangle([(cx, cy), (cx + cell_w, cy + cell_h)],
                               radius=18, fill=WHITE,
                               outline=USTURF_GREEN, width=3)
        # Class big
        cls_w = int(cls_font.getlength(cls))
        bbox = cls_font.getbbox(cls)
        cls_text_y = cy + int(cell_h * 0.18) - bbox[1]
        draw.text((cx + (cell_w - cls_w) // 2, cls_text_y),
                  cls, font=cls_font, fill=USTURF_GREEN_DARK)
        # NV # below
        nv_label_size = max(16, int(W * 0.022))
        nv_label_font = load_font(POPPINS_MED, nv_label_size)
        nv_label_y = cls_text_y + cls_size + int(cell_h * 0.10)
        draw_box_w = cell_w
        # "NV LICENSE #"
        nv_text = "NV LICENSE #"
        nv_w = int(nv_label_font.getlength(nv_text))
        draw.text((cx + (cell_w - nv_w) // 2, nv_label_y),
                  nv_text, font=nv_label_font, fill=DIM_GREY)
        # Number
        num_y = nv_label_y + nv_label_size + 6
        num_text_w = int(num_font.getlength(num))
        draw.text((cx + (cell_w - num_text_w) // 2, num_y),
                  num, font=num_font, fill=BLACK)

    # CTA — only on square. Skip on 9:16 (Meta serves native CTA sticker for Reels/Stories)
    if not is_vertical:
        cta_h = max(90, int(H * 0.085))
        cta_w = min(int(W * 0.62), 720)
        cta_size = max(28, int(cta_h * 0.36))
        cta_font = load_font(POPPINS_BOLD, cta_size)
        cta_x = (W - cta_w) // 2
        cta_y = H - cta_h - int(H * 0.06)
        draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, "GET A FREE ESTIMATE",
                      USTURF_GREEN, WHITE, cta_font)

    canvas.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# V6: Lifetime vs 10-Year — comparison columns
# -----------------------------------------------------------------------------

def build_v6_warranty_compare(W, H, out):
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas, "RGBA")

    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    pad_x = int(W * 0.07)

    # Eyebrow
    eb_size = max(22, int(W * 0.028))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "ARTIFICIAL TURF WARRANTY",
                  eb_font, int(H * 0.05) + top_shift, W, USTURF_GREEN_DARK)

    # Headline
    head_size = int(W * 0.10)
    head_font = load_font(POPPINS_BLACK, head_size)
    head_y = int(H * 0.10) + top_shift
    draw_centered(draw, "LIFETIME.", head_font, head_y, W, USTURF_GREEN_DARK)
    head_y2 = head_y + head_size + 8
    draw_centered(draw, "NOT 10 YEARS.", head_font, head_y2, W, BLACK)

    # Two-column comparison
    comp_y = head_y2 + head_size + int(H * 0.04)
    col_h = int(H * 0.32)
    col_w = (W - pad_x * 2 - int(W * 0.03)) // 2
    col_pad = int(W * 0.03)

    # Left column — "OTHER VEGAS INSTALLERS" gray X 10-YEAR
    left_x = pad_x
    draw.rounded_rectangle([(left_x, comp_y),
                            (left_x + col_w, comp_y + col_h)],
                           radius=18, fill=(238, 238, 238), outline=DIM_GREY, width=2)
    # Top label
    sub_label_size = max(18, int(W * 0.024))
    sub_label_font = load_font(POPPINS_BOLD, sub_label_size)
    draw_centered(draw, "OTHERS", sub_label_font,
                  comp_y + int(col_h * 0.10), col_w + 2 * left_x, DIM_GREY)
    # Big "10"
    big_n_size = int(W * 0.16)
    big_n_font = load_font(POPPINS_BLACK, big_n_size)
    big_n = "10"
    big_n_w = int(big_n_font.getlength(big_n))
    bbox = big_n_font.getbbox(big_n)
    big_n_y = comp_y + int(col_h * 0.30)
    draw.text((left_x + (col_w - big_n_w) // 2, big_n_y - bbox[1]),
              big_n, font=big_n_font, fill=DIM_GREY)
    # YEAR label
    year_size = max(22, int(W * 0.030))
    year_font = load_font(POPPINS_BLACK, year_size)
    year_y = big_n_y + big_n_size + 6
    draw_centered(draw, "YEAR WARRANTY",
                  year_font, year_y, col_w + 2 * left_x, DIM_GREY)

    # Right column — "US TURF" green check LIFETIME
    right_x = pad_x + col_w + col_pad
    draw.rounded_rectangle([(right_x, comp_y),
                            (right_x + col_w, comp_y + col_h)],
                           radius=18, fill=USTURF_GREEN, outline=USTURF_GREEN_DARK, width=3)
    # Label
    label_w_offset = right_x - left_x  # offset for centering on right column
    # Use a tweak: draw centered relative to right column manually
    rl_text = "US TURF"
    rl_w = int(sub_label_font.getlength(rl_text))
    draw.text((right_x + (col_w - rl_w) // 2, comp_y + int(col_h * 0.10) - sub_label_font.getbbox(rl_text)[1]),
              rl_text, font=sub_label_font, fill=WHITE)
    # Big "∞" (use a giant green check via large glyph; fall back to LIFETIME text fit)
    life_text = "LIFETIME"
    # Fit LIFETIME within col_w
    life_size = big_n_size
    life_font = load_font(POPPINS_BLACK, life_size)
    while int(life_font.getlength(life_text)) > col_w - 40 and life_size > 40:
        life_size -= 6
        life_font = load_font(POPPINS_BLACK, life_size)
    life_w = int(life_font.getlength(life_text))
    bbox_l = life_font.getbbox(life_text)
    # Vertically center within where the big_n was
    life_y = big_n_y + (big_n_size - life_size) // 2
    draw.text((right_x + (col_w - life_w) // 2, life_y - bbox_l[1]),
              life_text, font=life_font, fill=WHITE)
    # WARRANTY label
    time_text = "WARRANTY"
    time_w = int(year_font.getlength(time_text))
    draw.text((right_x + (col_w - time_w) // 2, year_y - year_font.getbbox(time_text)[1]),
              time_text, font=year_font, fill=WHITE)

    # Reassurance
    reas_size = max(20, int(W * 0.026))
    reas_font = load_font(POPPINS_MED, reas_size)
    reas_y = comp_y + col_h + int(H * 0.04)
    draw_centered(draw, "Lifetime warranty included on every US Turf install.",
                  reas_font, reas_y, W, (60, 60, 60))

    # CTA — only on square. Skip on 9:16 (Meta serves native CTA sticker for Reels/Stories)
    if not is_vertical:
        cta_h = max(90, int(H * 0.085))
        cta_w = min(int(W * 0.62), 720)
        cta_size = max(28, int(cta_h * 0.36))
        cta_font = load_font(POPPINS_BOLD, cta_size)
        cta_x = (W - cta_w) // 2
        cta_y = H - cta_h - int(H * 0.06)
        draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, "GET A FREE ESTIMATE",
                      USTURF_GREEN, WHITE, cta_font)

    canvas.save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

RATIOS = {
    "1x1": (1080, 1080),
    "9x16": (1080, 1920),
}


def for_each(name, build_fn):
    for ratio, (W, H) in RATIOS.items():
        out = OUT / ratio / f"{name}-{ratio}.png"
        build_fn(W, H, out)


def main():
    print("Building Phase 2 batch — 6 variants × 2 ratios = 12 images")
    for_each("V1-stat-shock-472-families", build_v1_stat_shock_472)
    for_each("V2-rebate-math-7-back", build_v2_rebate_math)
    for_each("V3-payment-anchor-166mo", build_v3_payment_anchor)
    for_each("V4-longevity-22-years", build_v4_longevity)
    for_each("V5-trust-block-4-licenses", build_v5_licenses)
    for_each("V6-warranty-lifetime-vs-10yr", build_v6_warranty_compare)
    print(f"\nDone. → {OUT}/")


if __name__ == "__main__":
    main()
