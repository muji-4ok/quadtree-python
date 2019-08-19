class Rectangle:
    def __init__(self, center_x: int, center_y: int, half_width: int, half_height: int):
        self.center_x = center_x
        self.center_y = center_y
        self.half_width = half_width
        self.half_height = half_height

    def __contains__(self, item: tuple):
        left = self.center_x - self.half_width
        right = self.center_x + self.half_width
        top = self.center_y - self.half_height
        bot = self.center_y + self.half_height
        x, y = item

        return left <= x < right and top <= y < bot

    def intersects(self, bound):
        sdx = self.center_x - self.half_width, self.center_x + self.half_width
        sdy = self.center_y - self.half_height, self.center_y + self.half_height
        bdx = bound.center_x - bound.half_width, bound.center_x + bound.half_width
        bdy = bound.center_y - bound.half_height, bound.center_y + bound.half_height

        return max(sdx[0], bdx[0]) <= min(sdx[1], bdx[1]) and max(sdy[0], bdy[0]) <= min(sdy[1], bdy[1])


class QuadTree:
    def __init__(self, capacity, boundary):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.children = None
        self.count = 0

    def query(self, bound):
        if not self.boundary.intersects(bound):
            return []
        else:
            common_points = []

            if self.points is not None:
                for point in self.points:
                    if point in bound:
                        common_points.append(point)
            else:
                for child in self.children:
                    common_points += child.query(bound)

            return common_points

    def insert(self, point):
        if point not in self.boundary:
            return False

        self.count += 1

        if self.children:
            for child in self.children:
                if child.insert(point):
                    break
        else:
            self.points.append(point)

            if len(self.points) > self.capacity:
                self.divide()

        return True

    def divide(self):
        self.children = []

        x = self.boundary.center_x
        y = self.boundary.center_y
        fw = self.boundary.half_width / 2
        fh = self.boundary.half_height / 2

        ne = QuadTree(self.capacity, Rectangle(x + fw, y - fh, fw, fh))
        nw = QuadTree(self.capacity, Rectangle(x - fw, y - fh, fw, fh))
        sw = QuadTree(self.capacity, Rectangle(x - fw, y + fh, fw, fh))
        se = QuadTree(self.capacity, Rectangle(x + fw, y + fh, fw, fh))

        self.children.append(ne)
        self.children.append(nw)
        self.children.append(sw)
        self.children.append(se)

        while self.points:
            point = self.points.pop()

            for child in self.children:
                if child.insert(point):
                    break

        self.points = None
