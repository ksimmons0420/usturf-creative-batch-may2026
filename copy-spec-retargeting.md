# US Turf — Phase 4 Retargeting Batch (5 Concern Themes)

**Date:** 2026-05-07
**Brand:** US Turf (Pomelli style — Poppins, real install photos > generated)
**Audience:** Warm retargeting — visited social2026 LP, didn't convert
**Format:** 1:1 (feed) + 9:16 (Reels/Stories — no creative-baked CTA per Meta safe-zone rule)
**Destination adset:** Retargeting campaign (existing or new — confirm)
**CTA standard:** "GET A FREE ESTIMATE →" on 1:1 only
**Copy compliance:** All claims verified against US Turf project memory + brand-dna.md + client confirmation 2026-05-07. No fabricated install timelines, no warranty overreach.

---

## Retargeting psychology
Different from prospecting (Phase 2). These users have already seen the LP and chose not to convert. Job of these ads: address the SPECIFIC objection that kept them on the fence. Tone is direct, conversational, less "here's who we are" and more "let me address the thing you're worried about."

---

## R1 — HEAT SURVIVAL: "Will it stay green in 115°?"
**Concern:** Vegas summers are brutal. They worry fake turf will melt, fade, or cook in 115°F.

| Field | Value |
|---|---|
| Eyebrow | THE VEGAS HEAT TEST |
| Headline | **STILL GREEN AT 115°F.** |
| Sub-line | This Vegas yard is one full Mojave summer old. Same lawn. Same color. Lifetime warranty. |
| Visual | `lush-vegas-backyard.png` — existing real install. "115°F" thermometer chip overlay top-right. |
| CTA (1:1 only) | GET A FREE ESTIMATE → |
| Format priority | 9:16 primary, 1:1 secondary |
| Verification | ✅ Lifetime warranty + real install photos confirmed in project memory |

---

## R2 — REBATE TRUST: "Will the rebate actually pay out?"
**Concern:** "$7/sq.ft back" sounds too good. They worry the paperwork is a nightmare or they won't qualify.

| Field | Value |
|---|---|
| Eyebrow | WE FILE THE PAPERWORK |
| Headline | **YOUR $7/SQ.FT REBATE.** |
| Sub-line | $5 from SNWA. $2 from LVVWD. We file every form. You sign and bank the check. |
| Visual | Cream card layout with rebate breakdown ($5 + $2 = $7 math), similar to V2 from Phase 2. Subtle "stamp/check" iconography. |
| CTA (1:1 only) | CLAIM YOUR REBATE → |
| Format priority | 1:1 primary, 9:16 secondary |
| Verification | ✅ SNWA $5 + LVVWD $2 = $7 confirmed via SNWA site + Simply Turf LP audit |

---

## R3 — PET DURABILITY: "Can my dog destroy it?" *(REVISED 2026-05-07 per client)*
**Concern:** Dog owners worry claws/digging/urine will trash the install.

**Client clarification (2026-05-07):** Lifetime warranty does NOT cover pet-caused wear (claws, digging, urine staining). Urine stains specifically void warranty unless properly maintained. Pivot from "we cover the damage" to "we sell the maintenance solution + partner with Cleaner Turf for full-service care."

| Field | Value |
|---|---|
| Eyebrow | BUILT FOR DESERT PAWS |
| Headline | **VEGAS DOGS DESERVE BETTER.** |
| Sub-line | 20% cooler than concrete on hot paws. Pet-safe infill. We carry the maintenance kits in-house to keep it fresh — or partner with Cleaner Turf for full-service upkeep. |
| Visual | `family-on-turf.png` — existing photo with golden retriever (used in V4 Phase 2) |
| CTA (1:1 only) | GET A FREE ESTIMATE → |
| Format priority | 9:16 primary, 1:1 secondary |
| Why it works | Honest. Leads with verified cooling benefit. Adds the in-house maintenance angle as a unique differentiator no competitor offers. Sets up an upsell on the call. Zero warranty exposure. |
| Verification | ✅ "20% cooler" + "pet-safe infill" confirmed in brand DNA. ✅ In-house maintenance + Cleaner Turf partnership confirmed by client 2026-05-07. NO warranty claims made. |

---

## R4 — FULL-YARD UPSELL: "What about pavers + lighting + the rest?"
**Concern:** Some visitors want a TOTAL outdoor refresh, not just turf. They left because they thought we only do grass.

| Field | Value |
|---|---|
| Eyebrow | TURF + PAVERS + LIGHTING + IRRIGATION |
| Headline | **WE BUILD THE WHOLE BACKYARD.** |
| Sub-line | One install team. Full Vegas backyard transformations. 4 NV contractor licenses (B2 · C3 · C4 · C10) for the whole job. |
| Visual | `lush-vegas-backyard.png` — wide shot already shows turf + pavers + fire pit + planters |
| CTA (1:1 only) | GET A FREE ESTIMATE → |
| Format priority | 1:1 primary, 9:16 secondary |
| Verification | ✅ All 4 NV license #s confirmed in project memory (B2 #0081302, C3 #0081384, C4 #0081385, C10 #0089330) |

---

## R5 — QUALITY-TIER ANCHOR: "Why not the cheaper $1.80 option?" *(REVISED 2026-05-07 per client)*
**Concern:** Price-shoppers comparing US Turf to budget DIY/Home Depot turf at $1.80/sq.ft.

**Client clarification (2026-05-07):** Specific competitor pricing is OK, BUT they've had issues with customers referencing ad pricing vs final signed estimate. Softened "$4.99/sq.ft" to "Starts at $4.99" and added disclaimer: "*Pricing varies by project size, scope, and signed estimate."

| Field | Value |
|---|---|
| Eyebrow | NOT ALL TURF IS EQUAL |
| Headline | **$1.80 vs $5.50 vs $4.99.** |
| Sub-line | Budget DIY rolls: $1.80/sq.ft, 5-yr warranty, fades in 2 summers. Premium installers from $5.50/sq.ft. **US Turf: starts at $4.99/sq.ft. Lifetime warranty. 472 Vegas reviews.** |
| Disclaimer (small) | *Pricing varies by project size, scope, and signed estimate. |
| Visual | 3-column comparison card on cream background (Phase 2 V6 pattern). Gray "BUDGET" / yellow "PREMIUM" / green "US TURF" columns. |
| CTA (1:1 only) | GET A FREE ESTIMATE → |
| Format priority | 1:1 primary, 9:16 secondary |
| Verification | ✅ "Starts at $4.99" softens absolute claim. ✅ Disclaimer matches LP standard language. ⚠️ "$1.80 budget" + "$5.50 premium" are public-source approximations — no specific competitor named. |

---

## Production approach
1. **Photos:** Reuse existing competitor-assets library. R1, R3, R4 use real install photos. R2 + R5 are graphic layouts (cream card pattern).
2. **Build script:** `build-retargeting.py` in same repo as Phase 2's `build-batch.py`. Reuses helpers (load_font, draw_centered, fit_cover, draw_cta_pill, add_top_scrim, add_bottom_scrim, add_band_scrim, draw_polygon_star). Same Poppins fonts.
3. **Output:** PNG at 1080×1080 (1x1) and 1080×1920 (9x16). Total: 5 variants × 2 ratios = 10 images.
4. **9:16 rules:** No creative-baked CTA pill (Meta serves native sticker on Reels/Stories). Top content shifted down 8% to clear top safe zone. Same patterns as Phase 2 fixes.
5. **Repo:** Pushed to existing `ksimmons0420/usturf-creative-batch-may2026` under `renders/ad-batch/may2026-retargeting/`.

## Open follow-up (post-launch)
- Confirm retargeting adset destination (existing or new build-out)
- Consider pet-specific photo upgrade: current `family-on-turf.png` shows family + dog but a single-dog hero photo could lift R3 further
- Consider real customer testimonial overlay on R1 ("Year 2 review: still green!" with quote attribution) once we have the right testimonial
