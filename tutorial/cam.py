"""Write <name>_cam.usda: the scene sublayered under a 3/4 camera that frames its bounds."""
import math, os, sys
from pxr import Usd, UsdGeom, Gf, Sdf

src, dst, el, az, zoom = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
st = Usd.Stage.Open(src)
bb = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default", "render"]).ComputeWorldBound(st.GetPseudoRoot()).ComputeAlignedRange()
c, size = bb.GetMidpoint(), bb.GetSize()
r = max(size) * zoom
e, a = math.radians(el), math.radians(az)
eye = c + Gf.Vec3d(r * math.cos(e) * math.sin(a), r * math.sin(e), r * math.cos(e) * math.cos(a))
out = Usd.Stage.CreateNew(dst)
out.GetRootLayer().subLayerPaths.append("./" + os.path.relpath(src, os.path.dirname(os.path.abspath(dst))).replace("\\", "/"))
UsdGeom.SetStageUpAxis(out, UsdGeom.Tokens.y)
cam = UsdGeom.Camera.Define(out, "/RenderCam")
cam.CreateFocalLengthAttr(35)
cam.CreateClippingRangeAttr(Gf.Vec2f(0.05, r * 10))
m = Gf.Matrix4d().SetLookAt(eye, c, Gf.Vec3d(0, 1, 0)).GetInverse()
UsdGeom.Xformable(cam).AddTransformOp().Set(m)
out.GetRootLayer().Save()
# Lights for RTX (Storm adds a headlight; RTX does not).
from pxr import UsdLux
sun = UsdLux.DistantLight.Define(out, "/RenderLights/sun")
sun.CreateIntensityAttr(1400); sun.CreateAngleAttr(1.5)
UsdGeom.Xformable(sun).AddRotateXYZOp().Set(Gf.Vec3f(-50, 30, 0))
dome = UsdLux.DomeLight.Define(out, "/RenderLights/sky")
dome.CreateIntensityAttr(250); dome.CreateColorAttr(Gf.Vec3f(0.75, 0.85, 1.0))
out.GetRootLayer().Save()
