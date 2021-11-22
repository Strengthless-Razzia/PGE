import pywavefront
scene = pywavefront.Wavefront('something.obj', strict=True, encoding="iso-8859-1", parse=False)
scene.parse()  # Explicit call to parse() needed when parse=False

# Iterate vertex data collected in each material
for name, material in scene.materials.items():
    # Contains the vertex format (string) such as "T2F_N3F_V3F"
    # T2F, C3F, N3F and V3F may appear in this string
    material.vertex_format
    # Contains the vertex list of floats in the format described above
    print(material.vertices)
    # Material properties
    material.diffuse
    material.ambient
    material.texture
    # ..