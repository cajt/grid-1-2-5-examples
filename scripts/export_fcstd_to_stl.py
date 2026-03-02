#!/usr/bin/env python3
import sys
import os
import FreeCAD
import Mesh

# ---------- argument handling (FreeCAD 0.19 safe) ----------
argv = sys.argv
if '--' in argv:
    argv = argv[argv.index('--') + 1:]
else:
    argv = argv[1:]

if len(argv) != 2:
    print("Usage: freecadcmd -c export_fcstd_to_stl.py -- input.FCStd output.stl")
    sys.exit(1)

input_file = os.path.abspath(argv[0])
output_file = os.path.abspath(argv[1])

if not os.path.isfile(input_file):
    raise RuntimeError("Input file does not exist: {}".format(input_file))

# ensure output directory exists
out_dir = os.path.dirname(output_file)
if out_dir and not os.path.isdir(out_dir):
    os.makedirs(out_dir)

# ---------- open document safely ----------
doc_name = os.path.splitext(os.path.basename(input_file))[0]

if doc_name in FreeCAD.listDocuments():
    doc = FreeCAD.getDocument(doc_name)
else:
    doc = FreeCAD.openDocument(input_file)

FreeCAD.setActiveDocument(doc.Name)

# ---------- resolve active body ----------
active = doc.ActiveObject

if active is None:
    raise RuntimeError("No active object in document.")

# Case 1: active object IS a body
if active.TypeId == "PartDesign::Body":
    body = active

# Case 2: active object is a feature inside a body
elif hasattr(active, "getParentGeoFeatureGroup"):
    body = active.getParentGeoFeatureGroup()
else:
    raise RuntimeError(
        "Cannot resolve active Body from active object type: {}".format(active.TypeId)
    )

if body is None or body.TypeId != "PartDesign::Body":
    raise RuntimeError("Resolved object is not a PartDesign Body.")

if body.Tip is None:
    raise RuntimeError("Body has no Tip.")

shape = body.Tip.Shape
if shape.isNull():
    raise RuntimeError("Body Tip shape is null.")

print("Exporting Body:", body.Name)
print("Tip Feature:", body.Tip.Name)

mesh = Mesh.Mesh()
mesh.addFacets(shape.tessellate(0.1))
mesh.write(output_file)

print("Export completed:", output_file)