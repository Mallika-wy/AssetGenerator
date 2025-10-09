"""
python ply_to_usd_mesh.py <ply_path> <usd_path> [--meters_per_unit <meters_per_unit>] [--mesh_simplify_target <mesh_simplify_target>]
python ply_to_usd_mesh.py data/demo1/colmap/dense/0/fused.ply data/demo1/fused.usd
"""

import os
import numpy as np
import open3d as o3d
from pxr import Usd, UsdGeom, Sdf, Gf, Vt

def ply_to_usd_mesh(ply_path: str, usd_path: str, meters_per_unit: float = 1.0, mesh_simplify_target: int = 0):
    """
    方案B：PLY点云->重建网格->USD网格（UsdGeom.Mesh）。
    :param ply_path: 输入PLY点云路径
    :param usd_path: 输出USD文件路径
    :param meters_per_unit: 单位（如毫米为0.001，米为1.0）
    :param mesh_simplify_target: 网格简化目标面数（0为不简化）
    """
    # 1. 读取点云
    pcd = o3d.io.read_point_cloud(ply_path)
    if len(pcd.points) == 0:
        raise ValueError("Empty point cloud.")
    # 法线估计
    if not pcd.has_normals():
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30))
    # 2. 网格重建（Poisson）
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
    # 可选：去除孤立小组件
    mesh = mesh.remove_unreferenced_vertices()
    mesh = mesh.remove_degenerate_triangles()
    mesh = mesh.remove_duplicated_triangles()
    mesh = mesh.remove_duplicated_vertices()
    mesh = mesh.remove_non_manifold_edges()
    # 可选：简化网格
    if mesh_simplify_target > 0 and len(mesh.triangles) > mesh_simplify_target:
        mesh = mesh.simplify_quadric_decimation(mesh_simplify_target)
    mesh.compute_vertex_normals()
    verts = np.asarray(mesh.vertices, dtype=np.float32)
    faces = np.asarray(mesh.triangles, dtype=np.int32)
    has_colors = mesh.has_vertex_colors()
    # 3. 新建USD舞台
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
    # 可选：颜色
    if has_colors:
        cols = np.asarray(mesh.vertex_colors, dtype=np.float32)
        cols = np.clip(cols, 0.0, 1.0)
        vt_cols = Vt.Vec3fArray([Gf.Vec3f(float(c[0]), float(c[1]), float(c[2])) for c in cols])
        pv_api = UsdGeom.PrimvarsAPI(mesh_prim.GetPrim())
        pv = pv_api.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.vertex)
        pv.Set(vt_cols)
    # 法线
    if mesh.has_vertex_normals():
        nrm = np.asarray(mesh.vertex_normals, dtype=np.float32)
        vt_nrm = Vt.Vec3fArray([Gf.Vec3f(float(n[0]), float(n[1]), float(n[2])) for n in nrm])
        mesh_prim.CreateNormalsAttr(vt_nrm)
        mesh_prim.SetNormalsInterpolation(UsdGeom.Tokens.vertex)
    # extent
    min_xyz = verts.min(axis=0)
    max_xyz = verts.max(axis=0)
    extent = Vt.Vec3fArray([Gf.Vec3f(float(min_xyz[0]), float(min_xyz[1]), float(min_xyz[2])),
                                Gf.Vec3f(float(max_xyz[0]), float(max_xyz[1]), float(max_xyz[2]))])
    mesh_prim.CreateExtentAttr(extent)
    stage.Save()
    print(f"Saved USD mesh asset: {usd_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PLY点云->网格->USD网格（方案B）")
    parser.add_argument("ply_path", type=str, help="输入PLY点云路径")
    parser.add_argument("usd_path", type=str, help="输出USD文件路径")
    parser.add_argument("--meters_per_unit", type=float, default=1.0, help="单位（如毫米为0.001，米为1.0）")
    parser.add_argument("--mesh_simplify_target", type=int, default=0, help="网格简化目标面数（0为不简化）")
    args = parser.parse_args()
    ply_to_usd_mesh(args.ply_path, args.usd_path, args.meters_per_unit, args.mesh_simplify_target)
