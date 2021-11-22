import bpy

vertices = open("/home/remi/Documents/UPSSITECH/PGE/Blender/objet/plaque.xyz", "w")
edges = open("/home/remi/Documents/UPSSITECH/PGE/Blender/objet/plaque.edges", "w")

#vertices.write("Bonjour monde")
for vertex in bpy.data.objects['Plaque_1'].data.vertices:
    vertices.write("{} {} {}\n".format(vertex.co.x, vertex.co.y, vertex.co.z))
    
for edge in bpy.data.objects['Plaque_1'].data.edges:
    edges.write("{} {}\n".format(edge.vertices[0], edge.vertices[1]))

