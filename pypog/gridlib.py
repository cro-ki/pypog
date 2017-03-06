'''
    Grid objects

    ** By Cro-Ki l@b, 2017 **
'''
from math import sqrt


class BaseGrid(object):
    """ Base class for grids
    This class should be overriden """
    def __init__(self, width, height):
        """ instanciate a new BaseGrid object """
        self._width = 0
        self.width = width
        self._height = 0
        self.height = height

    def __repr__(self):
        return "<{} object>".format(self.__class__.__name__)

    @staticmethod
    def _assertCoordinates(*args):
        """ raise a ValueError if the args are not (x, y) iterables, where x and y are integers
        usage:
            self._assertCoordinates((x1, y1), (x2, y2), ...)
        """
        try:
            if all([isinstance(i, int) for x, y in args for i in (x, y)]):
                return
        except (TypeError, ValueError):
            pass
        raise ValueError("{} is not a valid (x, y) coordinates iterable".format(args))

    # properties
    @property
    def width(self):
        """ the width of the grid """
        return self._width

    @width.setter
    def width(self, width):
        """ set a new width for the grid.
        the new width has to be a strictly positive integer"""
        if not isinstance(width, int) or not width > 0:
            raise ValueError("'width' has to be a strictly positive integer")
        self._width = width

    @property
    def height(self):
        """ the height of the grid """
        return self._height

    @height.setter
    def height(self, height):
        """ set a new height for the grid.
        the new height has to be a strictly positive integer"""
        if not isinstance(height, int) or not height > 0:
            raise ValueError("'width' has to be a strictly positive integer")
        self._height = height

    # geometric methods
    def __len__(self):
        """ return the number of cells in the grid """
        return self.height * self.width

    def __contains__(self, key):
        """return True if the (x, y) coordinates are in the grid"""
        try:
            self._assertCoordinates(key)
        except ValueError:
            pass
        else:
            return 0 <= key[0] < self._width and 0 <= key[1] < self._height
        return False

    def __iter__(self):
        """ iterate over the coordinates of the grid """
        for item in ((x, y) for x in range(self.width) for y in range(self.height)):
            yield item
        raise StopIteration()

    @classmethod
    def _bounding_rect(cls, *args):
        """ return (xmin, ymin, xmax, ymax) from (x, y) coordinates """
        cls._assertCoordinates(*args)
        xs, ys = zip(*args)
        xs.sort()
        ys.sort()
        return xs[0], xs[-1], ys[0], ys[-1]

    # graphical methods
    @staticmethod
    def graphicsitem(x, y, scale=120):
        """ returns the list of the points which compose the (x, y) cell """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    # geometrical algorithms
    @classmethod
    def neighbors(cls, x, y):
        """ returns a list of the neighbors of (x, y) """
        return [key for key in cls._neighbors(x, y) if cls._is_in(key)]

    @classmethod
    def _neighbors(cls, x, y):
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def line(cls, x1, y1, x2, y2):
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def line3d(cls, x1, y1, z1, x2, y2, z2):
        """ returns a line from (x1 ,y1, z1) to (x2, y2, z2)
        as a list of (x, y, z) coordinates """
        if not all(isinstance(c, int) for c in [z1, z2]):
            raise TypeError("x1, y1, z1, x2, y2, z2 have to be integers")
        hoLine = cls.line(x1, y1, x2, y2)
        if z1 == z2:
            return [(x, y, z1) for x, y in hoLine]
        else:
            ligneZ = SquareGrid.line(0, z1, (len(hoLine) - 1), z2)
            return [(hoLine[d][0], hoLine[d][1], z) for d, z in ligneZ]

    @classmethod
    def zone(cls, x, y, radius):
        """ returns the list of the coordinates of the cells in a zone around (x, y)
        """
        cls._assertCoordinates((x, y))
        if not isinstance(radius, int):
            raise TypeError("radius has to be an integer (given: {})".format(radius))
        if not radius >= 0:
            raise ValueError("radius has to be positive")
        buffer = frozenset([(x, y)])

        for _ in range(0, radius):
            current = buffer
            for x, y in current:
                buffer |= frozenset(cls.neighbors(x, y))
        return list(buffer)

    @classmethod
    def triangle(cls, xa, ya, xh, yh, iAngle):
        """ return the list of the (x, y) coordinates in a triangle
        with (xa, ya) apex and (xh, yh) middle of the base """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def triangle3d(self, xa, ya, za, xh, yh, zh, iAngle):
        """Returns a list of (x, y, z) coordinates in a 3d-cone
        A is the top of the cone, H if the center of the base

        WARNING: result is a dictionary of the form {(x, y): (-z, +z)}

        This is for performance reason and because on a 2d grid, you generally don't need a complete list of z coordinates
        as you don't want to display them: you just want to know if an altitude is inside a range.

        That could change in later version
        """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def rectangle(cls, x1, y1, x2, y2):
        """return a list of cells in a rectangle between (X1, Y1), (X2, Y2)"""
        cls._assertCoordinates((x1, y1), (x2, y2))
        xa, ya, xb, yb = min([x1, x2]), min([y1, y2]), max([x1, x2]), max([y1, y2])
        return [(x, y) for x in range(xa, xb + 1) for y in range(ya, yb + 1)]

    @classmethod
    def hollow_rectangle(cls, x1, y1, x2, y2):
        """return a list of cells composing the sides of the rectangle between (X1, Y1), (X2, Y2)"""
        cls._assertCoordinates((x1, y1), (x2, y2))
        xmin, ymin, xmax, ymax = cls._bounding_rect((x1, y1), (x2, y2))
        return [(x, ymin) for x in range(xmin, xmax + 1)] + \
               [(x, ymax) for x in range(xmin, xmax + 1)] + \
               [(xmin, y) for y in range(ymin, ymax + 1)] + \
               [(xmax, y) for y in range(ymin, ymax + 1)]

    @classmethod
    def rotate(cls, center, coordinates, rotations):
        """ return the 'coordinates' list of (x, y) coordinates
        after a rotation of 'rotations' times around the (x, y) center """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

#     def moving_cost(self, *args):
#         return 1
#
#     def path(self, x1, y1, x2, y2):
#         raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

class SquareGrid(BaseGrid):
    """ Square grid object """
    def __init__(self, *args, **kwargs):
        BaseGrid.__init__(self, *args, **kwargs)

    @staticmethod
    def graphicsitem(x, y, scale=120):
        """ reimplemented from BaseGrid.graphicsitem """
        return  [
                    (x * scale, y * scale), \
                    ((x + 1) * scale, y * scale), \
                    ((x + 1) * scale, (y + 1) * scale), \
                    (x * scale, (y + 1) * scale)
                ]

    @classmethod
    def _neighbors(cls, x, y):
        """ reimplemented from BaseGrid._neighbors """
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), \
                (x - 1, y), (x + 1, y)  , \
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

    @classmethod
    def line(cls, x1, y1, x2, y2):
        """ reimplemented from BaseGrid.line
        Implementation of bresenham's algorithm
        """
        result = []

        if (x1, y1) == (x2, y2):
            return [(x1, y1)]

        # DIAGONAL SYMETRY
        V = (abs(y2 - y1) > abs(x2 - x1))
        if V: y1, x1, y2, x2 = x1, y1, x2, y2

        # VERTICAL SYMETRY
        reversed_sym = (x1 > x2)
        if reversed_sym:
            x2, y2, x1, y1 = x1, y1, x2, y2

        DX = x2 - x1 ; DY = y2 - y1
        offset = 0.0
        step = 1 if DY > 0 else -1
        alpha = (abs(DY) / DX)

        y = y1
        for x in range(x1, x2 + 1):
            coord = (y, x) if V else (x, y)
            result.append(coord)

            offset += alpha
            if offset > 0.5:
                y += step
                offset -= 1.0

        if reversed_sym:
            result.reverse()
        return result

    @classmethod
    def triangle(cls, xa, ya, xh, yh, iAngle):
        """ reimplemented from BaseGrid.triangle """
        if (xa, ya) == (xh, yh):
            return [(xa, ya)]

        result = []

        # direction vector
        dx_dir, dy_dir = xh - xa, yh - ya

        # normal vector
        dx_n, dy_n = -dy_dir, dx_dir

        # B and C positions
        k = 1 / (iAngle * sqrt(3))
        xb, yb = xh + (k * dx_n), yh + (k * dy_n)
        xc, yc = xh + (-k * dx_n), yh + (-k * dy_n)

        xb, yb = round(xb), round(yb)
        xc, yc = round(xc), round(yc)

        # sides:
        lines = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]

        # base (lower slope)
        x1, y1, x2, y2 = min(lines, key=lambda x: (abs ((x[3] - x[1]) / (x[2] - x[0])) if x[2] != x[0] else 10 ** 10))
        base = cls.line(x1, y1, x2, y2)
        y_base = y1
        lines.remove((x1, y1, x2, y2))

        # 'hat' (2 other sides)
        hat = []
        y_top = None
        for x1, y1, x2, y2 in lines:
            if y_top == None:
                y_top = y2
            hat.extend(cls.line(x1, y1, x2, y2))

        # sense (1 if top is under base, -1 if not)
        sense = 1 if y_top > y_base else -1

        # rove over y values from base to hat
        for x, y in base:
            while not (x, y) in hat:
                result.append((x, y))
                y += sense
        result.extend(hat)

        return result

    @classmethod
    def triangle3d(cls, xa, ya, za, xh, yh, zh, iAngle):
        """ reimplemented from BaseGrid.triangle3d """
        result = []

        flat_triangle = cls.triangle(xa, ya, xh, yh, iAngle)
        k = 1 / (iAngle * sqrt(3))

        length = max(abs(xh - xa), abs(yh - ya))

        vertical_line = cls.line(0, za, length, zh)

        # build a dict with X key and value is a list of Z values
        vertical_line_dict = {d:[] for d, z in vertical_line}
        for d, z in vertical_line:
            vertical_line_dict[d].append(z)

        # this is approximative: height is update according to the manhattan distance to center
        for x, y in flat_triangle:
            distance = int(max(abs(x - xa), abs(y - ya)))
            try:
                z_list = vertical_line_dict[ distance ]
            except KeyError:
                distance = length
                z_list = vertical_line_dict[ distance ]
            dh = int(k * distance) + 1 if distance > 0 else 0
            result[ (x, y) ] = ((min(z_list) - dh) , (max(z_list) + dh))
        return result


    @classmethod
    def rotate(cls, center, coordinates, rotations):
        """ reimplemented from BaseGrid.rotate """
        if coordinates == [center] or rotations % 4 == 0:
            return coordinates
        x0, y0 = center
        result = []
        for x, y in coordinates:
            dx, dy = x - x0, y - y0
            for _ in range(rotations):
                dx, dy = dy, -dx
            xr, yr = dx + x0, dy + y0
            result.append((xr, yr))
        return result

class _HexGrid(BaseGrid):
    """ Base class for hexagonal grids classes
    This class should be overridden """
    def __init__(self, *args, **kwargs):
        BaseGrid.__init__(self, *args, **kwargs)

    @staticmethod
    def cv_cube_off(xu, yu, zu):
        """convert cubic coordinates (xu, yu, zu) in standards coordinates (x, y) [offset]"""
        y = int(xu + (zu - (zu & 1)) / 2)
        x = zu
        return (x, y)

    @staticmethod
    def cv_off_cube(x, y):
        """converts standards coordinates (x, y) [offset] in cubic coordinates (xu, yu, zu)"""
        zu = x
        xu = int(y - (x - (x & 1)) / 2)
        yu = int(-xu - zu)
        return (xu, yu, zu)

    # > unused
    @staticmethod
    def cube_round(x, y, z):
        """returns the nearest cell (in cubic coords)
        x, y, z can be floating numbers, no problem."""
        rx, ry, rz = round(x), round(y), round(z)
        x_diff, y_diff, z_diff = abs(rx - x), abs(ry - y), abs(rz - z)
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return (rx, ry, rz)

    # > unused
    @staticmethod
    def hex_distance_cube(xa, ya, za, xb, yb, zb):
        """returns the manhattan distance between the two cells"""
        return max(abs(xa - xb), abs(ya - yb), abs(za - zb))

    # > unused
    @staticmethod
    def distance_off(xa, ya, xb, yb):
        """ distance between A and B (offset coordinates)"""
        # 10 times quicker if no conversion...
        xua, yua, zua = FHexGrid.cv_off_cube(xa, ya)
        xub, yub, zub = FHexGrid.cv_off_cube(xb, yb)
        return max(abs(xua - xub), abs(yua - yub), abs(zua - zub))


class FHexGrid(_HexGrid):
    """ Flat-hexagonal grid object """

    def __init__(self, *args, **kwargs):
        _HexGrid.__init__(self, *args, **kwargs)

    @staticmethod
    def graphicsitem(x, y, scale=120):
        """ reimplemented from BaseGrid.graphicsitem """
        if x % 2 != 0:
            y += 0.5
        return [
                   (((x * 0.866) + 0.2886) * scale , y * scale), \
                   (((x * 0.866) + 0.866) * scale  , y * scale), \
                   (((x * 0.866) + 1.1547) * scale , (y + 0.5) * scale), \
                   (((x * 0.866) + 0.866) * scale  , (y + 1) * scale), \
                   (((x * 0.866) + 0.2886) * scale , (y + 1) * scale), \
                   ((x * 0.866) * scale          , (y + 0.5) * scale)
                ]

    @classmethod
    def _neighbors(cls, x, y):
        if x % 2 == 0:
            return [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x, y + 1), (x - 1, y), (x - 1, y - 1)]
        else:
            return [(x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]

    @classmethod
    def line(cls, x1, y1, x2, y2):
        """ reimplemented from BaseGrid.line
        Implementation of bresenham's algorithm """
        if (x1, y1) == (x2, y2):
            return [(x1, y1)]

        reversed_sym = (x1 > x2)
        if reversed_sym:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if abs(x2 - x1) < (2 * abs((y2 - y1)) + abs(x2 % 2) - abs(x1 % 1)):
            # vertical quadrants

            # unit is half the width: u = 0.5773
            # half-height is then 0.8860u, or sqrt(3)/2
            direction = 1 if y2 > y1 else -1

            dx = 1.5 * (x2 - x1)
            dy = direction * (y2 - y1)
            if (x1 + x2) % 2 == 1:
                if x1 % 2 == 0:
                    dy += direction * 0.5
                else:
                    dy -= direction * 0.5

            k = dx / (dy * sqrt(3))
            pas = 0.5 * sqrt(3)

            result = []
            offset = 0.0
            pos = (x1, y1)
            result.append(pos)

            while pos != (x2, y2):
                offset += (k * pas)
                if offset <= 0.5:
                    x, y = pos
                    pos = x, y + direction
                    result.append(pos)
                    offset += (k * pas)
                else:
                    x, y = pos
                    if (x % 2 == 0 and direction == 1) or (x % 2 == 1 and direction == -1):
                        pos = x + 1, y
                    else:
                        pos = x + 1, y + direction
                    result.append(pos)
                    offset -= 1.5

                # in case of error in the algorithm, we should avoid infinite loop:
                if direction * pos[1] > direction * y2:
                    result = []
                    break

        else:
            # horizontal quadrants
            dx = x2 - x1 ; dy = y2 - y1
            if (x1 + x2) % 2 == 1:
                dy += 0.5 if x1 % 2 == 0 else -0.5

            k = dy / dx
            pas = 1

            result = []
            d = 0.0
            pos = (x1, y1)
            result.append(pos)

            while pos != (x2, y2):
                d += k * pas
                if d > 0:
                    x, y = pos
                    if x % 2 == 0:
                        pos = x + 1, y
                    else:
                        pos = x + 1, y + 1
                    result.append(pos)
                    d -= 0.5
                else:
                    x, y = pos
                    if x % 2 == 0:
                        pos = x + 1, y - 1
                    else:
                        pos = x + 1, y
                    result.append(pos)
                    d += 0.5

                # in case of error in the algorithm, we should avoid infinite loop:
                if pos[0] > x2:
                    result = []
                    break

        if reversed_sym:
            result.reverse()
        return result

    @classmethod
    def triangle(cls, xa, ya, xh, yh, iAngle):
        """ reimplemented from BaseGrid.triangle """
        if (xa, ya) == (xh, yh):
            return [(xa, ya)]

        result = []

        # convert to cubic coodinates (see 'cube_coords' lib)
        xua, yua, _ = cls.cv_off_cube(xa, ya)
        xuh, yuh, zuh = cls.cv_off_cube(xh, yh)

        # direction vector
        dx_dir, dy_dir = xuh - xua, yuh - yua

        # normal vector
        dx_n, dy_n = -(2 * dy_dir + dx_dir), (2 * dx_dir + dy_dir)
        dz_n = (-dx_n - dy_n)

        # B and C positions
        k = 1 / (iAngle * sqrt(3))
        xub, yub, zub = xuh + (k * dx_n), yuh + (k * dy_n), zuh + (k * dz_n)
        xuc, yuc, zuc = xuh + (-k * dx_n), yuh + (-k * dy_n), zuh + (-k * dz_n)

        xub, yub, zub = cls.cube_round(xub, yub, zub)
        xuc, yuc, zuc = cls.cube_round(xuc, yuc, zuc)

        xb, yb = cls.cv_cube_off(xub, yub, zub)
        xc, yc = cls.cv_cube_off(xuc, yuc, zuc)

        # sides
        segments = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]

        # base (lower slope)
        x1, y1, x2, y2 = min(segments, key=lambda x: (abs ((x[3] - x[1]) / (x[2] - x[0])) if x[2] != x[0] else 10 ** 10))
        base = cls.line(x1, y1, x2, y2)
        y_base = y1
        segments.remove((x1, y1, x2, y2))

        # 'hat' (the 2 other sides)
        chapeau = []
        y_sommet = None
        for x1, y1, x2, y2 in segments:
            if y_sommet == None:
                y_sommet = y2
            chapeau.extend(cls.line(x1, y1, x2, y2))

        # sense (1 if top is under base, -1 if not)
        sens = 1 if y_sommet > y_base else -1

        # rove over y values from base to hat
        for x, y in base:
            while not (x, y) in chapeau:
                result.append((x, y))
                y += sens
        result.extend(chapeau)

        return result

    @classmethod
    def triangle3d(cls, xa, ya, za, xh, yh, zh, iAngle):
        """ reimplemented from BaseGrid.triangle3d """

        flat_triangle = cls.triangle(xa, ya, xh, yh, iAngle)

        result = {}

        k = 1 / (iAngle * sqrt(3))

        # use cubic coordinates
        xua, yua, zua = cls.cv_off_cube(xa, ya)
        xuh, yuh, zuh = cls.cv_off_cube(xh, yh)

        length = max(abs(xuh - xua), abs(yuh - yua), abs(zuh - zua))

        vertical_line = SquareGrid.line(0, za, length, zh)

        # build a dict with X key and value is a list of Z values
        vertical_line_dict = {d:[] for d, z in vertical_line}
        for d, z in vertical_line:
            vertical_line_dict[d].append(z)

        # this is approximative: height is update according to the manhattan distance to center
        for x, y in flat_triangle:
            xu, yu, zu = cls.cv_off_cube(x, y)
            distance = int(max(abs(xu - xua), abs(yu - yua), abs(zu - zua)))
            try:
                z_list = vertical_line_dict[ distance ]
            except KeyError:
                distance = length
                z_list = vertical_line_dict[ distance ]
            dh = int(k * distance) + 1 if distance > 0 else 0
            result[ (x, y) ] = ((min(z_list) - dh) , (max(z_list) + dh))
        return result

    @classmethod
    def rotate(cls, center, coordinates, rotations):
        """ reimplemented from BaseGrid.rotate """
        if coordinates == [center] or rotations % 6 == 0:
            return coordinates
        x0, y0 = center
        xu0, yu0, zu0 = cls.cv_off_cube(x0, y0)
        result = []

        for x, y in coordinates:
            xu, yu, zu = cls.cv_off_cube(x, y)
            dxu, dyu, dzu = xu - xu0, yu - yu0, zu - zu0
            for _ in range(rotations):
                dxu, dyu, dzu = -dzu, -dxu, -dyu
            xru, yru, zru = dxu + xu0, dyu + yu0, dzu + zu0
            xr, yr = cls.cv_cube_off(xru, yru, zru)
            result.append((xr, yr))
        return result



