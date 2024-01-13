# the function to judge whether the observer can see the object
from map import Map
import math
def check(x1, y1, z1, x2, y2, z2, x3, y3, z3):#dot 2 is in the middle
    k32 = (z3-z2)/((x3-x2)**2+(y3-y2)**2)**0.5
    k31 = (z3-z1)/((x3-x1)**2+(y3-y1)**2)**0.5
    k12 = (z1-z2)/((x1-x2)**2+(y1-y2)**2)**0.5
    if z3>z1:
        if k32<k31:
            return False
        return True
    elif z3<z1:
        if k12<k31:
            return False
        return True
    else:
        if z2>z1:
            return False
        return True

def is_intersect(x1, y1, x2, y2, x3, y3):#thanks to chatgpt
    # 计算线段的方向向量
    dx = x2 - x1
    dy = y2 - y1

    # 计算正方形的边界
    square_left = x3 - 0.5
    square_right = x3 + 0.5
    square_top = y3 + 0.5
    square_bottom = y3 - 0.5

    # 计算线段与正方形的边界相交的参数t
    t_horizontal_left = (square_left - x1) / dx if dx != 0 else float('inf')
    t_horizontal_right = (square_right - x1) / dx if dx != 0 else float('inf')
    t_vertical_top = (square_top - y1) / dy if dy != 0 else float('inf')
    t_vertical_bottom = (square_bottom - y1) / dy if dy != 0 else float('inf')

    # 确保t在0到1之间，且交点在正方形的边界上
    valid_t_values = [t for t in [t_horizontal_left, t_horizontal_right, t_vertical_top, t_vertical_bottom] if 0 <= t <= 1]

    # 计算交点坐标
    intersection_points = [(x1 + t*dx, y1 + t*dy) for t in valid_t_values]

    # 判断交点是否在正方形的边界上
    for x, y in intersection_points:
        if square_left <= x <= square_right and square_bottom <= y <= square_top:
            return True

    return False

def view(x1,y1,x2,y2,sight_range):
    z1 = Map.height_map[x1][y1]
    z2 = Map.height_map[x2][y2]
    if (x2-x1)**2 + (y2 - y1)**2 < sight_range**2 :
        return False #not in conditional distance
    else:
        for i in range(abs(x1-x2+1)):
            for j in range(abs(y1-y2+1)):# go over all the positions in the sight range
                if is_intersect(x1,y1,x2,y2,i,j):
                    return check(x1,y1,z1,x2,y2,z2,i,j,Map.height_map[i],Map.height_map[j])
