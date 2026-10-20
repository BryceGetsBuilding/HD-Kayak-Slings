# Kayak Cradles — Build Doc

Two free-standing wooden cradles that hold a kayak in a webbing sling, copied
from the reference photos and sized for an **Old Town Sportsman 106 PDL**
(36" wide, ~107 lb, pedal drive removed for storage). Build **two identical
cradles** and set them ~6.5 ft apart along the hull.

Files in this folder:

| File | What it is |
|---|---|
| `build-guide.pdf` | **Step-by-step printable build guide** (10 pages, a rendered visual for every assembly step) — start here |
| `BILL-OF-MATERIALS.md` | **Complete BOM** — lumber, every cut piece, fasteners with a screw schedule, sling, consumables, tools, cost estimate |
| `make_guide.py` | Regenerates `build-guide.pdf` from the drawings + renders + this doc |
| `guide_s1_parts.png` … `guide_s8.png` | Per-step renders embedded in the guide |
| `photo-match-design.png` / `.svg` | Dimensioned end view + plan view |
| `hardware-detail.png` | Close-up of the post-top bolt / washer / nut stack |
| `cut-sheet.png` / `.svg` | Board-by-board cutting layout — how many 2×4s, every piece, length, and cut |
| `cradle_freecad.py` | Parametric generator — 5 PartDesign parts + an Assembly with joints; prints the cut list |
| `cradle_model.FCStd` / `.step` | Pre-built model — one cradle on the origin, jointed assembly + hull ghost |
| `cradle_freecad_part_version.py.bak` | Older generator that builds one flat Part (no assembly) — kept as a fallback |
| `BUILD.md` | This document |

---

## The design

Each cradle is a flat vertical frame standing on two feet:

- **2 vertical posts** — dead vertical (90° to the ground), each standing **on
  its foot**, outer face flush with the foot's outer edge. The webbing wraps
  over the top end of each post, down the outside face, and is clamped by two
  carriage bolts side-by-side (with big fender washers, or an optional steel
  plate, so the heads can't pull through the weave).
- **1 bottom rail** — 2x4 laid flat, cut to **fit exactly between the two
  posts** (butts their inner faces). It rests on the feet at its ends and ties
  the posts together at the bottom.
- **2 diagonal V-braces** — upright 2x4 (3½" face flush with the frame, *not*
  laid on their sides), running at **45°** from the **center of the bottom
  rail** up to each post, in the same vertical plane as the sling. **A 45°
  bevel at each end, but the two bevels are perpendicular to each other, not
  parallel** — it's a right trapezoid, not a parallelogram: the bottom bevel
  is cut so it sits flat on the *horizontal* rail, the top bevel is cut so it
  sits flush on the *vertical* post face, and a horizontal surface and a
  vertical surface are perpendicular to each other. Cut one end, then **flip
  the board end-for-end** before cutting the other end at the same 45° — if
  you cut both ends without flipping you get a parallelogram, which will not
  sit flush on both the rail and the post. They're sized to meet at a point
  at the rail centre — no notch, no overlap.
- **2 feet** — 2x4 laid flat, one under each post, running **front-to-back**
  (perpendicular to the frame). They run the full 30" (they're the only thing
  resisting a fore/aft tip). The post sits on the foot with its outer face
  **flush with the foot's outer edge**, so the foot is *not* centred on the
  post — it overhangs 2" on the inboard side (where the rail end lands on it).
- **1 optional foot stretcher** tying the two feet together.
- **The sling** — 3"-wide polyester webbing (4" is fine too). The hull settles
  into it; with the boat in place the low point sits ~19½" off the ground,
  which clears a 13.75"-tall YakAttack Bunkster cart by ~5-6".

### Key dimensions

| | |
|---|---|
| Post spacing | **38" on center** (36½" clear — the 36" hull passes between) |
| Post length | **30"** (posts stand on the feet; tops ~31½" off the ground) |
| Bottom rail | **36½"**, 2x4 laid flat; fits exactly between the two posts |
| V-brace | **~25¾"** long edge; 45° bevel each end, perpendicular to each other |
| Feet | **30"** long, one under each post (post flush with the foot's outer edge) |
| Foot stretcher (optional) | **39½"** |
| Sling webbing | **3"-wide polyester** (4" ok); ~7 ft per cradle |
| Loaded sling low point | ~19½" off the ground (clears the 13.75" cart by ~5-6") |
| Cradle-to-cradle spacing | ~6.5 ft (78") along the hull |

---

## Cut list — per cradle (cut everything ×2 for the pair)

All parts are 2x4 (actual 1½" × 3½").

| Part | Qty | Length | Notes |
|---|---|---|---|
| Post | 2 | 30" | square both ends; stands on its foot, outer face flush with the foot's outer edge |
| Bottom rail | 1 | 36½" | square both ends; **laid flat**; cut to fit exactly between the two posts (butts their inner faces); rests on the feet at its ends |
| V-brace | 2 | ~25¾" long edge → **cut to fit** | **45° bevel at each end, perpendicular to each other** (a right trapezoid, not a parallelogram — flip the board end-for-end between cuts): bottom seats flat on the rail, top lies flush on the post; sized so the two meet at a point at the rail centre |
| Foot | 2 | 30" | square ends; sand/round the top corners of both ends |
| Gusset (optional) | 4–6 | ~7" | 2x4 or ½" ply scrap — covers each brace joint |
| Foot stretcher (optional) | 1 | 39½" | laid flat across the top of both feet; 1 screw down into each foot |
| Post-top pad (optional) | 2 | 3½" | scrap 2x4, outdoor carpet, or stick-on rubber |

---

## Shopping list

Everything below is available at **one Home Depot or Lowe's run**. Quantities
are for **the pair** (both cradles).

### Lumber
- **7 × 8-ft 2x4** (6 get used per `cut-sheet.png` — 16 pieces ≈ 42 board-ft;
  the 7th is insurance against a bad cut, plus offcuts for gussets/pads).
- Stud-grade SPF/DF is fine for garage storage. Ground-contact **pressure-
  treated** or cedar if the cradles will live outdoors.

### Fasteners & hardware
| Item | Qty | HD (Everbilt) / Lowe's (Hillman) |
|---|---|---|
| 5⁄16"-18 × 2½" carriage bolt, zinc | 8 (+2 spare) | fastener bins / blister packs |
| 5⁄16"-18 nylon-insert lock nut, zinc | 8 (+2) | |
| 5⁄16" fender washer, zinc (1¼–1½" OD) | 8 (+2) | **outside only, under each nut** (over the webbing) — spreads clamp load so the nut can't cut through it. No washer needed under the dome head; it seats straight against the wood on the inside. |
| Flat tie/nail plate, ~3" × 5", galvanized | 0–4 | **Optional.** The load per strap end is only ~40–50 lb, so fender washers are plenty. Add a plate over the webbing on each post top only if you want the photo look or extra abrasion/tear protection outdoors. HD: Simpson Strong-Tie TP35 (SKU 100375154). |
| 3" exterior structural / deck screws (#9–#10) | 1 lb box (~75) | Deckmate/Grip-Rite, Deck Plus, SPAX, or GRK. Used at every wood joint: foot-to-post (2 per foot, up from below), rail-to-foot (2 per end, down through the rail), brace-to-post & brace-to-rail (1 each), stretcher-to-foot (1 each). At each foot junction the 4 screws sit 1" either side of the board centre — 2" apart, ¾" edge distance. |

### Sling — polyester tow / recovery / tree-saver strap
Allow **~7 ft of usable webbing per cradle** (the straight run is ~37", plus
~12" of sag, plus the wrap over each post top and a few inches of tail).
**Cut the sewn loop ends (or hooks) off**, cut to length, melt-seal the raw
ends with a lighter.

- **Most in-stock — 2" polyester tow strap:** *Husky 2" × 20 ft Recovery Tow
  Strap* (Home Depot #59925, loop ends, no hooks). Buy 1, cut the loops off,
  cut in half — one strap does both cradles. 2" is plenty at ~55 lb per cradle
  (≈1–2 psi on the hull); wider is just a bonus. Harbor Freight / Walmart /
  Tractor Supply / auto-parts stores carry equivalent 2" straps.
- **3" tree-saver, if you want the wider strap:**
  - Home Depot: *Keeper 3" × 8 ft Tree Saver Strap* — buy 2. (Skip the 3" × 6 ft —
    too short once the loops are cut off.)
  - Lowe's: *VEVOR 3" × 20 ft tree-saver strap* — buy 1, cut in half.
- **3" from a big-box shelf:** *Lawn Chair USA 3" polypropylene webbing roll*
  (Walmart). Soft and UV-stable but polypropylene creeps under constant load —
  OK indoors, but a 2" polyester tow strap is the better choice.
- **Polyester, not nylon.** Tow/tree-saver straps are polyester and barely
  stretch. Their 20,000-lb+ rating is irrelevant overkill here; width is all
  that matters, to spread hull pressure.
- (By the yard, if you'd rather mail-order: Strapworks / US Cargo Control /
  "Country Brook Design 3 inch polyester webbing" on Amazon — ~14 ft.)

### Optional / from scrap — nothing to buy
- Gussets and post-top pads come out of 2x4 offcuts.
- Post-top pad facing: a carpet remnant or a rubber stair-tread scrap.

### Tools
Miter saw (best for the repeated 45° V-brace bevels) or circular saw ·
drill/driver · drill bits (5⁄16", ¼", + pilot) · ½" wrench or socket ·
tape measure · speed square · 2–3 clamps · rasp or 80-grit sandpaper ·
lighter (to melt-seal the webbing ends) · eye protection.

---

## Assembly

Do one full cradle, then repeat.

1. **Cut the parts.** Cut the 2 posts, 1 rail and 2 feet to length (square
   ends). The rail must be **36½"** — the exact gap between the posts. Leave the
   2 V-braces as ~28" blanks for now.

2. **Drop in the rail.**
   - Lay the two feet **flat on the ground**, front-to-back, **38" on center**
     — the spacing the posts will stand at — with each foot's 2" inboard
     overhang facing the other.
   - Lay the bottom rail **flat** across the feet, resting on those overhangs,
     ends **36½"** apart — exactly where the posts' inner faces will land.
   - From **on top of each rail end** drive **2 × 3"
     screws** straight down through the rail into the foot. Put them **1"
     either side of the board centreline** — 2" apart, ¾" from each edge —
     and use the same layout at both ends.

3. **Post + foot sub-assemblies.**
   - Stand a post on the **outer portion** of each foot: the post sits with
     its **outer face flush with the foot's outer edge**, over the part of
     the foot not already covered by the rail. Check the frame is square
     (equal diagonals) before fastening.
   - Drive **2 × 3" screws** up through the foot into the
     post (pre-drill). Put them **1" either side of the board centreline** —
     2" apart, ¾" from each edge — and use the same layout on both feet.

4. **Fit the V-braces (one 45° cut per end).**
   - Cut a 45° bevel on one end, then **flip the board end-for-end** and cut
     the other end at the same 45° setting — the two cuts end up
     **perpendicular to each other**, not parallel (a right trapezoid, not a
     parallelogram). One end needs to sit flat on the horizontal rail, the
     other flush on the vertical post face, and those surfaces are 90° apart,
     so the cuts have to be too. Cutting both ends without flipping the board
     gives a parallelogram that won't sit flush on both surfaces. Long edge ≈
     25¾" — cut one, test fit, trim, then use it as the pattern for the rest.
   - Run each brace from the **center of the rail top** up at 45° to a post.
     Bottom bevel seats flat on the rail; top bevel lies flush on the post
     face. The two braces meet at a point at the rail centre.
   - Fasten each brace: **1 screw down through the brace's bottom end into the
     rail** (driven from the brace's top face, near its tip — accessible once
     the frame is standing), and **1 screw driven horizontally from the brace
     face into the post**, about 1½" below the brace/post tip. A scrap gusset
     over each joint is optional insurance.

5. **Foot stretcher (optional).** Lay it flat across the tops of both feet near
   one end; **1 screw down through it into each foot**.

6. **Ease the foot ends.** Round the top corners of all four foot ends with a
   rasp or sander so nobody stubs a toe.

7. **Repeat for cradle #2.**

8. **Post-top pads (optional).** Staple carpet or stick rubber to the top of
   each post where the hull might touch.

---

## The sling

Per cradle:

1. Cut a length of 3" polyester webbing ~30" longer than the straight-line
   distance between the two post tops (≈7 ft). **Melt-seal both cut ends** with
   a lighter so they can't fray.
2. Round over the top edge of the post where the webbing will bend, then wrap
   one end over the post top and down the **outside** face ~5".
3. Mark two hole centers **side-by-side across the strap, ~2" apart**, about
   1½–2" down from the post top. (If using the optional plate, lay it over the
   webbing and mark through it.)
4. Drill 5⁄16" straight through: webbing → post (→ plate).
5. Push the carriage bolts in **from the inside face of the post** (tap them so
   the square shoulder seats into the wood; the dome head sits straight against
   the wood, no washer needed there). The smooth head ends up on the inside,
   toward the hull. On the outside, add a fender washer (and the plate, if
   used) and a nylon-lock nut. Snug them up — firm, not crushing the webbing flat.
6. Repeat on the other post. Before final tightening, pull the webbing through
   so that with the kayak resting in it the low point sits ~19–20" off the
   ground — roughly **12" of sag** below the post tops. Trim the excess, leave
   a few inches of tail, re-seal the cut.

Set the two cradles ~6.5 ft (78") apart, lift the (drive-removed) kayak in,
and fine-tune the webbing tension so the hull beds evenly.

---

## The FreeCAD model

`cradle_freecad.py` builds one `cradle_model` document containing:

1. **5 PartDesign Bodies** — `Post`, `Bottom_Rail`, `V_Brace` (its 45° bevels
   are drawn into the profile sketch), `Foot`, `Foot_Stretcher`. Each is a
   Sketch + Pad; edit a sketch or the `PARAMETERS` block to resize.
2. **An Assembly, `Cradle_Rig`** — `App::Link` instances of those bodies for
   **one cradle centred on the origin**: 2 posts, 2 braces, 2 feet, 1 rail,
   1 stretcher (8 links). Set `N_CRADLES = 2` in the script to instance both
   real cradles side by side.
3. **Joints** (`Joints` group) — `Foot_L_1` is grounded; every other part is
   tied back through a chain of **Fixed** joints, so the cradle is fully
   constrained. The joints use `Detach = true` with explicit connector
   placements, so `Cradle_Rig.solve()` holds each part at its intended pose.
4. **`webbing_sling_*` / `hull_ghost_*`** — plain visual `Part::Feature`s, not
   part of the assembly.
5. **`Hardware` group** — procedurally-modelled fasteners as `App::Link`s
   (visual only, placed by coordinate — not part of the joint solve):
   - `Carriage_Bolt` ×4, `Fender_Washer` ×4, `Hex_Nut` ×4 — two per post top;
     dome seats straight on the wood, inside face; washer + nut flush on the
     webbing's outside face.
   - `Deck_Screw` ×14 — at each foot junction, 2 up through the foot into the
     post and 2 down through the rail end into the foot (all 1" off the board
     centreline → 2" apart, ¾" edge distance, matched on both feet); plus
     2 from the brace faces into the posts, 2 down through the brace bottoms
     into the rail, and 2 down through the stretcher into the feet.
   Toggle with `ADD_HARDWARE` / `ADD_SCREWS`; sizes are in the `PARAMETERS`
   block (`BOLT_DIA`, `WASHER_OD`, `NUT_AF`, `SCREW_DIA`, …).

- **Open the pre-built model:** open `cradle_model.FCStd`.
- **Regenerate:** in the GUI, `Macro → Macros…`, point at `cradle_freecad.py`,
  `Execute`. Edit the `PARAMETERS` block first — `N_CRADLES` (1 modelled by
  default, set 2 to see both), `BUILD_QTY` (2, drives the cut-list text),
  post spacing, post/foot length, `CRADLE_GAP`, strap/stretcher/ghost toggles.
  It closes and rebuilds `cradle_model` and re-prints the cut list each run.
- **Headless** (`freecadcmd cradle_freecad.py`) builds the 5 parts and places
  the links, but **skips the joints** — the Assembly joint API needs the GUI.
  Use the GUI to get the constrained assembly.
- `cradle_freecad_part_version.py.bak` is the earlier generator that builds a
  single flat Part (no bodies, no assembly) — simpler, fully headless, same
  geometry and cut list. Rename it to `.py` if you want that instead.

---

## Options / adjustments

- **Narrower or wider boat later:** change `POST_SPACING` in the FreeCAD script
  and re-run for a fresh cut list.
- **Lower stance:** if you don't need to roll the cart under, drop `POST_LEN`
  to ~22–24" for a shorter, even more stable cradle.
- **More rack resistance:** keep the foot stretcher, and/or add a second
  stretcher near the other end of the feet.
- **Outdoors:** pressure-treated or cedar lumber, stainless hardware, and keep
  the webbing shaded or covered — UV is what eventually kills polyester.
