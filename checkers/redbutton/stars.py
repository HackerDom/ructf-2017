from pngcanvas import *
from os import urandom
from random import random

import numpy
import math

W = 256
H = 256

def rough_line(canvas, x1, y1, x2, y2):
	x1 = int(x1)
	y1 = int(y1)
	x2 = int(x2)
	y2 = int(y2)

	dx = x2 - x1
	dy = y2 - y1

	is_steep = abs(dy) > abs(dx)

	if is_steep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2

	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1

	dx = x2 - x1
	dy = y2 - y1

	error = dx // 2
	ystep = 1 if y1 < y2 else -1

	y = y1
	for x in range(x1, x2 + 1):
		coord = (y, x) if is_steep else (x, y)
		canvas.point(*coord)
		error -= abs(dy)
		if error < 0:
			y += ystep
			error += dx

def place_stars(canvas):
	seed = urandom(W * H + 1)

	for x in range(W):
		for y in range(H):
			s = (seed[x * H + y] << 8) + seed[x * H + y + 1]
			if s > 200:
				continue
			if s > 10:
				brightness = s & 0x7f
			else:
				brightness = s & 0xff
			if brightness:
				canvas.point(x, y, (brightness, brightness, brightness, 0xff))

def rotate(vec, angle):
	angle = numpy.pi / 180 * angle
	m = ((math.cos(angle), math.sin(angle)), (-math.sin(angle), math.cos(angle)))
	return numpy.dot(m, vec)

def bounds(vec1, vec2):
	return (
		min(vec1[0], vec2[0], -vec1[0], -vec2[0]),
		min(vec1[1], vec2[1], -vec1[1], -vec2[1]),
		max(vec1[0], vec2[0], -vec1[0], -vec2[0]),
		max(vec1[1], vec2[1], -vec1[1], -vec2[1]))

def contains(box, point):
	return point[0] >= box[0] and point[0] <= box[2] and point[1] >= box[1] and point[1] <= box[3]

def hits(box1, box2):

    if box1[0] > box2[2] or box2[0] > box1[2]:
        return False

    if box1[1] > box2[3] or box2[1] > box1[3]:
        return False
 
    return True

def offset(box, origin):
	return (box[0] + origin[0], box[1] + origin[1], box[2] + origin[0], box[3] + origin[1])

def place_crosses(canvas, color, l1, l2, angle, count):
	boxes = []

	for i in range(count):
		vec1 = numpy.array((l1 / 2, 0))
		vec2 = rotate(numpy.array((l2 / 2, 0)), angle)

		rot = random() * 360
		vec1 = rotate(vec1, rot)
		vec2 = rotate(vec2, rot)

		box = bounds(vec1, vec2)

		while True:
			origin = (random() * (W - box[2] + box[0]) - box[0], random() * (H - box[3] + box[1]) - box[1])

			hits_other = False
			for other in boxes:
				if hits(offset(box, origin), other):
					hits_other = True
					break

			if not hits_other:
				boxes.append(offset(box, origin))
				break

		#canvas.color = (0xff, 0, 0, 0xff)
		#canvas.rectangle(*offset(box, origin))

		line1 = tuple(origin - vec1) + tuple(origin + vec1)
		line2 = tuple(origin - vec2) + tuple(origin + vec2)

		canvas.color = color
		rough_line(canvas, *line1)
		rough_line(canvas, *line2)



def generate_image(color, l1, l2, angle, count):
	canvas = PNGCanvas(W, H, color = (0, 0, 0, 0xff))

	canvas.filled_rectangle(0, 0, W - 1, H - 1)

	place_stars(canvas)
	place_crosses(canvas, color, l1, l2, angle, count)

	return canvas.dump()