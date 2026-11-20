"""A ladder whose rails, rungs and rung count follow three numbers:
    Rails.sy  the length      Rung.sx  the width      Rung.ty  the rung spacing

    python ladder.py   -> ladder_network.usda (the recipe) + ladder.usda (the result)
"""
from usd_chunks import Scene

with Scene.new() as scene:
    # -- the nodes, wired in order ---------------------------------------------------------
    gap = scene.create.vector_math_ops(operation="Scale", a=(1, 0, 0), name="Gap")    # (width, 0, 0)
    rise = scene.create.vector_math_ops(gap, operation="Scale", a=(0, 1, 0), name="Rise")  # (0, spacing, 0)

    rail = scene.create.usd_cube(rise, prim_path="/World/ladder/rail", name="RailBox")  # 1 m cube
    rails = scene.create.transform(rail, primpath_location="/World/ladder/rail", name="Rails",
                                   sx=0.06, sy=3.0, sz=0.06)                     # sy: LENGTH
    pair = scene.create.duplicate_prim(rails, source_prim="/World/ladder/rail",
                                       dest_path="/World/ladder/rails", copies=2, name="RailPair")

    rung = scene.create.usd_cube(pair, prim_path="/World/ladder/rung", name="RungBox")
    rung_x = scene.create.transform(rung, primpath_location="/World/ladder/rung", name="Rung",
                                    sx=0.5, sy=0.04, sz=0.05, ty=0.3)            # sx: WIDTH, ty: SPACING
    steps = scene.create.duplicate_prim(rung_x, source_prim="/World/ladder/rung",
                                        dest_path="/World/ladder/rungs", name="Steps")

    tidy = scene.create.prune_prim(steps, prim_path="/World/ladder/rail", name="DropRail")
    tidy = scene.create.prune_prim(tidy, prim_path="/World/ladder/rung", name="DropRung")
    scene.set_output(tidy)

    # -- the rules: everything else is worked out from the three drivers ------------------
    gap.get_param("scale").value = "@Rung.sx@"
    rise.get_param("scale").value = "@Rung.ty@"
    rails.get_param("ty").value = "@Rails.sy@ / 2"                       # stand on the ground
    rails.get_param("tx").value = "-@Rung.sx@ / 2"                       # left rail at the left edge
    pair.get_param("copy_translate").value = "@Gap.result@"              # right rail one width over
    steps.get_param("copies").value = "(@Rails.sy@ - 0.05) / @Rung.ty@"  # as many rungs as fit
    steps.get_param("copy_translate").value = "@Rise.result@"            # each one spacing higher

    scene.save("ladder_network.usda")
    scene.export("ladder.usda")
