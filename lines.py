import xml.etree.ElementTree as ET
from kurven import charset, to_point, isint

def build_line(root, a, b, name):
    element = ET.SubElement(root, 'command')
    element.set("name", "Segment")

    sub_element = ET.SubElement(element, 'input')
    sub_element.set("a0", str(a))
    sub_element.set("a1", str(b))
    sub_element = ET.SubElement(element, 'output')
    sub_element.set("a0", str(name))

    return element

def interpolate(pointA, pointB, point):
    pointA = to_point(pointA)
    pointB = to_point(pointB)

    return [pointA, pointB, str(pointA).lower()]

def interpolate_tree(points, depth=0):
    commands = []
    _points = dict()
    for i in range(len(points) - 1):
        point_name = to_point(i + depth)
        if len(points) == 2:
            point_name = "E"
        
        _points[i] = interpolate(points[i], points[i + 1], point_name)
        commands.append(_points[i])

    if len(points) > 2:
        new_points = list(_points.keys())
        new_points = map(lambda point: point + depth, new_points)
        new_points = list(new_points)

        commands.extend(interpolate_tree(new_points, depth=depth + len(new_points)))
    return commands

if __name__ == "__main__":
    print(interpolate_tree([ "A", "B", "C" ]))

def build_expressions(effectors=1):
    if effectors >= len(charset) and effectors < 0:
        raise ValueError

    exprs = interpolate_tree(charset[:effectors + 1])
    return exprs
