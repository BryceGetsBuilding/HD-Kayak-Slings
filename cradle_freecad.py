# =====================================================================
#  Kayak cradle - PartDesign parts + Assembly (with joints)
#  For an Old Town Sportsman 106 PDL  (36" wide, ~107 lb, drive removed)
#
#  Builds ONE document containing:
#    - 5 PartDesign Bodies (each a Sketch + Pad):
#        Post, Bottom_Rail, V_Brace (45-deg bevels), Foot, Foot_Stretcher
#    - an Assembly "Cradle_Rig" with App::Link instances of those bodies
#        (2 posts, 2 braces, 2 feet, 1 rail, 1 stretcher  x2 cradles)
#    - a Grounded joint + Fixed joints so the whole thing is constrained
#    - the webbing sling + a hull ghost as plain visual references
#
#  HOW TO RUN
#    GUI:      Macro -> Macros... -> point at this file -> Execute
#    Headless: freecadcmd cradle_freecad.py   (Assembly joints need the GUI,
#              so headless builds the parts + a plain placed layout only)
#
#  Units: inches in this file; x25.4 -> mm for FreeCAD.
# =====================================================================

import os
import math
import FreeCAD as App
import Part

IN = 25.4
V = App.Vector
Pl = App.Placement
Rot = App.Rotation

# ---------------------------------------------------------------------
#  PARAMETERS  (edit these)
# ---------------------------------------------------------------------
BOARD_T = 1.5          # 2x4 actual thickness
BOARD_W = 3.5          # 2x4 actual width

POST_SPACING = 38.0    # centre-to-centre of the two posts (36.5" clear -> 36" hull passes between)
POST_LEN     = 30.0
FOOT_LEN     = 30.0

ADD_STRETCHER = True
ADD_STRAP     = True
STRAP_SAG     = 12.0
STRAP_WIDTH   = 3.0

N_CRADLES  = 1        # how many cradles to model (1 = a single cradle on the origin)
BUILD_QTY  = 2        # how many you actually build for the boat (fore + aft)
CRADLE_GAP = 78.0     # spacing between the two real cradles along the hull

SHOW_HULL_GHOST = True

ADD_HARDWARE  = True   # model the carriage bolts / fender washers / hex nuts at the strap ends
ADD_SCREWS    = True   # a few visible screw heads at the frame joints
BOLT_DIA   = 0.3125   # 5/16"
BOLT_LEN   = 2.5      # carriage bolt length
HEAD_DIA   = 0.66     # dome head across
HEAD_H     = 0.19     # dome rise
NECK       = 0.31     # square neck
WASHER_OD  = 1.25     # fender washer
WASHER_ID  = 0.36
WASHER_T   = 0.06
NUT_AF     = 0.50     # hex nut across flats
NUT_T      = 0.27
BOLT_DROP  = 2.0      # bolt centre this far below the post top
BOLT_GAP   = 2.0      # spacing between the two bolts across the strap
SCREW_DIA  = 0.19
SCREW_HEAD = 0.38
SCREW_LEN  = 3.0

# ---------------------------------------------------------------------
#  Derived
# ---------------------------------------------------------------------
FOOT_TOP_Z   = BOARD_T
POST_BOT_Z   = FOOT_TOP_Z                    # posts stand ON the feet
POST_TOP_Z   = POST_BOT_Z + POST_LEN
RAIL_TOP_Z   = FOOT_TOP_Z + BOARD_T          # rail laid flat on the feet, between the posts
# The posts' outer faces sit flush with the outer edges of the feet, at
#   +/- (POST_SPACING/2 + BOARD_T/2)  from centre.  The feet are 2" wider than
# the posts, so each foot is shifted 1" INBOARD (not centred on its post).
FLUSH_Y      = POST_SPACING / 2.0 + BOARD_T / 2.0   # post outer face = foot outer edge
BRACE_INFACE = POST_SPACING / 2.0 - BOARD_T / 2.0   # post inner face
RAIL_LEN     = 2.0 * BRACE_INFACE                   # rail fits exactly between the posts
STRETCH_SPAN = 2.0 * FLUSH_Y                        # stretcher spans the feet outer edges
GUI = App.GuiUp

DOC_NAME = "cradle_model"

# =====================================================================
#  Part builders  (PartDesign Body = Sketch + Pad)
# =====================================================================
def _rect_body(doc, name, dx, dy, pad_len):
    """A rectangular 2x4 piece: rectangle dx x dy on the XY plane,
       padded pad_len in +Z. Local origin at the (0,0,0) corner."""
    import Sketcher
    body = doc.addObject("PartDesign::Body", name)
    sk = body.newObject("Sketcher::SketchObject", name + "_profile")
    sk.Placement = Pl(V(0, 0, 0), Rot())
    p = [V(0, 0, 0), V(dx * IN, 0, 0), V(dx * IN, dy * IN, 0), V(0, dy * IN, 0)]
    for i in range(4):
        sk.addGeometry(Part.LineSegment(p[i], p[(i + 1) % 4]), False)
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 4, 1))
    doc.recompute()
    pad = body.newObject("PartDesign::Pad", name + "_pad")
    pad.Profile = sk
    pad.Length = pad_len * IN
    sk.Visibility = False
    doc.recompute()
    return body


BRACE_LEN = BRACE_INFACE * math.sqrt(2.0)   # long-edge length of the V-brace


def _brace_body(doc, name):
    """The V-brace: a 2x4 with a 45-deg bevel at EACH end, but the two bevels
       are PERPENDICULAR to each other, not parallel -- this is a right
       trapezoid, not a parallelogram. It has to be: the bottom end seats
       flat on the HORIZONTAL rail top, and the top end sits flush on the
       VERTICAL post face, and a horizontal plane and a vertical plane are
       perpendicular. Cut one end at 45 deg, then flip the board end-for-end
       (or flip the saw's bevel direction) before cutting the other end --
       repeating the same bevel without flipping gives a parallelogram, which
       would NOT sit flush on both surfaces.
       Local frame: X = run 0..BRACE_INFACE, Y = height, Z = 0..BOARD_W (depth).
       Side profile is a 4-sided right trapezoid: the two short edges (the
       actual saw cuts) are one horizontal, one vertical; the two long edges
       (the board's uncut faces) are parallel to each other at 45 deg."""
    import Sketcher
    run = BRACE_INFACE
    w = BOARD_T * math.sqrt(2.0)          # board footprint along the run at each 45-deg end
    pts = [V(0.0, 0.0, 0.0),             # inner point, at the rail centre
           V(w * IN, 0.0, 0.0),          # outer end of the bottom bevel, on the rail
           V(run * IN, (run - w) * IN, 0.0),   # bottom of the top bevel, at the post
           V(run * IN, run * IN, 0.0)]         # top of the top bevel, at the post
    body = doc.addObject("PartDesign::Body", name)
    sk = body.newObject("Sketcher::SketchObject", name + "_profile")
    sk.Placement = Pl(V(0, 0, 0), Rot())
    n = len(pts)
    for i in range(n):
        sk.addGeometry(Part.LineSegment(pts[i], pts[(i + 1) % n]), False)
    for i in range(n):
        sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % n, 1))
    doc.recompute()
    pad = body.newObject("PartDesign::Pad", name + "_pad")
    pad.Profile = sk
    pad.Length = BOARD_W * IN
    sk.Visibility = False
    doc.recompute()
    return body


def build_bodies(doc):
    b = {}
    b["Post"]           = _rect_body(doc, "Post",           BOARD_W, BOARD_T, POST_LEN)
    b["Bottom_Rail"]    = _rect_body(doc, "Bottom_Rail",    BOARD_W, RAIL_LEN, BOARD_T)
    b["Foot"]           = _rect_body(doc, "Foot",           FOOT_LEN, BOARD_W, BOARD_T)
    b["Foot_Stretcher"] = _rect_body(doc, "Foot_Stretcher", STRETCH_SPAN, BOARD_W, BOARD_T)
    b["V_Brace"]        = _brace_body(doc, "V_Brace")
    for body in b.values():
        if GUI:
            body.ViewObject.ShapeColor = (0.82, 0.66, 0.42)
    doc.recompute()
    return b


# =====================================================================
#  Instance placements  (world = cradle coords; Cradle 1 centred on origin)
#    X = along the hull    Y = between the posts    Z = up
# =====================================================================
def _rot_from_axes(cx, cy, cz):
    """A rotation whose columns are the given (unit) frame axes."""
    a, b, c = V(*cx), V(*cy), V(*cz)
    for u in (a, b, c):
        u.normalize()
    m = App.Matrix(a.x, b.x, c.x, 0,
                   a.y, b.y, c.y, 0,
                   a.z, b.z, c.z, 0,
                   0, 0, 0, 1)
    return Rot(m)

# The V_Brace body carries its 45-deg shape in its side profile, so each brace
# only needs an axis permutation into cradle coords (no extra tilt):
#   right brace: local X -> +Y, local Y -> +Z, local Z (depth) -> +X
#   left  brace: local X -> -Y, local Y -> +Z, local Z (depth) -> -X  (mirror)
_BRACE_ROT_R = _rot_from_axes((0, 1, 0), (0, 0, 1), (1, 0, 0))
_BRACE_ROT_L = _rot_from_axes((0, -1, 0), (0, 0, 1), (-1, 0, 0))


def instance_table(x0):
    """name -> (body key, world Placement) for one cradle at hull offset x0."""
    t = {}
    for s, tag in ((-1.0, "L"), (1.0, "R")):
        y = s * POST_SPACING / 2.0
        # foot shifted inboard so its OUTER edge sits on the FLUSH_Y plane
        foot_py = (FLUSH_Y - BOARD_W) if s > 0 else -FLUSH_Y
        t["Foot_%s" % tag] = ("Foot",
            Pl(V(x0 - FOOT_LEN / 2.0, foot_py, 0.0) * IN, Rot()))
        t["Post_%s" % tag] = ("Post",
            Pl(V(x0 - BOARD_W / 2.0, y - BOARD_T / 2.0, POST_BOT_Z) * IN, Rot()))
        if s > 0:
            t["Brace_%s" % tag] = ("V_Brace",
                Pl(V(x0 - BOARD_W / 2.0, 0.0, RAIL_TOP_Z) * IN, _BRACE_ROT_R))
        else:
            t["Brace_%s" % tag] = ("V_Brace",
                Pl(V(x0 + BOARD_W / 2.0, 0.0, RAIL_TOP_Z) * IN, _BRACE_ROT_L))
    t["Bottom_Rail"] = ("Bottom_Rail",
        Pl(V(x0 - BOARD_W / 2.0, -RAIL_LEN / 2.0, FOOT_TOP_Z) * IN, Rot()))
    if ADD_STRETCHER:
        t["Foot_Stretcher"] = ("Foot_Stretcher",
            Pl(V(x0 + FOOT_LEN / 2.0, -STRETCH_SPAN / 2.0, FOOT_TOP_Z) * IN,
               Rot(V(0, 0, 1), 90)))
    return t


# =====================================================================
#  Assembly + joints
# =====================================================================
def build_assembly(doc, bodies):
    asm = doc.addObject("Assembly::AssemblyObject", "Cradle_Rig")
    doc.recompute()

    links = {}          # instance name -> App::Link
    world = {}          # instance name -> Placement

    offsets = [i * CRADLE_GAP for i in range(N_CRADLES)]
    for ci, x0 in enumerate(offsets, start=1):
        for base, (bkey, plc) in instance_table(x0).items():
            nm = "%s_%d" % (base, ci)
            lk = doc.addObject("App::Link", nm)
            lk.LinkedObject = bodies[bkey]
            lk.Placement = plc
            asm.addObject(lk)
            links[nm] = lk
            world[nm] = plc
    doc.recompute()

    if not GUI:
        App.Console.PrintWarning(
            "No GUI: parts placed but Assembly joints skipped "
            "(joint API needs the FreeCAD GUI).\n")
        return asm, links

    import JointObject
    import UtilsAssembly
    jg = UtilsAssembly.getJointGroup(asm)

    ground_name = "Foot_L_1"
    gj = jg.newObject("App::FeaturePython", "Ground_" + ground_name)
    JointObject.GroundedJoint(gj, links[ground_name])
    try:
        JointObject.ViewProviderGroundedJoint(gj.ViewObject)
    except Exception:
        pass

    def fix(child, parent):
        fj = jg.newObject("App::FeaturePython", "Fix_%s__%s" % (child, parent))
        JointObject.Joint(fj, 0)                      # 0 = Fixed
        try:
            JointObject.ViewProviderJoint(fj.ViewObject)
        except Exception:
            pass
        fj.Reference1 = (links[parent], [""])
        fj.Reference2 = (links[child], [""])
        # Detach = don't re-derive the joint frames from the references; use the
        # ones we set, so the solver locks the parts at their known relative pose.
        fj.Detach1 = True
        fj.Detach2 = True
        fj.Placement1 = Pl()
        fj.Placement2 = world[child].inverse().multiply(world[parent])
        return fj

    # chain every part back to the grounded foot
    for ci in range(1, N_CRADLES + 1):
        f_l, f_r = "Foot_L_%d" % ci, "Foot_R_%d" % ci
        p_l, p_r = "Post_L_%d" % ci, "Post_R_%d" % ci
        rail = "Bottom_Rail_%d" % ci
        if ci == 1:
            fix(f_r, f_l)
        else:
            fix(f_l, "Foot_L_1")
            fix(f_r, f_l)
        fix(p_l, f_l)           # posts stand on the feet
        fix(p_r, f_r)
        fix(rail, p_l)          # rail butts between the posts (rests on the feet)
        fix("Brace_L_%d" % ci, rail)
        fix("Brace_R_%d" % ci, rail)
        if ADD_STRETCHER:
            fix("Foot_Stretcher_%d" % ci, f_l)

    try:
        asm.solve()
    except Exception as e:
        App.Console.PrintWarning("solve() said: %s\n" % e)
    doc.recompute()
    return asm, links


# =====================================================================
#  Sling + hull ghost  (plain visual Part features, not in the assembly)
# =====================================================================
def _beam_between(p1, p2, width, thick):
    v = V(p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    b = Part.makeBox(thick * IN, width * IN, v.Length * IN,
                     V(-thick * IN / 2.0, -width * IN / 2.0, 0.0))
    b.Placement = Pl(V(p1[0] * IN, p1[1] * IN, p1[2] * IN), Rot(V(0, 0, 1), v))
    return b


STRAP_THICK = 0.12   # webbing thickness -- the wrap segments sit with their
                     # INNER face exactly flush on the wood (centreline pushed
                     # out by half the thickness), not floating clear of it.


def _strap_path(x0):
    """Key points of one sling, post top -> post top, routed so it actually
       wraps over each post and down to the real clamp point (matches the
       Carriage_Bolt placement in add_hardware), instead of just stopping at
       the post centreline:
         clamp (where the bolts are) -> up the OUTER face -> across the top ->
         down the INNER face into the sag -> ... -> mirror on the other post.
       The wrap (clamp/side/top) sits flush against the wood -- its centreline
       is offset by half the webbing thickness so the INNER face lands right
       on the post surface, with no gap and no burial."""
    y_in = BRACE_INFACE                      # post inner face |Y| (unchanged, hangs free)
    y_out = FLUSH_Y + STRAP_THICK / 2.0      # post outer face, strap flush against it
    z_top = POST_TOP_Z + STRAP_THICK / 2.0   # post top, strap flush against it
    z_clamp = POST_TOP_Z - BOLT_DROP         # bolt height (flush is fine, nothing to embed in)
    n_sag = 16
    pts = [(x0, -y_out, z_clamp), (x0, -y_out, z_top), (x0, -y_in, z_top)]
    for k in range(1, n_sag):
        tt = k / float(n_sag)
        yy = -y_in + 2.0 * y_in * tt
        zz = z_top - STRAP_SAG * (1.0 - (2.0 * tt - 1.0) ** 2)
        pts.append((x0, yy, zz))
    pts += [(x0, y_in, z_top), (x0, y_out, z_top), (x0, y_out, z_clamp)]
    return pts


def _strap_ribbon(pts, thick, width, x0):
    """Build the whole sling as ONE flat mitred ribbon instead of a chain of
       independently-rotated boxes. Every point in pts shares the same x0, so
       the path is planar (all in the Y-Z plane) -- extrude a single 2D offset
       outline along X once. A per-segment box chain twists at sharp corners
       (each box's flat end-cap shows edge-on where the direction changes),
       which is exactly the "sideways link" artifact at the post-wrap turns;
       one planar extrusion has no per-segment rotation at all, so it can't."""
    yz = [(p[1], p[2]) for p in pts]
    n = len(yz)

    def seg_normal(a, b):
        dy, dz = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dy, dz)
        return (dz / L, -dy / L)

    seg_n = [seg_normal(yz[i], yz[i + 1]) for i in range(n - 1)]
    vert_n = []
    for i in range(n):
        ns = ([seg_n[i - 1]] if i > 0 else []) + ([seg_n[i]] if i < n - 1 else [])
        vx = sum(a[0] for a in ns) / len(ns)
        vy = sum(a[1] for a in ns) / len(ns)
        L = math.hypot(vx, vy)
        vert_n.append((vx / L, vy / L) if L > 1e-9 else (0.0, 0.0))

    h = thick / 2.0
    top = [(yz[i][0] + vert_n[i][0] * h, yz[i][1] + vert_n[i][1] * h) for i in range(n)]
    bot = [(yz[i][0] - vert_n[i][0] * h, yz[i][1] - vert_n[i][1] * h) for i in range(n)]
    outline = top + list(reversed(bot))
    wpts = [V(x0 * IN, y * IN, z * IN) for (y, z) in outline]
    wpts.append(wpts[0])
    face = Part.Face(Part.makePolygon(wpts))
    solid = face.extrude(V(width * IN, 0, 0))
    solid.translate(V(-width * IN / 2.0, 0, 0))
    return solid


def add_references(doc):
    offsets = [i * CRADLE_GAP for i in range(N_CRADLES)]
    for ci, x0 in enumerate(offsets, start=1):
        if ADD_STRAP:
            pts = _strap_path(x0)
            o = doc.addObject("Part::Feature", "webbing_sling_%d" % ci)
            o.Shape = _strap_ribbon(pts, STRAP_THICK, STRAP_WIDTH, x0)
            if GUI:
                o.ViewObject.ShapeColor = (0.20, 0.42, 0.20)
        if SHOW_HULL_GHOST:
            hw = 36.0
            hb = POST_TOP_Z - STRAP_SAG + 0.5
            o = doc.addObject("Part::Feature", "hull_ghost_%d" % ci)
            o.Shape = Part.makeBox(52.0 * IN, hw * IN, 12.0 * IN,
                                   V((x0 - 26.0) * IN, -hw / 2.0 * IN, hb * IN))
            if GUI:
                o.ViewObject.ShapeColor = (0.55, 0.72, 0.85)
                o.ViewObject.Transparency = 80
    doc.recompute()


# =====================================================================
#  Hardware  —  procedurally modelled bolts / washers / nuts / screws
#  (visual only; grouped under "Hardware", not part of the joint solve)
# =====================================================================
def _carriage_bolt_shape():
    r  = BOLT_DIA / 2.0 * IN
    hr = HEAD_DIA / 2.0 * IN
    hh = HEAD_H * IN
    Rs = (hr * hr + hh * hh) / (2.0 * hh)          # sphere r for a cap of height hh, base radius hr
    sph = Part.makeSphere(Rs, V(0, 0, hh - Rs))
    dome = sph.common(Part.makeBox(4 * Rs, 4 * Rs, hh + 0.01 * IN,
                                   V(-2 * Rs, -2 * Rs, -0.005 * IN)))   # cap, z in [0, hh]
    dome.Placement = App.Placement(V(0, 0, 0), App.Rotation(V(1, 0, 0), 180))  # flat face at z=0, dome -> -z
    nk = NECK * IN
    neck  = Part.makeBox(nk, nk, nk, V(-nk / 2.0, -nk / 2.0, 0))
    shank = Part.makeCylinder(r, BOLT_LEN * IN, V(0, 0, 0))
    return dome.fuse(neck).fuse(shank)


def _fender_washer_shape():
    t = WASHER_T * IN
    return (Part.makeCylinder(WASHER_OD / 2.0 * IN, t)
            .cut(Part.makeCylinder(WASHER_ID / 2.0 * IN, 3 * t, V(0, 0, -t))))


def _hex_nut_shape():
    af = NUT_AF * IN
    t  = NUT_T * IN
    cr = af / 2.0 / math.cos(math.radians(30))
    pts = [V(cr * math.cos(math.radians(60 * i)),
             cr * math.sin(math.radians(60 * i)), 0) for i in range(6)]
    pts.append(pts[0])
    nut = Part.Face(Part.makePolygon(pts)).extrude(V(0, 0, t))
    return nut.cut(Part.makeCylinder(BOLT_DIA / 2.0 * IN * 1.03, 3 * t, V(0, 0, -t)))


def _screw_head_shape():
    """A flush countersunk head + a short shank stub (local +Z = out of the wood)."""
    hr = SCREW_HEAD / 2.0 * IN
    sr = SCREW_DIA / 2.0 * IN
    hh = 0.10 * IN
    head  = Part.makeCone(sr, hr, hh, V(0, 0, -hh))          # countersink, flush at z=0
    disc  = Part.makeCylinder(hr, 0.03 * IN, V(0, 0, -0.03 * IN))
    shank = Part.makeCylinder(sr, SCREW_LEN * IN, V(0, 0, -SCREW_LEN * IN))
    return head.fuse(disc).fuse(shank)


_STEEL   = (0.62, 0.64, 0.67)
_STEEL_L = (0.72, 0.73, 0.75)


def add_hardware(doc):
    if not (ADD_HARDWARE or ADD_SCREWS):
        return
    grp = doc.addObject("App::DocumentObjectGroup", "Hardware")

    parts = {}
    def _part(name, shape, color):
        o = doc.addObject("Part::Feature", name)
        o.Shape = shape
        if GUI:
            o.ViewObject.Visibility = False
            try:
                o.ViewObject.ShapeColor = color
            except Exception:
                pass
        parts[name] = o
        return o
    if ADD_HARDWARE:
        _part("Carriage_Bolt", _carriage_bolt_shape(), _STEEL)
        _part("Fender_Washer", _fender_washer_shape(), _STEEL_L)
        _part("Hex_Nut",       _hex_nut_shape(),       _STEEL)
    if ADD_SCREWS:
        _part("Deck_Screw",    _screw_head_shape(),    _STEEL)
    doc.recompute()

    n = 0
    def link(base, plc, color=None):
        nonlocal n
        n += 1
        lk = doc.addObject("App::Link", "%s_%03d" % (base, n))
        lk.LinkedObject = parts[base]
        lk.Placement = plc
        grp.addObject(lk)

    def screw(pt, out_dir):
        link("Deck_Screw",
             App.Placement(V(pt[0] * IN, pt[1] * IN, pt[2] * IN),
                           App.Rotation(V(0, 0, 1), V(*out_dir))))

    binf = POST_SPACING / 2.0 - BOARD_T / 2.0       # post inner face |Y|
    d45  = math.sqrt(2.0) / 2.0
    offsets = [i * CRADLE_GAP for i in range(N_CRADLES)]
    for x0 in offsets:
        for s in (-1.0, 1.0):
            inface = s * binf
            Rn = App.Rotation(V(1, 0, 0), -90.0 if s > 0 else 90.0)  # local +Z -> s*Y
            pz = (POST_TOP_Z - BOLT_DROP) * IN
            if ADD_HARDWARE:
                # Dome head seats straight against the wood on the inside (no
                # washer needed there -- wood doesn't need load spread the way
                # webbing does). Going outboard from there: post thickness,
                # then the webbing itself (it wraps the OUTSIDE face), then the
                # washer sits flush on the webbing's outside, then the nut
                # flush on the washer -- each one touching the last, no gaps
                # and no overlap with the strap.
                for dx in (-BOLT_GAP / 2.0, BOLT_GAP / 2.0):
                    px = (x0 + dx) * IN
                    def at(off_in):     # world point on the bolt axis, off_in outboard of the inner face
                        return V(px, (inface + s * off_in) * IN, pz)
                    link("Carriage_Bolt", App.Placement(at(0.0), Rn))
                    link("Fender_Washer", App.Placement(at(BOARD_T + STRAP_THICK), Rn))
                    link("Hex_Nut",       App.Placement(at(BOARD_T + STRAP_THICK + WASHER_T), Rn))
            if ADD_SCREWS:
                btip_z = RAIL_TOP_Z + binf          # brace/post meeting height
                # brace top -> post: horizontal screw from the brace, ~1.35"
                # below the brace/post tip, biting ~1.5" into the post
                # (hand-tuned on the R side, mirrored to the L side)
                screw((x0, s * (binf - 1.5358), btip_z - 1.3528), (0.0, -s, 0.0))
                # brace -> rail: driven DOWN through the brace's bottom end
                # (near its tip, where it meets the rail) into the rail --
                # accessible from the brace's top face once the frame is
                # standing (hand-tuned on the L side, mirrored to the R side;
                # flipped from the old up-through-the-rail-from-below approach)
                screw((x0, s * 1.35, RAIL_TOP_Z + 1.53), (0.0, 0.0, 1.0))
                # tie the junction down to the foot: 2 up through the foot into
                # the post, 2 down through the rail end into the foot.  All sit
                # 1 in off the board centreline (2 in apart -> 3/4 in edge
                # distance on the 3.5 in face) and are matched on both feet.
                for ex in (-1.0, 1.0):
                    screw((x0 + ex, s * (POST_SPACING / 2.0), 0.0),
                          (0.0, 0.0, -1.0))               # foot -> post, from below
                    screw((x0 + ex, s * (binf - 1.0), RAIL_TOP_Z),
                          (0.0, 0.0, 1.0))                # rail end -> foot, from above
                # down through the foot stretcher into this foot
                if ADD_STRETCHER:
                    screw((x0 + FOOT_LEN / 2.0 - BOARD_W / 2.0, s * (binf - 0.75),
                           RAIL_TOP_Z), (0.0, 0.0, 1.0))
    doc.recompute()


# =====================================================================
#  Cut list
# =====================================================================
def _fmt(x):
    whole = int(x)
    e = int(round((x - whole) * 8))
    if e == 8:
        whole, e = whole + 1, 0
    names = {0: "", 1: "-1/8", 2: "-1/4", 3: "-3/8", 4: "-1/2",
             5: "-5/8", 6: "-3/4", 7: "-7/8"}
    return '%d%s"' % (whole, names[e])


STOCK_LEN = 96.0     # a "2x4x8" is 96 in


def print_cutlist():
    rows = [
        ("Post",           2, POST_LEN,     "square ends; stand on the feet, outer faces flush with the feet outer edges"),
        ("Bottom rail",    1, RAIL_LEN,     "square ends; laid flat, fits between the posts; rests on the feet at its ends"),
        ("V-brace",        2, BRACE_LEN,    "45 deg bevel each end, PERPENDICULAR to each other (not parallel -- flip the board between cuts); bottom on rail, top flush to post; meet at rail centre"),
        ("Foot",           2, FOOT_LEN,     "square ends; round the top corners; set 1in inboard so its outer edge is flush with the post"),
    ]
    if ADD_STRETCHER:
        rows.append(("Foot stretcher", 1, STRETCH_SPAN, "laid flat across both feet"))

    m = ["", "=" * 62,
         " KAYAK CRADLE  -  cut list PER CRADLE  (build %d for the boat)" % BUILD_QTY,
         " 2x4 stock (actual %.1f x %.1f in)" % (BOARD_T, BOARD_W), "=" * 62]
    for part, qty, length, note in rows:
        m.append("  %-16s x%d  %-16s %s" % (part, qty, _fmt(length) + ('' if part != 'V-brace' else ' long edge'), note))

    # --- shopping / board estimate for the whole build ---
    pieces = []
    for part, qty, length, _ in rows:
        pieces += [(part, length)] * (qty * BUILD_QTY)
    total_in = sum(p[1] for p in pieces)
    # greedy first-fit-decreasing bin pack into 96 in boards (kerf ~0.125 per cut)
    boards = []
    for part, length in sorted(pieces, key=lambda x: -x[1]):
        for b in boards:
            if b["left"] >= length + 0.15:
                b["left"] -= length + 0.15
                b["cuts"].append((part, length))
                break
        else:
            boards.append({"left": STOCK_LEN - length - 0.15, "cuts": [(part, length)]})

    m += ["-" * 62,
          "  Posts %s apart on centre  |  loaded sling low point ~%s off ground"
          % (_fmt(POST_SPACING), _fmt(POST_TOP_Z - STRAP_SAG)),
          "  Set the %d cradles %s apart along the hull." % (BUILD_QTY, _fmt(CRADLE_GAP)),
          "=" * 62,
          " SHOPPING  (all %d cradles):  %d pieces, %.0f board-feet" % (BUILD_QTY, len(pieces), total_in / 12.0),
          "   -> BUY %d x 2x4x8 (96 in)" % len(boards), ""]
    for i, b in enumerate(boards, 1):
        segs = "  +  ".join("%s %s" % (p, _fmt(L)) for p, L in b["cuts"])
        m.append("   Board %d:  %s   (offcut ~%s)" % (i, segs, _fmt(max(b["left"], 0))))
    m += ["=" * 62, ""]
    App.Console.PrintMessage("\n".join(m) + "\n")


# =====================================================================
#  Display fixup  --  explicit, idempotent visibility/appearance pass.
#  New objects created through the plain API (no user driving the GUI)
#  can end up with whatever ViewObject defaults FreeCAD feels like that
#  session, which is how this model has repeatedly opened to a blank 3D
#  view.  Rather than rely on defaults, force every object into the
#  state we actually want, every time this script runs.
# =====================================================================
_MASTER_NAMES = ("Post", "Bottom_Rail", "Foot", "Foot_Stretcher", "V_Brace",
                 "Carriage_Bolt", "Fender_Washer", "Hex_Nut", "Deck_Screw")
_HIDE_TYPES = ("App::Origin", "App::Plane", "App::Line", "App::Point",
               "Assembly::JointGroup", "App::FeaturePython",
               "Assembly::BomGroup", "Assembly::BomObject",
               "Sketcher::SketchObject")


def fix_display(doc):
    if not GUI:
        return
    import FreeCADGui as Gui
    gd = Gui.getDocument(doc)
    for o in doc.Objects:
        vo = gd.getObject(o.Name)
        if vo is None:
            continue
        try:
            if o.Name in _MASTER_NAMES or o.TypeId in _HIDE_TYPES:
                vo.Visibility = False
                continue
            vo.Visibility = True
            if hasattr(vo, "DisplayMode"):
                modes = list(vo.listDisplayModes()) if hasattr(vo, "listDisplayModes") else []
                vo.DisplayMode = "Flat Lines" if ("Flat Lines" in modes or not modes) else modes[0]
        except Exception:
            pass
    doc.recompute()


# =====================================================================
#  Main
# =====================================================================
def main():
    for d in list(App.listDocuments().keys()):
        if d == DOC_NAME:
            App.closeDocument(d)
    doc = App.newDocument(DOC_NAME)

    bodies = build_bodies(doc)
    build_assembly(doc, bodies)
    add_references(doc)
    add_hardware(doc)
    doc.recompute()
    fix_display(doc)

    if GUI:
        try:
            import FreeCADGui as Gui
            Gui.activeDocument().activeView().viewIsometric()
            Gui.SendMsgToActiveView("ViewFit")
        except Exception:
            pass

    print_cutlist()

    if not GUI:
        here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
        doc.saveAs(os.path.join(here, DOC_NAME + ".FCStd"))
        try:
            Part.export([o for o in doc.Objects if o.isDerivedFrom("Part::Feature")
                         or o.isDerivedFrom("PartDesign::Body")],
                        os.path.join(here, DOC_NAME + ".step"))
        except Exception as e:
            App.Console.PrintWarning("STEP export skipped: %s\n" % e)
        App.Console.PrintMessage("Saved %s.FCStd\n" % DOC_NAME)


main()
