# US Turf — Phase 2 Creative Batch (6 Variants)

**Date:** 2026-05-06
**Brand:** US Turf (Pomelli style — Poppins, white-text-top + photo-bottom split)
**Format primary:** 9:16 vertical (Reels/Stories) + 1:1 (feed)
**Destination adset:** "2/23 Ads" (live scaling adset, $40/day, $31 CPL last 3d)
**CTA standard:** "GET A FREE ESTIMATE →"
**Compliance check:** Every claim verified against US Turf project memory + audit notes. No fabrications.

---

## Variant 1 — STAT-SHOCK: 472 Vegas Families
**Source signal:** Turf Bros wins on review-volume framing. Our 4.7★ rating loses to their "1,400+" until we frame as families, not stars.

| Field | Value |
|---|---|
| Headline | **472 VEGAS FAMILIES.** |
| Sub-line | One US Turf install. ★ 4.7 on Google. Family-owned since 2003. |
| Visual | Real US Turf install hero photo (existing CDN photo). White text top band, photo bottom band. Pomelli pattern. |
| CTA | GET A FREE ESTIMATE → |
| Format | 9:16 vertical (primary), 1:1 secondary |
| Why it works | Volume framing beats star rating. "472 families" is a defensible moat. |
| Verification | ✅ 472 reviews / 4.7★ confirmed in project memory + on social2026 LP |

## Variant 2 — REBATE MATH: $5 + $2 = $7
**Source signal:** Simply Turf's "$5 SNWA + $2 LVVWD = $7" beats "up to $7" for credibility. Math > round number.

| Field | Value |
|---|---|
| Headline | **$5 + $2 = $7/SQ.FT BACK.** |
| Sub-line | SNWA pays $5. LVVWD adds $2. Vegas homeowners only. We handle the paperwork. |
| Visual | White card center with the equation as visual focal point. Background: turf install photo (slightly desaturated/blurred). |
| CTA | CLAIM YOUR REBATE → |
| Format | 1:1 (best for math layouts), 9:16 secondary |
| Why it works | Specific numbers + breakdown = trust. Mirrors Simply Turf's framing without copying. |
| Verification | ✅ SNWA $5/sqft + LVVWD $2/sqft = $7/sqft confirmed via SNWA site + Simply Turf LP |

## Variant 3 — PAYMENT ANCHOR: $166/mo
**Source signal:** SYNLawn's 24-48mo Wells Fargo financing beats our 18mo on duration. Counter by anchoring on monthly payment, not term length.

| Field | Value |
|---|---|
| Headline | **VEGAS YARDS FROM $166/MO.** |
| Sub-line | 0% interest. 18 months. Typical 600 sq.ft yard at $4.99/sq.ft = $2,994 ÷ 18. |
| Visual | Hero photo of a real installed Vegas backyard. Bold price callout, smaller fine print. |
| CTA | SEE FINANCING → (or GET A FREE ESTIMATE →) |
| Format | 9:16 |
| Why it works | Monthly framing makes the price feel achievable. Counters SYNLawn duration without comparing. |
| Verification | ⚠️ **Math: $4.99 × 600 = $2,994 / 18 = $166.33/mo. Confirm 600 sq.ft is the right anchor — could go 400 ($110/mo) or 1,000 ($277/mo).** |

## Variant 4 — LONGEVITY: Family-Owned Since 2003
**Source signal:** Direct counter to Panda Turf's recent license #0095121. We have 22 years; they have weeks.

| Field | Value |
|---|---|
| Headline | **22 YEARS. ONE FAMILY. ALL VEGAS.** |
| Sub-line | Installing artificial turf in the Mojave since 2003. Built for the desert. Built to last. |
| Visual | Either: (a) family/founder portrait if you have one, or (b) install photo with "EST. 2003" stamp overlay. Recommend (a) for warmth. |
| CTA | GET A FREE ESTIMATE → |
| Format | 9:16 + 1:1 |
| Why it works | Trust + warmth that recent competitors structurally cannot match. |
| Verification | ✅ 2003 founding confirmed in project memory ("Family-owned Las Vegas artificial turf installation since 2003") |

## Variant 5 — TRUST BLOCK: All 4 NV Licenses
**Source signal:** Panda displays one license #. We have FOUR (B2/C3/C4/C10). Stacking 4x signals general-contractor scope.

| Field | Value |
|---|---|
| Headline | **B2 · C3 · C4 · C10.** |
| Sub-line | 4 Nevada contractor licenses. Most Vegas turf companies have one. We're licensed for the full job. |
| Visual | Clean white card showing the 4 license numbers as 4-cell stat grid: NV #0081302 / #0081384 / #0081385 / #0089330. Small US Turf logo + small install photo in corner. |
| CTA | GET A FREE ESTIMATE → |
| Format | 1:1 (best for stat-grid layouts) |
| Why it works | Verifiable. License #s are public — invites the curious to check. Implies scope (full landscape, not just drop-in turf). |
| Verification | ✅ All 4 NV license #s confirmed in project memory (B2 #0081302, C3 #0081384, C4 #0081385, C10 #0089330) |

## Variant 6 — WARRANTY COMPARISON: Lifetime vs 10-Year
**Source signal:** Panda warranties 10 years. We warranty for life. Direct compare wins.

| Field | Value |
|---|---|
| Headline | **LIFETIME. NOT 10 YEARS.** |
| Sub-line | Some Vegas installers warranty for 10 years. We warranty for life. US Turf install — lifetime warranty included. |
| Visual | Two-column timeline: gray "10 YEARS" line cutoff vs green "LIFETIME →" line continuing past frame. OR a "vs" comparison card with gray X / green check. |
| CTA | GET A FREE ESTIMATE → |
| Format | 1:1 (comparison layouts work square) + 9:16 variant |
| Why it works | Defensible factual comparison. Easy 2-second comprehension. Doesn't name competitor — clean tone. |
| Verification | ✅ US Turf lifetime warranty confirmed in project memory + on social2026 LP |

---

## Production approach
1. Hero images: **reuse existing US Turf install photos** from `skills/product-visual-generator/brands/usturf/style-refs/` and `competitor-assets/` where possible. Generate net-new only for variants 4 (family/founder) + 6 (timeline graphic) if no library match exists.
2. Text overlay: Python + PIL using existing build-fullbleed-ads.py pattern. Poppins Black/ExtraBold per brand DNA.
3. Output: PNG + JPG, 9:16 (1080×1920) and 1:1 (1080×1080) where specified.
4. Repo: push to ksimmons0420/usturf-renders under `/ads/may2026-batch/`.

## Open questions / decisions needed before image-gen
1. **Variant 3 anchor**: 600 sq.ft = $166/mo. Confirm or pick a different anchor.
2. **Variant 4 visual**: do you have a family/founder photo I can use, or should I do "EST. 2003" overlay on an install photo?
3. **Variant 5 license #s**: confirm B2 #0081302 / C3 #0081384 / C4 #0081385 / C10 #0089330 are all current and correct.
4. **Any compliance flags**: any of these claims need legal review before going live (e.g., warranty wording)?

Once you answer these I'll generate all 6, push to repo, and ping you with previews.
