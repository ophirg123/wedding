# Wedding invitation — Michal & Ophir (3.11.2026, ביער חדרה)

## The reference Michal sent (12:49, 13.9.2026)
`reference_tal_nadav.jpg` — invitation for "טל ונדב", 10.10.2025.
She sent it as "this is what I like".

Style to match:
- ONE continuous-line drawing of the couple, standing, full body, minimal — no faces rendered in detail
- Soft watercolour botanical sprigs scattered around the border (blush, sage, mustard, dusty pink)
- Cream / off-white textured paper background
- Dusty-rose Hebrew display type for the names, dark grey for body text
- Centred layout: intro line -> names -> line drawing -> date -> day -> venue -> three time columns -> parents

## Our details
- מיכל ואופיר
- 3.11.2026, יום שלישי
- ביער, חדרה
- קבלת פנים 19:30, חופה TBD, ends 02:00
- הורי הכלה / הורי החתן — names TBD

## Face/likeness refs
`refs/` — O_front/O_34/O_prof (Ophir), M_front/M_smile/M_laugh/M_out (Michal).
Line art is forgiving: recognition comes from her very long dark hair and his tall
slim build + short hair, NOT from facial detail.

## Model notes
- gemini-3-pro-image (Nano Banana Pro) = best likeness, via /images/edits only
- gpt-image-2 renders correct Hebrew sometimes; ImageMagick is the safe path for text
- KEY=$(nvdesk secrets get IH_API_KEY); BASE=https://inference-api.nvidia.com/v1
