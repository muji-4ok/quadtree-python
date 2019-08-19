import pygame as p
from random import randint
import argparse
from quadtree import *

WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 50, 255, 50
WIDTH = 800
HEIGHT = 600
SIZE = WIDTH, HEIGHT
CAPACITY = 16


def draw_qt(tree: QuadTree, screen):
    x = tree.boundary.center_x - tree.boundary.half_width
    y = tree.boundary.center_y - tree.boundary.half_height
    w = tree.boundary.half_width * 2
    h = tree.boundary.half_height * 2

    p.draw.rect(screen, WHITE, p.Rect(x, y, w + 1, h + 1), 1)

    if tree.children:
        for child in tree.children:
            draw_qt(child, screen)


def launch_demo(count: int, width: int, height: int, quadrant_capacity: int, show_quadtree: bool):
    p.init()
    p.font.init()
    font = p.font.SysFont('Comic Sans MS', 40)
    size = width, height
    screen = p.display.set_mode(size)
    clock = p.time.Clock()

    main_bound = Rectangle(width // 2, height // 2, width // 2, height // 2)
    qt = QuadTree(quadrant_capacity, main_bound)
    points = []

    for _ in range(count):
        points.append((randint(0, width - 1), randint(0, height - 1)))

    points = set(points)

    for point in points:
        qt.insert(point)

    # Save screen with many points to surface, so we don't need to call thousands of expensive operations for
    # drawing individual pixels later, and can just blit the surface
    points_screen = p.Surface(size)
    points_screen.fill(BLACK)

    for point in points:
        points_screen.set_at(point, RED)

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            elif event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    exit_event = p.event.Event(p.QUIT, {})
                    p.event.post(exit_event)
            elif event.type == p.MOUSEMOTION:
                if p.mouse.get_pressed()[0]:
                    pos = p.mouse.get_pos()

                    if pos not in points:
                        points_screen.set_at(pos, RED)
                        points.add(pos)
                        qt.insert(pos)

        screen.fill(BLACK)
        x, y = p.mouse.get_pos()
        # Query boundary
        bound = Rectangle(x, y, 50, 50)
        x = bound.center_x - bound.half_width
        y = bound.center_y - bound.half_height
        w = bound.half_width * 2
        h = bound.half_height * 2
        queried = qt.query(bound)
        text = font.render(str(len(queried)), True, WHITE)
        screen.blit(points_screen, (0, 0))

        if show_quadtree:
            draw_qt(qt, screen)

        for point in queried:
            screen.set_at(point, GREEN)

        p.draw.rect(screen, GREEN, p.Rect(x, y, w, h), 1)
        screen.blit(text, (x, y))

        # Milliseconds since last frame, gives more information than fps
        fps = max(0.1, clock.get_fps())
        text = font.render("{:.2g}".format(1000 / fps), True, WHITE)
        screen.blit(text, (0, 0))

        p.display.flip()

        # Cap fps to 60
        clock.tick(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Demo of QuadTree class. You can add points by holding LMB')

    parser.add_argument('count', type=int, default=0, nargs='?',
                        help='Number of pregenerated random points on screen (default: %(default)s)')
    parser.add_argument('width', type=int, default=WIDTH, nargs='?', help='Width of window (default: %(default)s)')
    parser.add_argument('height', type=int, default=HEIGHT, nargs='?', help='Height of window (default: %(default)s)')
    parser.add_argument('--capacity', '-c', type=int, default=CAPACITY, required=False,
                        help='Maximum number of points that a quadrant can store before dividing')
    parser.add_argument('--show-quadtree', '-s', action='store_true', required=False,
                        help='Draw quadrants or not (default: %(default)s)')

    args = parser.parse_args()

    launch_demo(args.count, args.width, args.height, args.capacity, args.show_quadtree)
