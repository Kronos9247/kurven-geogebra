from kurven import build_expressions, build_points, charset
from lines import build_expressions as build_lines
from lines import build_line

import xml.etree.ElementTree as ET
import zipfile


hide_effectors = True
show_lines = True

if __name__ == "__main__":
    tree = ET.parse('geogebra.xml')
    root = tree.getroot()

    construct = root.find('construction')

    total_points = 25
    exprs_points = build_expressions(total_points)
    effector_points = build_points(total_points)
    points = list(effector_points)
    points.extend(exprs_points)
    for expr in points:
        # <expression label="A" exp="(0, 0)" type="point"/>
        element = ET.SubElement(construct, 'expression')

        element.set("label", expr[0])
        element.set("exp", expr[1])
        element.set("type", "point")

    if hide_effectors:
        filtered_points = filter(lambda point: point[0] != "E", exprs_points)

        for point in filtered_points:
            element = ET.SubElement(construct, 'element')

            element.set("label", point[0])
            element.set("type", "point")
            show_element = ET.SubElement(element, 'show')
            show_element.set("object", "false")
            show_element.set("label", "false")

    if show_lines:
        for line in build_lines(total_points):
            build_line(construct, line[0], line[1], line[2])

    with zipfile.ZipFile("geogebra.ggb", "w") as file:
        file.writestr('geogebra.xml', ET.tostring(root))