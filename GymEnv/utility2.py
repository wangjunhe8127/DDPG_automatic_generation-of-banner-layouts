import math
a1 = 0.25
a2 = 0.25
a3 = 0.25
a4 = 0.25

def get_E(layout, points, a):
    global alpha
    alpha = a
    tmp = get_E34(layout, points)
    res = a1*get_E1(points)+a2*get_E2(layout, points)+a3*tmp[0]+a4*tmp[1]
    return res

def get_E1(points):
    E_max = -float('inf')
    tmp = [0, 0, 0, 0, 0, 0]
    for i in range(7):
        for j in range(7):
            if i != j:
                tmp[0] += if_left(points[i], points[j])
                tmp[1] += if_right(points[i], points[j])
                tmp[2] += if_up(points[i], points[j])
                tmp[3] += if_down(points[i], points[j])
                tmp[4] += if_center_x(points[i], points[j])
                tmp[5] += if_center_y(points[i], points[j])
    for i in range(6):
        e = tmp[i]/(7*7) #对应公式，这里n是线框数量
        E = com_E(e, alpha)
        E_max = E if E > E_max else E_max
    return E_max

def get_E2(layout, points):
    res = 0
    for i in range(7):
        for j in range(7):
            if i != j:
                res += overlap(points[i], points[j])
                # print(overlap(points[i], points[j]))#测试重叠区域是否正确
    res = res/(layout[2]*layout[3])
    e = 1-res
    E = com_E(e, alpha)
    return E

def get_E34(layout, points):
    l_position = [layout[0], layout[1], layout[2]/3, layout[3]]
    r_position = [layout[0]+layout[2]*2/3, layout[1], layout[2]/3, layout[3]]
    t_position = [layout[0], layout[1], layout[2], layout[3]/3]
    b_position = [layout[0], layout[1]+layout[3]*2/3, layout[2], layout[3]/3]
    Al = com_A(l_position, points)
    Ar = com_A(r_position, points)
    At = com_A(t_position, points)
    Ab = com_A(b_position, points)
    elr = min(Al, Ar)/max(Al, Ar)
    etb = min(At, Ab)/max(At, Ab)
    return com_E(elr,alpha), com_E(etb,alpha)
#由e计算E
def com_E(e,alpha):
    res = math.atan(e*alpha)/math.atan(alpha)
    return res
#计算线框和布局1/3重叠区域
def com_A(position, points):
    res = 0
    for i in range(7):
        res += overlap(position, points[i])
    return res
#计算重叠区域子函数
def overlap(point1, point2):
    left = point1 if min(point1[0],point2[0])==point1[0] else point2 #两个线框中左边的线框
    right = point1 if left == point2 else point2 #两个线框中右边的线框
    up = point1 if min(point1[1],point2[1])==point1[1] else point2 #两个线框中上边的线框
    down = point1 if up == point2 else point2 #两个线框中下边的线框
    if left[0]+left[2]<right[0] or up[1]+up[3]<down[1]: #如果没有交集，就返回0
        return 0
    else:
        weight = min(point1[0]+point1[2],point2[0]+point2[2]) - max(point1[0],point2[0]) #x轴重叠部分长度
        high = min(point1[1]+point1[3],point2[1]+point2[3]) - max(point1[1],point2[1])#y轴重叠部分长度
        res = weight*high
        return res
# 以下是判断是否对齐函数
def if_left(point1,point2):
    res = 1 if point1[0] == point2[0] else 0
    return res
def if_right(point1,point2):
    res = 1 if point1[0]+point1[2] == point2[0]+point2[2] else 0
    return res
def if_up(point1,point2):
    res = 1 if point1[1] == point2[1] else 0
    return res
def if_down(point1,point2):
    res = 1 if point1[1]+point1[3] == point2[1]+point2[3] else 0
    return res
def if_center_x(point1,point2):
    res = 1 if point1[0]+point1[2]/2 == point2[0]+point2[2]/2 else 0
    return res
def if_center_y(point1,point2):
    res = 1 if point1[1]+point1[3]/2 == point2[1]+point2[3]/2 else 0
    return res
