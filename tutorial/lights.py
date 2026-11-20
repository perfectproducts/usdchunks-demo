from pxr import Usd, UsdLux
st = Usd.Stage.Open("ladder_cam.usda")
UsdLux.DistantLight(st.GetPrimAtPath("/RenderLights/sun")).GetIntensityAttr().Set(900)
UsdLux.DomeLight(st.GetPrimAtPath("/RenderLights/sky")).GetIntensityAttr().Set(140)
st.Save()
