from string import ascii_uppercase

"""
A, B, C, ...
"""

charset = ascii_uppercase[:26]
charset = [ char for char in charset ]
charset = filter(lambda char: char != "E", charset)
charset = list(charset)

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
        point_name = to_point(i + depth)
        if len(points) == 2:
            point_name = "E"
        
        _points[i] = interpolate(points[i], points[i + 1], point_name)
        commands.append(_points[i])

    if len(points) > 2:
        new_points = list(_points.keys())
        new_points = map(lambda point: point + depth, new_points)
        new_points = list(new_points)

        commands.append(interpolate_tree(new_points, depth=depth + len(new_points)))
    return "\n".join(commands)


def build_points(count, offset=2):
    points = charset[:count + 1]
    points = [[point, "({}, 0)".format(i * offset)] for i, point in enumerate(points)] 
    
    return points
    
def build_expressions(effectors=1):
    if effectors >= len(charset) and effectors < 0:
        raise ValueError

    exprs = interpolate_tree(charset[:effectors + 1])
    exprs = exprs.split("\n")
    exprs = map(lambda expr: expr.split("="), exprs)
    exprs = list(exprs)

    return exprs

    