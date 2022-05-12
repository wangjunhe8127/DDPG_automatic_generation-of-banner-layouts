import numpy as np


class ABC():
    def __init__(self):
        self.points_limit = []
        self.points_now = []
        self.layout = [0, 0, 0, 0]
    # 根据RL输出动作，更新线框x, y, w, h
    def update_points(self, action):
        for i in range(7):
            # 动作按顺序分别表示上、下、左、右。对应a[0],a[1],a[2],a[3]。基于此，在env.py中定义动作各个值都大于0，取值为[0,5]
            a = action[0][i*4:(i+1)*4]
            # 如果想要整数移动就打开下面一行代码的注释
            # a = [int(a[k]) for k in range(4)]
            # print(a)
            a_right = a[3]-a[2]
            a_down = a[1]-a[0]
            self.points_now[i][0] = min(self.points_now[i][0]+a_right,self.points_limit[i][1]) \
                if self.points_now[i][0]+a_right > self.points_limit[i][0] else self.points_limit[i][0]
            self.points_now[i][1] = min(self.points_now[i][1]+a_down,self.points_limit[i][3]) \
                if self.points_now[i][1]+a_down > self.points_limit[i][2] else self.points_limit[i][2]

    # 随机化每个线框的位置
    def init_points(self):
        for i in range(7):
            [xl, xr,yu,yd] = self.points_limit[i]
            x_center = np.random.uniform(low=xl, high=xr)
            y_center = np.random.uniform(low=yu, high=yd)
            w = self.points_wh(i)[2]
            h = self.points_wh(i)[3]
            self.points_now.append([x_center, y_center, w, h])
        return self.points_now

    # 计算当前布局下，某线框中心的边界,并保存为成员变量
    def compute_points_limit(self):
        res = []
        for i in range(7):
            x_half_distance = self.points_wh(i)[2] / 2
            y_half_distance = self.points_wh(i)[3] / 2
            x_left_limit = self.layout[0]+x_half_distance
            x_right_limit = self.layout[0]+self.layout[2]-x_half_distance
            y_up_limit = self.layout[1]+y_half_distance
            y_down_limit = self.layout[1]+self.layout[3]-y_half_distance
            res.append([x_left_limit, x_right_limit, y_up_limit, y_down_limit])
        self.points_limit = res

    # 线框长和宽
    def points_wh(self,num):
        res = {
            0: [100, 100, 100, 50],
            1: [50, 200, 200, 150],
            2: [200, 600, 400, 200],
            3: [240, 300, 100, 300],
            4: [700, 20, 50, 600],
            5: [400, 600, 150, 400],
            6: [20, 800, 700, 300],
        }
        return res.get(num, None)

    # 如果每次reset需要更改布局，只需要修改这个函数就可以
    def init_layout(self):
        self.layout = [0, 0, 800, 1200]
    # 每次gym中reset时，reset布局和线框
    def reset_ABC(self):
        self.init_layout()
        self.compute_points_limit()
        self.points_now = []
        self.init_points()

    # 测试时直接使用固定的位置测试,这个函数暂时没用到，后面你可以自己加
    def fixed_points(self):
        res = []
        for i in range(7):
            tmp = self.points_wh(i)
            res.append(tmp)
        return res
