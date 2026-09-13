# Invitation — reference research (image-search)

## Sheets pulled
- /tmp/s1.png   "wedding invitation suite illustrated couple portrait stationery design studio letterpress"
- /tmp/s2.png   "הזמנות לחתונה עיצוב איור זוג"  → Israeli **vendor tier**, weak. Wrong index.
- /tmp/s_35c1.png "hebrew wedding invitation behance" → mostly cohenprinting, gold-frame tier.
- /tmp/s_fbc6.png "one line art couple portrait illustration minimal ink" → Etsy tier BUT key lesson.
- /tmp/s5.png   "Quibe continuous line illustration portrait" → the actual canon.

## What the research says about our v1 draft (out/invitation.png)
v1 is weak for reasons the references make explicit:

1. **It is not a continuous line.** Quibe (the origin of this whole style) is ONE unbroken
   stroke that crosses over itself. Ours is a clean vector *outline* of two bodies —
   closer to a CAD silhouette / colouring book than to line art. This is the main failure.
2. **The pose is a photograph, not a composition.** Two people standing frontally, full body,
   feet and all, floating in the middle of the page. Every good example crops **close** —
   head + torso, intertwined embrace, foreheads together — so the line can loop and overlap.
3. **Blank faces are not actually the rule.** In the Tal&Nadav ref they are blank, but in the
   canon (Quibe) the same single line makes a brow, a nose, a lip. Blank ovals read as unfinished.
4. **Barefoot jeans + t-shirt** adds domestic detail that fights the elegance of the type.
5. Layout-wise the Tal&Nadav skeleton is fine — the failure is the drawing, not the grid.

## Directions to choose from
- **A — True Quibe:** close-crop, real single unbroken line, faces suggested with features,
  much larger on the page, dusty-rose or navy ink. Boldest, most "designed".
- **B — Embrace crop:** keep faceless/minimal but crop to head+torso in an embrace
  (her hair the dominant shape). Safer, still fixes the stiffness.
- **C — Keep Tal&Nadav literally:** full body standing, but redrawn with a real hand-drawn
  ink wobble and her in a long dress. Lowest risk, closest to what Michal actually sent.

## Open, not invented
- חופה time — placeholder `__:__` on the page
- parents' names — placeholder `______ ו______`

## Round 2 — wider search (more ideas)
- /tmp/w1.png "Moglea Hoban Press Ladyfingers Letterpress invitation suite" → **craft tier.**
  Deckled/torn paper edges, blind deboss, 2-colour max, type does all the work, tiny motifs.
  Lesson: restraint + material quality reads more expensive than more decoration.
- /tmp/w2.png "riso printed wedding invitation graphic design" → **contemporary tier.**
  Flat colour blocking, oversized display type, pink/red/mustard/cobalt, photobooth strips,
  die-cut shapes. Fresh and modern, but a different universe from what Michal picked.
- /tmp/w3.png "Rifle Paper Co wedding invitation botanical illustrated" → **on-brief, better.**
  Painted gouache florals that are BOLDER and more saturated than our pale washes, often a
  full dense frame, sometimes a small illustrated couple inside a scene.
  Lesson: our bg1.png is pretty but thin/generic — real florals have weight and a dark note.
- /tmp/w4.png "forest wedding invitation illustration pine trees ink linocut" → **venue-led.**
  Watercolour pine/forest rising from the bottom edge, misty layers, muted sage.

## New idea this surfaced — lead with the venue
The wedding is **ביער, חדרה** (in the forest). Every strong suite in w1/w3/w4 has ONE idea,
not "generic pretty florals". A forest treatment — pines/eucalyptus rising from the bottom
edge, couple line-drawn inside it — is specific to them, and still matches the cream +
dusty-rose palette Michal chose. This beats interchangeable border sprigs.

## Revised recommendation
Keep the Tal&Nadav grid. Change two things:
1. Drawing → close-crop embrace (B) or true continuous line (A), bigger on the page.
2. Botanicals → forest-led and with more weight/contrast, not pale scattered sprigs.

## Round 3 — dropped the word "wedding" entirely
Everything in rounds 1–2 was boring for a structural reason: the wedding index IS a vendor
catalogue. Searching non-wedding registers immediately got interesting.

- /tmp/x1.png "hebrew typography poster israeli graphic design עיצוב כרזה"
  → **Hebrew modernist type.** Bezalel-era wood type, hand-cut letterforms, Hebrew letters
  treated as SHAPES not as a font. Deep black + one hot accent. This is the single biggest
  untapped lever: our v1 set Hebrew in Assistant Light, i.e. a UI font.
- /tmp/x2.png "vintage israeli poster 1960s travel design bezalel" (Farkash Gallery)
  → **Mid-century Israeli travel poster.** Flat cut-paper colour, cypress/cactus/stone motifs,
  El Al jet-age optimism, hand-lettered Hebrew. Confident, warm, unmistakably Israeli.
- /tmp/x3.png "Jaffa orange crate label vintage citrus packing label"
  → **Jaffa crate label.** Lush painted fruit/blossom, ribbon banners, bilingual Hebrew/English,
  gold + red + cobalt, a "brand mark" for the couple. Fun, nostalgic, very giftable.

## Concepts worth actually proposing (none are "botanical border + line couple")
1. **"יער חדרה" as a 1960s Israeli travel poster** — the forest as a destination, flat cut-paper
   pines, hand-lettered names, "3.11.2026" as the departure date. Their venue becomes the idea.
2. **Hebrew letterform as the whole design** — a giant מ and א interlocking (Michal/Ophir) built
   from Bezalel-style wood type; everything else tiny. Bold, graphic, cheap to print.
3. **Jaffa-crate-label wedding mark** — painted citrus/eucalyptus, ribbon banner with
   "מיכל ואופיר", bilingual, gold/cobalt. Nostalgic Israeli, warm, not beige.
4. **El Al boarding pass / ticket** — "ביער, חדרה" as the destination, times as departure/
   boarding/landing. Matches the three-column time strip already in the Tal&Nadav layout.

Risk note: Michal explicitly sent the soft-cream-botanical reference. Any of 1–4 is a bigger
swing than she asked for. Do not ship one of these without showing her.

## ⚠️ Round 4 — THE REAL FINDING: a design system already exists
`~/wedding-invitation/` is an already-built digital invitation for this wedding. I should have
found it before generating anything. It is live at ophirg123.github.io/wedding.

**Established design language (NOT to be reinvented):**
- Palette (CSS vars): cream `#fbf8f3`, wine `#6d2e3c`, gold `#8f7340`, gold-light `#c7ae7d`,
  sage `#7d8b6a`, ink `#46362c`. Note: the ink is WARM BROWN, not navy/grey.
- Type: Heebo (Hebrew body), Frank Ruhl Libre, Cormorant Garamond (Latin/Dutch).
- Paper grain via SVG fractalNoise, multiply blend, opacity .5.
- Watercolour wildflower borders (`border_top.png`, `side_left/right.png`, `bouquet.png`)
  + falling petals `petal0-7.png`.
- **"Living ink" icons** — fine warm-brown single-weight line drawings: rings, coupe glasses,
  getaway car with tin cans, dancing couple, dessert stand, place setting. Each exists as a
  still PNG *and* an mp4 where the ink draws itself in. This is the distinctive idea and it
  already passes the swap-the-names test — it is a system, not decoration.
- Versions: Hebrew RTL, Dutch LTR (`nl/`), religious (`dati/`), QR (`qr_wedding.png`).

**REAL data (my BRIEF.md was wrong / incomplete):**
- קבלת פנים **19:00** (not 19:30) · חופה **20:30** (not TBD) · ארוחת ערב 21:15 ·
  ריקודים 22:00 · מתוקים 22:30 · מעגל סיום 02:00
- Hebrew date: **כ״ג בחשון תשפ״ז**
- Venue styled **״ביער״ · חדרה**
- Parents — הורי הכלה: **רונן ונירית פלד-חדד** · הורי החתן: **רודי וחגית חרותקה**

## Revised conclusion
The paper invitation is not a blank-page design problem. It is the **still, printed member of an
existing family**. The job: take the living-ink icon system + wine/gold/sage palette + Heebo /
Frank Ruhl Libre and render the A4 card as the print sibling of the website — same ink, same
icons marking the timeline, same petals. That is coherent, already loved, already "theirs",
and it kills the swap-test problem for free.

Everything in out/ (invitation.png, modern_M1/M2) is off-system and should be discarded.

## ⚠️⚠️ Round 5 — THE BRAND ALREADY EXISTS AND WAS APPROVED
`~/wedding-brand/` — a full identity project with its own BRIEF.md, 3+ rounds, and a
**mark approved by Michal & Ophir on 28.8**: `waterline/ab_w3.png` = `page/logo.png`.
Also on disk: `~/wedding-design/` (plans, stage), `~/wedding-booth/`, `~/wedding-guests/`.

### The approved mark
Two plants, stems entwined above a waterline, one merged root mass below.
- **Michal = pothos** — the leaf is literally a heart; roots in days; the plant you cut a
  piece off to give away; she is the one who keeps everything alive.
- **Ophir = monstera** — the fenestrations are engineering, not decoration (wind passes
  through instead of tearing; light reaches the leaves below); it climbs toward the light;
  sharp geometry as the counterpart to the heart.
- **Above water:** two plants, entwined, each still itself. **Below water:** roots completely
  merged, you cannot say where one ends and the other begins — "זה כל מה שעברנו ביחד".
- **Waterline** = horizontal rule at full weight, tapering to nothing at both ends.
  `MICHAL` sits left of the stems on the rule, `OPHIR` right. No jar, no frame, no vessel.
- Solid filled shapes, cream ground, deep ink. Date 3.11.26.

### Rules from that brief that bind the invitation
- Reference level = **Celine / Loewe / The Row / Jil Sander**, explicitly NOT wedding stationery.
- No hearts-as-clichés, no rings, no wreath, no oval frame, no interlocked script monogram.
- Must survive at **15–20 mm** (wax seal, napkin, embroidery).
- Black/ink only until the form works; colour after.
- REJECTED already: continuous single-line version ("too calligraphic, lost the botanical
  beauty"), M/O hidden in the roots, initials line `מ · א`.
- Still open (craft): roots read as tree roots not fleshy water roots; typography is stock
  serif and needs a chosen Latin+Hebrew pair; not vector yet.

### What this means for everything I did today
- My "continuous line drawing of the couple" **is a concept they already tried and rejected.**
- My beige botanical border is banned by their own brief ("no wreath", "not wedding stationery").
- The ~/wedding-invitation living-ink icon set (rings, glasses, car) predates the brand and
  uses exactly the wedding clichés the brand brief forbids — check which one is current
  before assuming the icons belong on the printed card.
- The invitation's job: apply the **approved logo** + its typographic system to A4.

### The obvious structural idea (from their own mark, not from me)
The waterline is already a horizontal rule that carries the names. On a portrait card it can
become the **organising line of the whole invitation**: plants above, and the details
(date, venue, times, parents) set below it — in the merged-roots zone. Content follows the
concept: separate above, shared below.
