import open3d as o3d
from pxr import Usd, UsdGeom, Sdf, Gf, Vt
import os
import numpy as np

def obj_to_usd_mesh(obj_path, usd_path, meters_per_unit=1.0):
    mesh = o3d.io.read_triangle_mesh(obj_path)
    if len(mesh.vertices) == 0:
        raise ValueError("Empty mesh.")
    verts = np.asarray(mesh.vertices, dtype=np.float32)
    faces = np.asarray(mesh.triangles, dtype=np.int32)
    os.makedirs(os.path.dirname(usd_path), exist_ok=True)
    stage = Usd.Stage.CreateNew(usd_path)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, meters_per_unit)
    root = UsdGeom.Xform.Define(stage, Sdf.Path("/Asset"))
    stage.SetDefaultPrim(root.GetPrim())
    mesh_prim = UsdGeom.Mesh.Define(stage, Sdf.Path("/Asset/Mesh"))
    vt_verts = Vt.Vec3fArray([Gf.Vec3f(float(v[0]), float(v[1]), float(v[2])) for v in verts])
    vt_faces = Vt.IntArray(faces.flatten().tolist())
    face_vertex_counts = Vt.IntArray([3] * len(faces))
    mesh_prim.CreatePointsAttr(vt_verts)
    mesh_prim.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh_prim.CreateFaceVertexIndicesAttr(vt_faces)
    stage.Save()
    print(f"Saved USD mesh asset: {usd_path}")

# 用法
obj_to_usd_mesh("data/demo4/name_mesh.obj", "data/demo4/name_mesh.usd")