from graphics import *
import numpy as np
import math as mt
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# calculate coordinates of pyramid in 3d
def calculate_coordinates3d(window_width, window_height):
    # calculate height and base length of pyramid on the base of window size
    height = window_height / 3
    base = window_width / 10

    # calculate coordinates of pyramid
    base1 = [-base, -base, 0, 1]
    base2 = [base, -base, 0, 1]
    base3 = [base, base, 0, 1]
    base4 = [-base, base, 0, 1]

    high = [0, 0, height, 1]

    return np.array([base1, base2, base3, base4, high])


# draw pyramid in 3d with given coordinates and colors of fill and outline
def draw_pyramid3d(pyramid, color_fill, color_outline):
    # get coordinates of pyramid
    Ax, Ay, Az, A1 = pyramid[0]
    Bx, By, Bz, B1 = pyramid[1]
    Cx, Cy, Cz, C1 = pyramid[2]
    Dx, Dy, Dz, D1 = pyramid[3]
    Ex, Ey, Ez, E1 = pyramid[4]

    #draw labels
    # label_A = Text(Point(Ax, Ay), "A")
    # label_B = Text(Point(Bx, By), "B")
    # label_C = Text(Point(Cx, Cy), "C")
    # label_D = Text(Point(Dx, Dy), "D")
    # label_E = Text(Point(Ex, Ey), "E")
    #
    # label_A.setTextColor(color_outline)
    # label_B.setTextColor(color_outline)
    # label_C.setTextColor(color_outline)
    # label_D.setTextColor(color_outline)
    # label_E.setTextColor(color_outline)
    #
    # label_A.draw(window)
    # label_B.draw(window)
    # label_C.draw(window)
    # label_D.draw(window)
    # label_E.draw(window)

    # draw pyramid with fill and outline
    #obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj = SplinePolygon([[Ax, Ay], [Bx, By], [Cx, Cy]])
    obj2 = SplinePolygon([[Ax, Ay], [Dx, Dy], [Cx, Cy]])
    obj.setFill(color_fill)
    obj2.setFill(color_fill)
    obj.setOutline(color_outline)
    obj2.setOutline(color_outline)
    obj.draw(window)
    obj2.draw(window)
    #obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ex, Ey))
    obj = SplinePolygon([[Ax, Ay], [Bx, By], [Ex, Ey]])
    obj.setFill(color_fill)
    obj.setOutline(color_outline)
    obj.draw(window)
    #obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Ex, Ey))
    obj = SplinePolygon([[Bx, By], [Cx, Cy], [Ex, Ey]])
    obj.setFill(color_fill)
    obj.setOutline(color_outline)
    obj.draw(window)
    #obj = Polygon(Point(Cx, Cy), Point(Dx, Dy), Point(Ex, Ey))
    obj = SplinePolygon([[Cx, Cy], [Dx, Dy], [Ex, Ey]])
    obj.setFill(color_fill)
    obj.setOutline(color_outline)
    obj.draw(window)
    #obj = Polygon(Point(Dx, Dy), Point(Ax, Ay), Point(Ex, Ey))
    obj = SplinePolygon([[Dx, Dy], [Ax, Ay], [Ex, Ey]])
    obj.setFill(color_fill)
    obj.setOutline(color_outline)
    obj.draw(window)

    # draw pyramid with outline (for animation)
    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj.setOutline(color_outline)
    obj.draw(window)
    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ex, Ey))
    obj.setOutline(color_outline)
    obj.draw(window)
    obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Ex, Ey))
    obj.setOutline(color_outline)
    obj.draw(window)
    obj = Polygon(Point(Cx, Cy), Point(Dx, Dy), Point(Ex, Ey))
    obj.setOutline(color_outline)
    obj.draw(window)
    obj = Polygon(Point(Dx, Dy), Point(Ax, Ay), Point(Ex, Ey))
    obj.setOutline(color_outline)
    obj.draw(window)

    window.setBackground("white")

    return draw_pyramid3d


# move pyramid in 3d
def move3d(pyramid, move_x, move_y, move_z):
    # create matrix of move
    f = np.array([[1, 0, 0, move_x],
                  [0, 1, 0, move_y],
                  [0, 0, 1, move_z],
                  [1, 0, 0, 1]])
    # transpose matrix
    ft = f.T
    # multiply matrix of move and coordinates of pyramid
    Prxy = pyramid.dot(ft)
    return Prxy

# project pyramid in 3d
def trimetric_prct3d(pyramid, TetaG1, TetaG2, TetaG3):
    # convert degrees to radians
    TetaR1 = (TetaG1 * mt.pi) / 180
    TetaR2 = (TetaG2 * mt.pi) / 180
    TetaR3 = (TetaG3 * mt.pi) / 180

    # create matrices of projection
    f1 = np.array([
        [1, 0, 0, 0],
        [0, mt.cos(TetaR1), -mt.sin(TetaR1), 0],
        [0, mt.sin(TetaR1), mt.cos(TetaR1), 0],
        [0, 0, 0, 1]
    ])

    f2 = np.array([
        [mt.cos(TetaR2), 0, mt.sin(TetaR2), 0],
        [0, 1, 0, 0],
        [-mt.sin(TetaR2), 0, mt.cos(TetaR2), 0],
        [0, 0, 0, 1]
    ])

    f3 = np.array([
        [mt.cos(TetaR3), -mt.sin(TetaR3), 0, 0],
        [mt.sin(TetaR3), mt.cos(TetaR3), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # multiply matrices of projection and coordinates of pyramid
    Prxy1 = np.dot(pyramid, f1.T)
    Prxy2 = np.dot(Prxy1, f2.T)
    Prxy3 = np.dot(Prxy2, f3.T)

    return Prxy3


# rotate pyramid around center
def rotate_around_center3d(pyramid, TetaX, TetaY, TetaZ):
    # calculate center of pyramid
    center_x = np.mean(pyramid[:, 0])
    center_y = np.mean(pyramid[:, 1])
    center_z = np.mean(pyramid[:, 2])

    # move pyramid to center
    pyramid[:, 0] -= center_x
    pyramid[:, 1] -= center_y
    pyramid[:, 2] -= center_z

    # convert degrees to radians
    TetaRX = (TetaX * mt.pi) / 180
    TetaRY = (TetaY * mt.pi) / 180
    TetaRZ = (TetaZ * mt.pi) / 180

    # create matrices of rotation
    f_x = np.array([
        [1, 0, 0, 0],
        [0, mt.cos(TetaRX), -mt.sin(TetaRX), 0],
        [0, mt.sin(TetaRX), mt.cos(TetaRX), 0],
        [0, 0, 0, 1]
    ])

    f_y = np.array([
        [mt.cos(TetaRY), 0, mt.sin(TetaRY), 0],
        [0, 1, 0, 0],
        [-mt.sin(TetaRY), 0, mt.cos(TetaRY), 0],
        [0, 0, 0, 1]
    ])

    f_z = np.array([
        [mt.cos(TetaRZ), -mt.sin(TetaRZ), 0, 0],
        [mt.sin(TetaRZ), mt.cos(TetaRZ), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # multiply matrices of rotation and coordinates of pyramid
    pyramid = pyramid.dot(f_x).dot(f_y).dot(f_z)

    # move pyramid back to original position
    pyramid[:, 0] += center_x
    pyramid[:, 1] += center_y
    pyramid[:, 2] += center_z

    return pyramid


#draw polygon with spline interpolation
def SplinePolygon(control_points):
    # set control points
    control_points = np.asarray(control_points)
    control_points = sorted(control_points, key=lambda point: point[0])
    control_points = np.asarray(control_points)
    # create spline
    spline = interp1d(control_points[:, 0], control_points[:, 1])

    # calculate points of spline
    x  = np.linspace(min(control_points[:, 0]), max(control_points[:, 0]), 30)
    y = spline(x)
    points = np.array([
        [x[i], y[i]] for i in range(len(x))
    ])

    # create polygon
    obj = Polygon([Point(point[0], point[1]) for point in points])

    return obj


# draw pyramid with floating edge algorithm
def floating_edge_algorithm(pyramid, pyramidProect, Xmax, Ymax, Zmax, color_fill, color_outline):
    # get coordinates of orig pyramid
    Ax, Ay, Az, A1 = pyramid[0]
    Bx, By, Bz, B1 = pyramid[1]
    Cx, Cy, Cz, C1 = pyramid[2]
    Dx, Dy, Dz, D1 = pyramid[3]
    Ex, Ey, Ez, E1 = pyramid[4]

    # analyze position
    Flag, FlagAB, FlagBC, FlagCD, FlagDA = 0, 0, 0, 0, 0
    if (abs(Ez-Zmax)<abs(Az-Zmax)):
        Flag = 0
    else:
        Flag = 1

    if (abs(Dy-Ymax)<abs(Ay-Ymax) and abs(Cy-Ymax)<abs(By-Ymax)):
        FlagCD = 1
    elif (abs(Dy-Ymax)>abs(Ay-Ymax) and abs(Cy-Ymax)>abs(By-Ymax)):
        FlagAB = 1
    else:
        FlagCD = 1
        FlagAB = 1

    if (abs(Bx-Xmax)<abs(Ax-Xmax) and abs(Cx-Xmax)<abs(Dx-Xmax)):
        FlagBC = 1
    elif (abs(Bx-Xmax)>abs(Ax-Xmax) and abs(Cx-Xmax)>abs(Dx-Xmax)):
        FlagDA = 1
    else:
        FlagBC = 1
        FlagDA = 1

    # get coordinates of proj pyramid
    Ax, Ay, Az, A1 = pyramidProect[0]
    Bx, By, Bz, B1 = pyramidProect[1]
    Cx, Cy, Cz, C1 = pyramidProect[2]
    Dx, Dy, Dz, D1 = pyramidProect[3]
    Ex, Ey, Ez, E1 = pyramidProect[4]

    #draw pyramid with fill and outline
    #obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj = SplinePolygon([[Ax, Ay], [Bx, By], [Cx, Cy]])
    obj2 = SplinePolygon([[Ax, Ay], [Dx, Dy], [Cx, Cy]])
    if Flag == 1:
        obj.setFill(color_fill)
        obj2.setFill(color_fill)
        obj.setOutline(color_outline)
        obj2.setOutline(color_outline)
        obj.draw(window)
        obj2.draw(window)

    #obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ex, Ey))
    obj = SplinePolygon([[Ax, Ay], [Bx, By], [Ex, Ey]])
    if FlagAB == 1:
        obj.setFill(color_fill)
        obj.setOutline(color_outline)
        obj.draw(window)

    #obj = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Ex, Ey))
    obj = SplinePolygon([[Bx, By], [Cx, Cy], [Ex, Ey]])
    if FlagBC == 1:
        obj.setFill(color_fill)
        obj.setOutline(color_outline)
        obj.draw(window)

    #obj = Polygon(Point(Cx, Cy), Point(Dx, Dy), Point(Ex, Ey))
    obj = SplinePolygon([[Cx, Cy], [Dx, Dy], [Ex, Ey]])
    if FlagCD == 1:
        obj.setFill(color_fill)
        obj.setOutline(color_outline)
        obj.draw(window)

    #obj = Polygon(Point(Dx, Dy), Point(Ax, Ay), Point(Ex, Ey))
    obj = SplinePolygon([[Dx, Dy], [Ax, Ay], [Ex, Ey]])
    if FlagDA == 1:
        obj.setFill(color_fill)
        obj.setOutline(color_outline)
        obj.draw(window)


    #draw labels
    label_A = Text(Point(Ax, Ay), "A")
    label_B = Text(Point(Bx, By), "B")
    label_C = Text(Point(Cx, Cy), "C")
    label_D = Text(Point(Dx, Dy), "D")
    label_E = Text(Point(Ex, Ey), "E")

    label_A.setTextColor("black")
    label_B.setTextColor("black")
    label_C.setTextColor("black")
    label_D.setTextColor("black")
    label_E.setTextColor("black")

    label_A.draw(window)
    label_B.draw(window)
    label_C.draw(window)
    label_D.draw(window)
    label_E.draw(window)

    # draw position of observer
    Xmax_ax, Ymax_ax, Zmax_ax, A1 = trimetric_prct3d(np.array([[Xmax, Ymax, Zmax, 1]]), 75, 35, 0)[0]
    label = Text(Point(Xmax_ax, Ymax_ax), "•")
    label.setTextColor("black")
    label.draw(window)

    window.setBackground("white")

    return floating_edge_algorithm


# build pyramid with matplotlib
def build_pyramid_with_matplotlib(coordinates, x, y, z):
    # check if coordinates are valid
    if len(coordinates) < 5:
        raise ValueError("Not enough points to build a pyramid")

    # get coordinates of the base
    base = coordinates[:4]

    # get coordinates of the apex
    apex = coordinates[4]

    # create triangular faces
    faces = []
    for i in range(4):
        faces.append([i, (i + 1) % 4, 4])

    # create figure and axes
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # plot the base
    ax.plot(base[:, 0], base[:, 1], base[:, 2], 'k')

    # plot the apex
    ax.plot([apex[0]], [apex[1]], [apex[2]], 'r', marker='o')

    ax.plot([x], [y], [z], 'r', marker='o')

    # plot the faces
    for face in faces:
        ax.plot([coordinates[face[0]][0], coordinates[face[1]][0], coordinates[face[2]][0]],
                 [coordinates[face[0]][1], coordinates[face[1]][1], coordinates[face[2]][1]],
                 [coordinates[face[0]][2], coordinates[face[1]][2], coordinates[face[2]][2]], 'k')

    # add markers with labels
    ax.scatter(base[:, 0], base[:, 1], base[:, 2], s=100, c='white', marker='o')
    for i, point in enumerate(base):
        ax.text(point[0], point[1], point[2], f'${chr(ord("A") + i)}$', ha='center', va='center', fontsize=12)

    ax.scatter([apex[0]], [apex[1]], [apex[2]], s=100, c='white', marker='o')
    ax.text(apex[0], apex[1], apex[2], 'E', ha='center', va='center', fontsize=12)

    # add additional labels
    ax.text(base[0][0], base[0][1], base[0][2], 'A', ha='center', va='center', fontsize=12)
    ax.text(base[1][0], base[1][1], base[1][2], 'B', ha='center', va='center', fontsize=12)

    # set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


# window settings
window_width = 500
window_height = 600

# create window
window = GraphWin("Lab 3, I task", window_width, window_height)

# set coordinates of observer
Xsp, Ysp, Zsp = 150, 200, 0
Xsp, Ysp, Zsp = 550, 100, -450

# calculate coordinates of pyramid
coord = calculate_coordinates3d(window_width, window_height)
coord_move = move3d(coord, 200, 300, -300)
coord_moving = coord_move.copy()
flag = True

# enable animation
while flag:
    # rotate pyramid around center
    coord_moving = rotate_around_center3d(coord_moving, 0, 0, 25)
    coord_ax = trimetric_prct3d(coord_moving, 75, 25, 0)

    # draw pyramid
    draw_pyramid3d(coord_ax, "green", "black")
    floating_edge_algorithm(coord_moving, coord_ax, Xsp, Ysp, Zsp, "red", "black")
    time.sleep(0.5)
    window.delete("all")

    # check if mouse clicked, if yes, close window
    if window.checkMouse():
        flag = False
        window.close()
