from collections.abc import Collection
from math import *
import numpy as np
import copy

def degrees_to_radians(angle: int | float):
    """
    Convert degrees to radians.
    :param angle: The degrees.
    :return: Radians.
    """
    return np.pi / 180 * angle

def radians_to_degrees(angle: int | float):
    """
    Convert radians to degrees.
    :param angle: The radians.
    :return: Degrees.
    """
    return angle * 180 / np.pi


class Point:
    """
    Represents a point in 2D space.
    In other parts of the package, you can also use an iterable with two values instead of this class.
    :param x: X-coordinate
    :param y: Y-coordinate
    """
    def __init__(self, x: int | float, y: int | float = None):
        if y is not None:
            self.x, self.y = x, y
        elif isinstance(x, tuple) or isinstance(x, list):
            self.x, self.y = x
        else:
            raise ValueError(
                f"Cannot parse alternative point input format of {x}\n"
                f"Alternative point input formats: tuple(x, y), list[x, y]"
            )

    def set(self, x: int | float, y: int | float):
        """
        Set the X and Y coordinates.
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :return: None
        """
        self.x, self.y = x, y

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise NotImplementedError(
                f"Cannot add {type(other)} to {type(Point(0, 0))}"
            )

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise NotImplementedError(
                f"Cannot add {type(other)} to {type(Point(0, 0))}"
            )

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            raise NotImplementedError(
                f"Cannot add {type(other)} to {type(Point(0, 0))}"
            )

    def __div__(self, other):
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        else:
            raise NotImplementedError(
                f"Cannot add {type(other)} to {type(Point(0, 0))}"
            )

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Point({self.x}; {self.y})"


class Line:
    """
    Represents a line segment in 2D space.
    In other parts of the package, you can also use (Point, Point), ((x1, y1), (x2, y2)) and (x1, y1, x2, y2) instead of this class.
    :param p1: The first point.
    :param p2: The second point.
    """
    def __init__(self, p1: Point | Collection[int | float, int | float],
                       p2: Point | Collection[int | float, int | float] = None):
        if p2 is not None:
            self.p1, self.p2 = p1, p2
        elif isinstance(p1[0], Point):
            self.p1, self.p2 = p1[0], p1[1]
        elif len(p1) == 4:
            self.p1, self.p2 = Point(p1[0], p1[1]), Point(p1[2], p1[3])
        elif isinstance(p1[0], tuple) or isinstance(p1[0], list):
            self.p1, self.p2 = Point(*p1[0]), Point(*p1[1])
        else:
            raise ValueError(
                f"Cannot parse alternative line input format of {p1}\n"
                f"Alternative line input formats: (p1, p2), ((x1, y1), (x2, y2)), (x1, y1, x2, y2), tuples or lists"
            )

    def __repr__(self):
        return f"Line({self.p1} -> {self.p2})"


class Polygon:
    """
    Represents a polygon in 2D space. The first and the last points are also connected.
    In other parts of the package, you can also use (Point, ...) and the same thing with other point representations instead of this class.
    :param points: The points of the polygon.
    """
    def __init__(self, *points: Collection[Point] or Collection[Collection[int | float, int | float]]):
        self.points = list(points)
        for i, point in enumerate(points):
            if not isinstance(point, Point):
                self.points[i] = Point(point)

    def get_points(self):
        """
        Get the points.
        :return: points
        """
        return self.points

    def get_lines(self):
        """
        Get the lines of the polygon based on its points.
        :return: A tuple of Line objects.
        """
        lines = []
        for i in range(len(self.points)):
            current = self.points[i]
            next = self.points[(i+1)%len(self.points)]
            lines.append(Line(current, next))
        return tuple(lines)

    def __repr__(self):
        return "Polygon(" + " -> ".join(self.get_points()) + ")"


class Ellipse:
    """
    Represents an ellipse in 2D space.
    The centre is a point. See the Point class for more details.
    In other parts of the package, you can also use (Point, width, height), ((x, y), width, height) and (x, y, width, height) instead of this class.
    :param centre: The center point.
    :param width: The width.
    :param height: The height.
    """
    def __init__(self, centre: Point | Collection[int | float, int | float], width: int | float = None, height: int | float = None):
        if width is not None and height is not None:
            if not isinstance(centre, Point):
                self.centre = Point(centre)
            else:
                self.centre = centre
            self.width, self.height = width, height
        elif len(centre) == 3:
            if not isinstance(centre[0], Point):
                self.centre = Point(centre[0])
            else:
                self.centre = centre[0]
            self.width, self.height = centre[1], centre[2]
        elif len(centre) == 4:
            self.centre = Point(centre[0], centre[1])
            self.width, self.height = centre[2], centre[3]
        else:
            raise ValueError(
                f"Cannot parse alternative ellipse input format of {centre}\n"
                f"Alternative line input formats: (Point, width, height), ((x, y), width, height) and (x, y, width, height)"
            )

    def __repr__(self):
        return "Ellipse(" + str(self.centre) + "; " + str(self.width) + ", " + str(self.height) + ")"


class PointTools:
    @staticmethod
    def _parse_points(points: [Point | Collection[int | float, int | float]]):
        """
        Make sure all points in the collection are Point objects.
        For internal use.
        :param points: The input points.
        :return: [Point, ...]
        """
        points = list(points)
        for i, point in enumerate(points):
            if not isinstance(point, Point):
                points[i] = Point(point)
        return points

    @staticmethod
    def shift_points(points: [Point | Collection[int | float, int | float]], x: int | float, y: int | float):
        """
        Shift points.
        :param points: The points in a collection. See draw.Point for more details.
        :param x: The shifting along the X-axis.
        :param y: The shifting along the Y-axis.
        :return: The shifted points.
        """
        points = PointTools._parse_points(points)
        for point in points:
            point.x += x
            point.y += y
        return points

    @staticmethod
    def rotate_points(points: [Point | Collection[int | float, int | float]], angle: int | float,
                      centre: Point | Collection[int | float, int | float] = None):
        """
        Rotate points by some angle in degrees
        :param points: The points in a collection. See draw.Point for more details.
        :param angle: The angle in degrees.
        :param centre: The centre of rotation, a Point (or see draw.Point for more options). Default is None, centre is at 0, 0.
        :return: The rotated points.
        """
        points = PointTools._parse_points(points)
        centre = PointTools._parse_points([centre])[0]
        angle = degrees_to_radians(angle)
        if centre:
            points = PointTools.shift_points(points, -centre.x, -centre.y)
        for point in points:
            x, y = np.dot([[point.x], [point.y]],
                          [[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
            point.x, point.y = x[0], y[0]
        if centre:
            points = PointTools.shift_points(points, centre.x, centre.y)
        return points

    @staticmethod
    def scale_points(points: [Point | Collection[int | float, int | float]], x: int | float, y: int | float,
                     centre: Point | Collection[int | float, int | float] = None):
        """
        Scale points apart or closer together with a given centre.
        :param points: The points in a collection. See draw.Point for more details.
        :param x: The scaling along the X-axis.
        :param y: The scaling along the Y-axis.
        :param centre: The centre of scaling, a Point (or see draw.Point for more options). Default is None, centre is at 0, 0.
        :return: The scaled points.
        """
        points = PointTools._parse_points(points)
        centre = PointTools._parse_points([centre])[0]
        if centre:
            points = PointTools.shift_points(points, -centre.x, -centre.y)
        for point in points:
            point.x *= x
            point.y *= y
        if centre:
            points = PointTools.shift_points(points, centre.x, centre.y)
        return points


class ObjectCollection:
    """
    An object collection contains other objects (points, lines, polygons and ellipses, and even other object collections).
    Every object, of course, has its own position, but the whole of the collection can be shifted, scaled and rotated at once.
    :param objects: The objects. Point, Line, Polygon, Ellipse, ObjectCollection
    :param modified_objects: A deep copy of objects. This is the list that gets modified.
    :type objects: Point | Line | Polygon | Ellipse | ObjectCollection
    """
    def __init__(self, *objects):  # Because I can't type ObjectCollection in here, :type is used in the docstring.
        self.objects = objects
        self.modified_objects = copy.deepcopy(objects)

    def update_modified_objects(self):
        """
        Update the modified_objects list with the new objects from the objects list. Doesn't remove anything.
        :return: None
        """
        copy_ = copy.deepcopy(self.objects)
        self.modified_objects.extend(copy_[len(self.modified_objects):])

    def copy_objects_to_modified_objects(self):
        """
        Deep copy the objects to modified_objects completely. For updating, see self.update_mofified_objects.
        :return: None
        """
        self.modified_objects = copy.deepcopy(self.objects)

    def pop_last_object(self):
        """
        Pops the last object in the list from both objects and modified_objects.
        :return: The popped object from objects and modified_objects.
        """
        pop1 = self.objects.pop()
        pop2 = self.modified_objects.pop()
        return pop1, pop2

    def shift(self, shift_x: int | float, shift_y: int | float):
        """
        Shift all the objects in the collection.
        Restore all changes with self.restore().
        :param shift_x: Amount along the X-axis.
        :param shift_y: Amount along the Y-axis.
        :return: None
        """
        shift_point = Point(shift_x, shift_y)
        for object in self.modified_objects:
            if isinstance(object, Point):
                object += shift_point
            elif isinstance(object, Line):
                object.p1 += shift_point
                object.p2 += shift_point
            elif isinstance(object, Polygon):
                for i in range(len(object.points)):
                    object.points[i] += shift_point
            elif isinstance(object, Ellipse):
                object.centre += shift_point
            elif isinstance(object, ObjectCollection):
                object.shift(shift_x, shift_y)

    def rotate(self, angle: int | float, centre: Point | Collection[int | float, int | float] = None):
        """
        Rotate all the objects in the collection.
        Restore all changes with self.restore().
        WARNING: The Ellipse object cannot be rotated if it's not a circle. Only the centre point of the ellipse is rotated.
        :param angle: The angle of rotation in degrees.
        :param centre: The centre of rotation, a Point (or see draw.Point for more options). Default is None, centre is at 0, 0.
        :return: None
        """
        if centre is None: centre = Point(0, 0)
        elif not isinstance(centre, Point): centre = Point(centre)
        for object in self.modified_objects:
            if isinstance(object, Point):
                new = PointTools.rotate_points([object], angle, centre)[0]
                object.set(new.x, new.y)
            elif isinstance(object, Line):
                new_p1, new_p2 = PointTools.rotate_points([object.p1, object.p2], angle, centre)
                object.p1 = new_p1
                object.p2 = new_p2
            elif isinstance(object, Polygon):
                for i in range(len(object.points)):
                    new = PointTools.rotate_points([object.points[i]], angle, centre)[0]
                    object.points[i].set(new.x, new.y)
            elif isinstance(object, Ellipse):
                new = PointTools.rotate_points([object.centre], angle, centre)[0]
                object.centre.set(new.x, new.y)
            elif isinstance(object, ObjectCollection):
                object.rotate(angle, centre)

    def scale(self, scale_x: int | float, scale_y: int | float,
              centre: Point | Collection[int | float, int | float] = None):
        """
        Scale all objects in the collection.
        Restore all changes with self.restore().
        :param scale_x: The scaling along the X-axis.
        :param scale_y: The scaling along the Y-axis.
        :param centre: The centre of rotation, a Point (or see draw.Point for more options). Default is None, centre is at 0, 0.
        :return: None
        """
        if centre is None: centre = Point(0, 0)
        elif not isinstance(centre, Point): centre = Point(centre)
        scale_point = Point(scale_x, scale_y)  # for easier and shorter code, so I can use some_point *= scale_point
        for object in self.modified_objects:
            if isinstance(object, Point):
                object -= centre
                object *= scale_point
                object += centre
            elif isinstance(object, Line):
                object.p1 -= centre
                object.p2 -= centre
                object.p1 *= scale_point
                object.p2 *= scale_point
                object.p1 += centre
                object.p2 += centre
            elif isinstance(object, Polygon):
                for i in range(len(object.points)):
                    object.points[i] -= centre
                    object.points[i] *= scale_point
                    object.points[i] += centre
            elif isinstance(object, Ellipse):
                object.centre -= centre
                object.centre *= scale_point
                object.centre += centre
                object.width *= scale_x
                object.height *= scale_y
            elif isinstance(object, ObjectCollection):
                object.scale(scale_x, scale_y, centre)

    def restore(self):
        """
        Restore any shifts, rotations and scalings to the original values.
        :return:
        """
        self.modified_objects = copy.deepcopy(self.objects)

    def __repr__(self):
        orig = "; ".join([str(a) for a in self.objects])
        mod = "; ".join([str(a) for a in self.modified_objects])
        return "ObjectCollection Modified: [" + mod + "]" + " / Original: [" + orig + "]"