# the function to judge whether the observer can see the object
#from map import Map
import math
def check_convexity(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    # 计算中间点与两个点的斜率
    slope1 = abs((z2 - z1) /((x2 - x1) ** 2 + (y2 - y1) ** 2)**0.5)
    slope2 = abs((z3 - z1) / (((x3 - x1) ** 2 + (y3 - y1) ** 2) )**0.5)

    # 判断斜率的大小关系
    if (z3-z1)*(z2-z1)<=0:
        if slope2 > slope1:
            return "凸起"
        elif slope2 <=  slope1:
            return "不凸起"
    else:
         if slope2 < slope1:
            return "凸起"
         elif slope2 >=  slope1:
            return "不凸起"

# 从用户输入获取点的坐标和p的值
x1,y1,z1 = 0,0,0
x2,y2,z2 = 1,1,-5
x3,y3,z3 = -1,-1,900
# 判断连线凸起性并输出结果
result = check_convexity(x1, y1, z1, x2, y2, z2, x3, y3, z3)
print("后两个点与中间点的连线" + result)
"""
def view(x1,y1,x2,y2,sight_range):
    z1 = Map.height_map[x1][y1]
    z2 = Map.height_map[x2][y2]
    if (x2-x1)**2 + (y2 - y1)**2 < sight_range**2 :
        return False #not in conditional distance
    else:
        for i in range(abs(x1-x2+1)):
            for j in range(abs(y1-y2+1)):# go over all the positions in the sight range


            """