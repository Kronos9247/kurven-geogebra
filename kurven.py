from string import ascii_uppercase

"""
A, B, C, ...
"""

charset = ascii_uppercase[:26]
charset = [ char for char in charset ]
charset = filter(lambda char: char != "E", charset)
charset = list(charset)

points = 2 # min 1

def isint(name):
    try:
        int(name)
        return True
    except:
        return False

def to_point(name):
    if isint(name):
        return "E_{" + str(name) + "}"
    else:
        return name

def interpolate_axis(pointA, pointB, coordinate="x"):
    return "{0}({2}) * t + {0}({1}) * (1 - t)".format(coordinate, pointA, pointB)

def interpolate(pointA, pointB, point):
    pointA = to_point(pointA)
    pointB = to_point(pointB)
    point = to_point(point)

    return point + "=(" + interpolate_axis(pointA, pointB) + ", " + interpolate_axis(pointA, pointB, coordinate="y") + ")"

def interpolate_tree(points, depth=0):
    commands = []
    _points = dict()
    for i in range(len(points) - 1):
        _points[i] = interpolate(points[i], points[i + 1], to_point(i + depth))
        commands.append(_points[i])

    if len(points) > 2:
        new_points = list(_points.keys())
        commands.append(interpolate_tree(new_points, depth=depth + len(new_points)))
    return "\n".join(commands)

if __name__ == "__main__":
    if points >= len(charset):
        raise ValueError
    
    print(interpolate_tree([ "A", "B", "C" ]))

    