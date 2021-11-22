import pywavefront
from tqdm import tqdm
import sys


if __name__ == "__main__":

    assert len(sys.argv) > 0 , "Usage : python3 get_points_and_edges.py file_name.obj"

    file_name = sys.argv[1]


    file_name_without_extention = file_name.split('.')[0]

    scene = pywavefront.Wavefront(file_name, strict=True, encoding="iso-8859-1", parse=False)
    scene.parse()  # Explicit call to parse() needed when parse=False

    points = []
    edges = []

    # Iterate vertex data collected in each material
    for name, material in scene.materials.items():

        for i in tqdm(range(0, len(material.vertices), 6)):
            point1 = material.vertices[i:i+3]
            point2 = material.vertices[i+3:i+6]
            if point1 not in points:
                points.append(point1)
            if point2 not in points:
                points.append(point2)

            edge = [points.index(point1), points.index(point2)]
            edge_inv = [points.index(point2), points.index(point1)]

            if edge not in edges and edge_inv not in edges:
                edges.append(edge)


with open(file_name_without_extention + '.xyz', 'x') as file_xyz:
    for point in points:
        file_xyz.write(f"{point[0]} {point[1]} {point[2]}\n")

with open(file_name_without_extention + '.edges', 'x') as file_edges:
    for edge in edges:
        file_edges.write(f"{edge[0]} {edge[1]}\n")