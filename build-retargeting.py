#!/usr/bin/env python3
"""US Turf — Phase 4 Retargeting Batch builder.

Generates 5 retargeting ad variants from the May 2026 competitor teardown
(R1-R5) targeting warm audiences who visited social2026 LP and didn't convert.

R1: Still green at 115°F   — heat survival objection
R2: $5 + $2 = $7 rebate    — rebate trust objection
R3: Vegas dogs deserve better — pet durability objection (REVISED 2026-05-07)
R4: We build the whole backyard — full-yard upsell objection
R5: $1.80 vs $5.50 vs $4.99 — quality-tier anchor objection (REVISED 2026-05-07)

Output: 5 variants × {1:1, 9:16} = 10 PNGs in renders/ad-batch/may2026-retargeting/
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

POPPINS_BLACK = "/tmp/ad-fonts/Poppins-Black.ttf"
POPPINS_BOLD = "/tmp/ad-fonts/Poppins-Bold.ttf"
POPPINS_SEMI = "/tmp/ad-fonts/Poppins-SemiBold.ttf"
POPPINS_REG = "/tmp/ad-fonts/Poppins-Regular.ttf"
POPPINS_MED = "/tmp/ad-fonts/Poppins-Medium.ttf"

REPO_ROOT = Path(__file__).parent
PHOTO_ROOT = Path("/Users/kylesimmons/.claude/skills/product-visual-generator/brands/usturf/competitor-assets")
OUT = REPO_ROOT / "renders" / "ad-batch" / "may2026-retargeting"
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


# --- Shared helpers (mirrored from build-batch.py for self-contained Phase 4) ---

def load_font(path, size):
    return ImageFont.truetype(path, size)


def draw_polygon_star(draw, cx, cy, r, fill):
    pts = []
    for j in range(10):
        ang = math.radians(-90 + j * 36)
        rr = r if j % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


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


def add_band_scrim(canvas, y_start, y_end, max_alpha=170, fade=80):
    W, H = canvas.size
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    fade_top = max(0, y_start - fade)
    for i in range(y_start - fade_top):
        a = int(max_alpha * (i / max(1, fade)))
        gd.line([(0, fade_top + i), (W, fade_top + i)], fill=(0, 0, 0, a))
    gd.rectangle([(0, y_start), (W, y_end)], fill=(0, 0, 0, max_alpha))
    fade_bot_end = min(H, y_end + fade)
    for i in range(fade_bot_end - y_end):
        a = int(max_alpha * (1 - i / max(1, fade)))
        gd.line([(0, y_end + i), (W, y_end + i)], fill=(0, 0, 0, a))
    if canvas.mode != "RGBA":
        canvas = canvas.convert("RGBA")
    canvas.alpha_composite(grad)
    return canvas


def draw_chip(draw, x, y, w, h, text, font, fill_bg, fill_text, radius=None):
    if radius is None:
        radius = h // 2
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, fill=fill_bg)
    text_w = int(font.getlength(text))
    bbox = font.getbbox(text)
    tx = x + (w - text_w) // 2
    ty = y + (h - (bbox[3] - bbox[1])) // 2 - bbox[1]
    draw.text((tx, ty), text, font=font, fill=fill_text)


def add_cta_block(canvas, is_vertical, label):
    """Add a green CTA pill at the bottom — only on 1:1, never 9:16
    (Meta serves native CTA sticker on Reels/Stories)."""
    if is_vertical:
        return
    W, H = canvas.size
    cta_h = max(90, int(H * 0.085))
    cta_w = min(int(W * 0.62), 720)
    cta_size = max(28, int(cta_h * 0.36))
    cta_font = load_font(POPPINS_BOLD, cta_size)
    cta_x = (W - cta_w) // 2
    cta_y = H - cta_h - int(H * 0.06)
    draw_cta_pill(canvas, cta_x, cta_y, cta_w, cta_h, label,
                  USTURF_GREEN, WHITE, cta_font)


# -----------------------------------------------------------------------------
# R1: Heat Survival — fullbleed photo + headline + thermometer chip
# -----------------------------------------------------------------------------

def build_r1_heat_115(W, H, out):
    photo = Image.open(PHOTO_ROOT / "lush-vegas-backyard.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    # Precompute key positions for band scrim
    eb_y_pre = int(H * 0.05) + top_shift
    big_size_pre = int(W * 0.155)
    big_y_pre = int(H * 0.13) + top_shift
    sub_size_pre = int(W * 0.072)
    sub_y_pre = (big_y_pre + big_size_pre) + int(H * 0.01)
    detail_size_pre = max(22, int(W * 0.030))
    detail_y_pre = sub_y_pre + sub_size_pre + int(H * 0.04)
    detail_end_y = detail_y_pre + (detail_size_pre + 12) * 3

    canvas = add_top_scrim(canvas, 0.78 if is_vertical else 0.65,
                           max_alpha=235 if is_vertical else 230)
    canvas = add_bottom_scrim(canvas, 0.40, max_alpha=200)
    # Band scrim behind sub + detail block on BOTH ratios (sun-lit turf otherwise drowns text)
    band_top = sub_y_pre - int(H * 0.025)
    band_bot = detail_end_y + int(H * 0.020)
    canvas = add_band_scrim(canvas, band_top, band_bot,
                            max_alpha=160 if is_vertical else 150,
                            fade=int(H * 0.04))
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Eyebrow
    eb_size = max(24, int(W * 0.030))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "THE VEGAS HEAT TEST",
                  eb_font, eb_y_pre, W, (*GOLD, 240))

    # Big headline "STILL GREEN."
    big_font = load_font(POPPINS_BLACK, big_size_pre)
    draw_centered(draw, "STILL GREEN.", big_font, big_y_pre, W, WHITE)

    # Sub line "AT 115°F." (gold accent)
    sub_font = load_font(POPPINS_BLACK, sub_size_pre)
    draw_centered(draw, "AT 115°F.", sub_font, sub_y_pre, W, GOLD)

    # Detail
    detail_font = load_font(POPPINS_SEMI, detail_size_pre)
    draw_centered(draw, "One full Mojave summer old.",
                  detail_font, detail_y_pre, W, (255, 255, 255, 230))
    draw_centered(draw, "Same lawn. Same color.",
                  detail_font, detail_y_pre + detail_size_pre + 12, W,
                  (255, 255, 255, 230))
    draw_centered(draw, "Lifetime warranty.",
                  detail_font, detail_y_pre + (detail_size_pre + 12) * 2, W,
                  (255, 255, 255, 230))

    # Thermometer chip top-right
    chip_w = int(W * 0.16)
    chip_h = int(W * 0.055)
    chip_x = W - chip_w - int(W * 0.05)
    chip_y = eb_y_pre + int(H * 0.005)
    chip_font = load_font(POPPINS_BLACK, max(20, int(W * 0.030)))
    draw_chip(draw, chip_x, chip_y, chip_w, chip_h, "115°F",
              chip_font, RED, WHITE)

    add_cta_block(canvas, is_vertical, "GET A FREE ESTIMATE")
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# R2: Rebate Trust — cream card with $5 + $2 = $7 math (mirrors V2 layout)
# -----------------------------------------------------------------------------

def build_r2_rebate_paperwork(W, H, out):
    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    photo = Image.open(PHOTO_ROOT / "lush-vegas-backyard.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=12))
    overlay = Image.new("RGBA", (W, H), (255, 255, 255, 80))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Eyebrow
    eb_size = max(22, int(W * 0.028))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "WE FILE THE PAPERWORK",
                  eb_font, int(H * 0.06) + top_shift, W, USTURF_GREEN_DARK)

    # Top label
    label_size = max(28, int(W * 0.052))
    label_font = load_font(POPPINS_BLACK, label_size)
    label_y = int(H * 0.13) + top_shift
    draw_centered(draw, "YOUR $7/SQ.FT REBATE.", label_font, label_y, W, BLACK)

    # Big "$5 + $2 = $7"
    eq_y = label_y + label_size + int(H * 0.04)
    main_size = int(W * 0.18)
    main_font = load_font(POPPINS_BLACK, main_size)
    eq_text = "$5 + $2 = $7"
    eq_w = int(main_font.getlength(eq_text))
    eq_x = (W - eq_w) // 2
    pieces = [("$5", USTURF_GREEN_DARK), (" + ", BLACK),
              ("$2", USTURF_BLUE), (" = ", BLACK),
              ("$7", ORANGE_CTA)]
    cx = eq_x
    for txt, color in pieces:
        bbox = main_font.getbbox(txt)
        draw.text((cx, eq_y - bbox[1]), txt, font=main_font, fill=color)
        cx += int(main_font.getlength(txt))

    # Detail rows
    detail_size = max(22, int(W * 0.028))
    detail_font = load_font(POPPINS_SEMI, detail_size)
    detail_y = eq_y + main_size + int(H * 0.04)
    rows = [
        ("$5/sq.ft", "SNWA Water Smart Rebate"),
        ("$2/sq.ft", "LVVWD top-up (qualified areas)"),
    ]
    for amt, desc in rows:
        pill_w = int(detail_font.getlength(amt)) + 32
        pill_h = detail_size + 18
        pill_x = int(W * 0.10)
        draw.rounded_rectangle([(pill_x, detail_y),
                                (pill_x + pill_w, detail_y + pill_h)],
                               radius=pill_h // 2, fill=USTURF_GREEN)
        draw.text((pill_x + 16, detail_y + 8),
                  amt, font=detail_font, fill=WHITE)
        draw.text((pill_x + pill_w + 18, detail_y + 8),
                  desc, font=detail_font, fill=BLACK)
        detail_y += pill_h + 14

    # Reassurance
    reas_size = max(20, int(W * 0.026))
    reas_font = load_font(POPPINS_MED, reas_size)
    reas_y = detail_y + int(H * 0.02)
    draw_centered(draw, "We file every form.",
                  reas_font, reas_y, W, (60, 60, 60))
    draw_centered(draw, "You sign and bank the check.",
                  reas_font, reas_y + reas_size + 10, W, (60, 60, 60))

    add_cta_block(canvas, is_vertical, "CLAIM YOUR REBATE")
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# R3: Pet Durability — fullbleed family/dog photo + cooling claim
# -----------------------------------------------------------------------------

def build_r3_dogs(W, H, out):
    photo = Image.open(PHOTO_ROOT / "family-on-turf.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    # Precompute positions
    eb_y_pre = int(H * 0.05) + top_shift
    big_size_pre = int(W * 0.105) if not is_vertical else int(W * 0.115)
    big_y_pre = int(H * 0.13) + top_shift
    detail_size_pre = max(22, int(W * 0.028))
    # Headline takes 2 lines: "VEGAS DOGS" / "DESERVE BETTER."
    headline_block_h = (big_size_pre + 6) * 2
    detail_y_pre = big_y_pre + headline_block_h + int(H * 0.04)
    detail_block_h = (detail_size_pre + 12) * 4  # up to 4 lines of sub-line
    detail_end_y = detail_y_pre + detail_block_h

    canvas = add_top_scrim(canvas, 0.80 if is_vertical else 0.65,
                           max_alpha=240 if is_vertical else 230)
    canvas = add_bottom_scrim(canvas, 0.40, max_alpha=210)
    # Band scrim behind sub-line on BOTH ratios (R3 family/dog photo is bright)
    band_top = detail_y_pre - int(H * 0.025)
    band_bot = detail_end_y + int(H * 0.020)
    canvas = add_band_scrim(canvas, band_top, band_bot,
                            max_alpha=170 if is_vertical else 160,
                            fade=int(H * 0.04))
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Eyebrow
    eb_size = max(24, int(W * 0.030))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "BUILT FOR DESERT PAWS",
                  eb_font, eb_y_pre, W, (*GOLD, 240))

    # Headline (2 lines)
    big_font = load_font(POPPINS_BLACK, big_size_pre)
    draw_centered(draw, "VEGAS DOGS", big_font, big_y_pre, W, WHITE)
    draw_centered(draw, "DESERVE BETTER.",
                  big_font, big_y_pre + big_size_pre + 6, W, GOLD)

    # Sub-line (wraps to multiple lines)
    detail_font = load_font(POPPINS_SEMI, detail_size_pre)
    sub_text = ("20% cooler than concrete on hot paws. Pet-safe infill. "
                "We carry maintenance kits in-house — or partner with "
                "Cleaner Turf for full-service upkeep.")
    pad_x = int(W * 0.07)
    sub_lines = wrap(sub_text, detail_font, W - pad_x * 2)
    sy = detail_y_pre
    for sl in sub_lines:
        draw_centered(draw, sl, detail_font, sy, W, (255, 255, 255, 230))
        sy += detail_size_pre + 12

    add_cta_block(canvas, is_vertical, "GET A FREE ESTIMATE")
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# R4: Full-Yard Upsell — wide install hero + license chip row
# -----------------------------------------------------------------------------

def build_r4_full_yard(W, H, out):
    photo = Image.open(PHOTO_ROOT / "lush-vegas-backyard.png").convert("RGBA")
    canvas = fit_cover(photo, W, H).convert("RGBA")
    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0

    eb_y_pre = int(H * 0.05) + top_shift
    # Auto-fit headline so "THE WHOLE BACKYARD." doesn't crop
    big_size_pre = int(W * 0.080)
    big_y_pre = int(H * 0.12) + top_shift

    # Precompute layout for band scrim
    detail_size_pre = max(22, int(W * 0.030))
    detail_y_pre = big_y_pre + big_size_pre * 2 + int(H * 0.04)
    chip_font_size_pre = max(16, int(W * 0.024))
    chip_h_pre = chip_font_size_pre + 22
    detail_block_h = (detail_size_pre + 12) * 2  # 2 wrapped sub-lines
    chip_y_pre = detail_y_pre + detail_block_h + int(H * 0.025)
    band_bot_y = chip_y_pre + chip_h_pre + int(H * 0.020)

    canvas = add_top_scrim(canvas, 0.78 if is_vertical else 0.65,
                           max_alpha=235 if is_vertical else 230)
    canvas = add_bottom_scrim(canvas, 0.42, max_alpha=215)
    # Band scrim behind sub + license chips on both ratios
    band_top = detail_y_pre - int(H * 0.025)
    canvas = add_band_scrim(canvas, band_top, band_bot_y,
                            max_alpha=160 if is_vertical else 150,
                            fade=int(H * 0.04))
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Eyebrow
    eb_size = max(22, int(W * 0.028))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "TURF · PAVERS · LIGHTING · IRRIGATION",
                  eb_font, eb_y_pre, W, (*GOLD, 240))

    # Headline (2 lines) — auto-shrink if "THE WHOLE BACKYARD." would overflow
    pad_x = int(W * 0.06)
    big_font = load_font(POPPINS_BLACK, big_size_pre)
    while int(big_font.getlength("THE WHOLE BACKYARD.")) > W - pad_x * 2 and big_size_pre > 50:
        big_size_pre -= 4
        big_font = load_font(POPPINS_BLACK, big_size_pre)
    draw_centered(draw, "WE BUILD",
                  big_font, big_y_pre, W, WHITE)
    draw_centered(draw, "THE WHOLE BACKYARD.",
                  big_font, big_y_pre + big_size_pre + 6, W, WHITE)

    # Sub line
    detail_font = load_font(POPPINS_SEMI, detail_size_pre)
    sub_text = ("One install team. Full Vegas backyard transformations. "
                "4 NV contractor licenses for the whole job.")
    sub_lines = wrap(sub_text, detail_font, W - pad_x * 2)
    sy = detail_y_pre
    for sl in sub_lines:
        draw_centered(draw, sl, detail_font, sy, W, (255, 255, 255, 235))
        sy += detail_size_pre + 12

    # License chip row — B2 · C3 · C4 · C10. Use solid dark backdrop so white text reads.
    chip_y = sy + int(H * 0.025)
    chip_font = load_font(POPPINS_BLACK, chip_font_size_pre)
    chips = ["B2", "C3", "C4", "C10"]
    chip_h = chip_h_pre
    chip_pad = int(W * 0.020)
    chip_widths = [int(chip_font.getlength(c)) + 32 for c in chips]
    total_chips_w = sum(chip_widths) + chip_pad * (len(chips) - 1)
    cx = (W - total_chips_w) // 2
    for c, cw in zip(chips, chip_widths):
        # Solid dark backdrop with subtle white outline (frosted-glass approximation)
        draw.rounded_rectangle([(cx, chip_y), (cx + cw, chip_y + chip_h)],
                               radius=10, fill=(0, 0, 0, 140),
                               outline=(255, 255, 255, 200), width=2)
        text_w = int(chip_font.getlength(c))
        bbox = chip_font.getbbox(c)
        tx = cx + (cw - text_w) // 2
        ty = chip_y + (chip_h - (bbox[3] - bbox[1])) // 2 - bbox[1]
        draw.text((tx, ty), c, font=chip_font, fill=WHITE)
        cx += cw + chip_pad

    add_cta_block(canvas, is_vertical, "GET A FREE ESTIMATE")
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ✓ {out.name}")


# -----------------------------------------------------------------------------
# R5: Quality-Tier Anchor — 3-column comparison card
# -----------------------------------------------------------------------------

def build_r5_pricing_compare(W, H, out):
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas, "RGBA")

    is_vertical = H > W * 1.5
    top_shift = int(H * 0.08) if is_vertical else 0
    pad_x = int(W * 0.05)

    tiers = [
        {
            "label": "BUDGET DIY",
            "label_color": DIM_GREY,
            "price": "$1.80",
            "price_color": DIM_GREY,
            "bg": (238, 238, 238),
            "outline": DIM_GREY,
            "details": ["5-yr warranty", "Fades in 2", "Vegas summers"],
            "detail_color": DIM_GREY,
            "detail_one_line": "5-yr warranty · Fades in 2 summers",
        },
        {
            "label": "PREMIUM",
            "label_color": (130, 100, 0),
            "price": "$5.50+",
            "price_color": (165, 130, 0),
            "bg": (255, 246, 220),
            "outline": GOLD,
            "details": ["Lifetime", "warranty", "(installer-grade)"],
            "detail_color": (90, 70, 0),
            "detail_one_line": "Lifetime warranty · Installer-grade",
        },
        {
            "label": "US TURF",
            "label_color": WHITE,
            "price": "$4.99+",
            "price_color": WHITE,
            "bg": USTURF_GREEN,
            "outline": USTURF_GREEN_DARK,
            "details": ["Lifetime warranty", "+ SNWA rebate", "+ 472 Google reviews"],
            "detail_color": WHITE,
            "detail_one_line": "Lifetime + SNWA rebate + 472 reviews",
        },
    ]

    # Eyebrow
    eb_size = max(22, int(W * 0.028))
    eb_font = load_font(POPPINS_BOLD, eb_size)
    draw_centered(draw, "NOT ALL TURF IS EQUAL",
                  eb_font, int(H * 0.05) + top_shift, W, USTURF_GREEN_DARK)

    if is_vertical:
        # ============ 9:16 layout — STACKED ROWS ============
        # Headline: "$1.80" / "vs $5.50" / "vs $4.99." stacked or just smaller
        head_size = int(W * 0.075)
        head_font = load_font(POPPINS_BLACK, head_size)
        head_text = "$1.80 vs $5.50 vs $4.99."
        # Auto-shrink to fit
        while int(head_font.getlength(head_text)) > W - pad_x * 2 and head_size > 32:
            head_size -= 3
            head_font = load_font(POPPINS_BLACK, head_size)
        head_y = int(H * 0.105) + top_shift
        draw_centered(draw, head_text, head_font, head_y, W, BLACK)

        # 3 stacked horizontal cards
        rows_y = head_y + head_size + int(H * 0.04)
        row_pad = int(W * 0.025)
        row_h = int(H * 0.13)
        # Available height for 3 rows: rows_y to ~80% of canvas
        avail_h = int(H * 0.80) - rows_y
        row_h = min(row_h, (avail_h - row_pad * 2) // 3)

        label_size = max(18, int(W * 0.026))
        label_font = load_font(POPPINS_BOLD, label_size)
        # Smaller price font for stacked layout (price already echoed in headline above)
        price_size = max(30, int(W * 0.052))
        price_font = load_font(POPPINS_BLACK, price_size)
        sqft_size = max(14, int(W * 0.018))
        sqft_font = load_font(POPPINS_SEMI, sqft_size)
        detail_size = max(15, int(W * 0.022))
        detail_font = load_font(POPPINS_SEMI, detail_size)

        # Width allocation: detail block = 55% of W, price block = 35% of W, 10% padding/gap
        detail_max_w = int(W * 0.55) - pad_x - int(W * 0.04)
        price_max_w = int(W * 0.35)

        for i, tier in enumerate(tiers):
            ry = rows_y + i * (row_h + row_pad)
            # Card
            draw.rounded_rectangle([(pad_x, ry), (W - pad_x, ry + row_h)],
                                   radius=16, fill=tier["bg"],
                                   outline=tier["outline"], width=3)
            # Left: label (top) + detail (bottom) — left-aligned
            inner_pad = int(W * 0.04)
            label_x = pad_x + inner_pad
            label_y = ry + int(row_h * 0.18)
            lbbox = label_font.getbbox(tier["label"])
            draw.text((label_x, label_y - lbbox[1]),
                      tier["label"], font=label_font, fill=tier["label_color"])
            # Detail one-liner — auto-fit to detail_max_w
            detail_y = ry + int(row_h * 0.58)
            d_size = detail_size
            d_font = detail_font
            while int(d_font.getlength(tier["detail_one_line"])) > detail_max_w and d_size > 12:
                d_size -= 1
                d_font = load_font(POPPINS_SEMI, d_size)
            dbbox = d_font.getbbox(tier["detail_one_line"])
            draw.text((label_x, detail_y - dbbox[1]),
                      tier["detail_one_line"], font=d_font, fill=tier["detail_color"])

            # Right: price + /sq.ft (right-aligned) — auto-fit to price_max_w
            price_x_right = W - pad_x - inner_pad
            p_size = price_size
            p_font = price_font
            while int(p_font.getlength(tier["price"])) > price_max_w and p_size > 22:
                p_size -= 2
                p_font = load_font(POPPINS_BLACK, p_size)
            pw = int(p_font.getlength(tier["price"]))
            pbbox = p_font.getbbox(tier["price"])
            price_y = ry + (row_h - p_size) // 2 - 6
            draw.text((price_x_right - pw, price_y - pbbox[1]),
                      tier["price"], font=p_font, fill=tier["price_color"])
            # /sq.ft below price, right-aligned
            sqft_text = "/sq.ft"
            sw = int(sqft_font.getlength(sqft_text))
            draw.text((price_x_right - sw, price_y - pbbox[1] + p_size + 2),
                      sqft_text, font=sqft_font, fill=tier["price_color"])

        # Disclaimer
        disc_size = max(13, int(W * 0.018))
        disc_font = load_font(POPPINS_MED, disc_size)
        disc_y = rows_y + (row_h + row_pad) * 3 + int(H * 0.015)
        draw_centered(draw, "*Pricing varies by project size, scope, and signed estimate.",
                      disc_font, disc_y, W, (110, 110, 110))

    else:
        # ============ 1:1 layout — 3 COLUMNS (unchanged) ============
        head_size = int(W * 0.078)
        head_font = load_font(POPPINS_BLACK, head_size)
        head_y = int(H * 0.10)
        draw_centered(draw, "$1.80  vs  $5.50  vs  $4.99.",
                      head_font, head_y, W, BLACK)

        cols_y = head_y + head_size + int(H * 0.05)
        col_h = int(H * 0.50)
        col_pad = int(W * 0.018)
        col_w = (W - pad_x * 2 - col_pad * 2) // 3

        label_size = max(18, int(W * 0.024))
        label_font = load_font(POPPINS_BOLD, label_size)
        price_size = max(28, int(W * 0.052))
        price_font = load_font(POPPINS_BLACK, price_size)
        detail_size = max(15, int(W * 0.020))
        detail_font = load_font(POPPINS_SEMI, detail_size)

        for i, col in enumerate(tiers):
            cx = pad_x + i * (col_w + col_pad)
            draw.rounded_rectangle([(cx, cols_y), (cx + col_w, cols_y + col_h)],
                                   radius=18, fill=col["bg"],
                                   outline=col["outline"], width=3)
            lw = int(label_font.getlength(col["label"]))
            lbbox = label_font.getbbox(col["label"])
            ly = cols_y + int(col_h * 0.10) - lbbox[1]
            draw.text((cx + (col_w - lw) // 2, ly),
                      col["label"], font=label_font, fill=col["label_color"])
            fit_size = price_size
            fit_font = price_font
            while int(fit_font.getlength(col["price"])) > col_w - 28 and fit_size > 22:
                fit_size -= 4
                fit_font = load_font(POPPINS_BLACK, fit_size)
            pw = int(fit_font.getlength(col["price"]))
            pbbox = fit_font.getbbox(col["price"])
            py = cols_y + int(col_h * 0.32) - pbbox[1]
            draw.text((cx + (col_w - pw) // 2, py),
                      col["price"], font=fit_font, fill=col["price_color"])
            sqft_size = max(12, int(W * 0.016))
            sqft_font = load_font(POPPINS_SEMI, sqft_size)
            sqft_text = "/sq.ft"
            sw = int(sqft_font.getlength(sqft_text))
            sy_pos = py + fit_size + 4
            draw.text((cx + (col_w - sw) // 2, sy_pos),
                      sqft_text, font=sqft_font, fill=col["price_color"])
            d_y = cols_y + int(col_h * 0.65)
            for d in col["details"]:
                dw = int(detail_font.getlength(d))
                dbbox = detail_font.getbbox(d)
                draw.text((cx + (col_w - dw) // 2, d_y - dbbox[1]),
                          d, font=detail_font, fill=col["detail_color"])
                d_y += detail_size + 6

        disc_size = max(13, int(W * 0.016))
        disc_font = load_font(POPPINS_MED, disc_size)
        disc_y = cols_y + col_h + int(H * 0.025)
        draw_centered(draw, "*Pricing varies by project size, scope, and signed estimate.",
                      disc_font, disc_y, W, (110, 110, 110))

    add_cta_block(canvas, is_vertical, "GET A FREE ESTIMATE")
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
    print("Building Phase 4 Retargeting Batch — 5 variants × 2 ratios = 10 images")
    for_each("R1-heat-115-degrees", build_r1_heat_115)
    for_each("R2-rebate-paperwork", build_r2_rebate_paperwork)
    for_each("R3-vegas-dogs", build_r3_dogs)
    for_each("R4-full-yard", build_r4_full_yard)
    for_each("R5-pricing-compare", build_r5_pricing_compare)
    print(f"\nDone. → {OUT}/")


if __name__ == "__main__":
    main()
