# _*_coding:utf-8-*-
import sys
import gym
import math
import numpy as np
from .utility1 import ABC
from .utility2 import get_E
gym.logger.set_level(40)
# import Params
class Env(gym.Env):
    # 初始化参数
    def __init__(self):
        # 状态空间为28维，7*4，暂定输出范围是-20~+20，可以对其缩放
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=(28,))
        # 动作空间为1,输出范围是0~+5，可以对齐缩放
        self.action_space = gym.spaces.Box(low=0, high=5, shape=(28,))
        # self.action_space = gym.spaces.Box(low=-2, high=2, shape=(28,))
        self.done = False
        self.past_reward = 0
        self.abc = ABC()

    # 根据RL输出动作，更新每个线框的x, y, w, h
    def update_state(self, action):
        self.abc.update_points(action)

    # 奖励函数
    def get_reward(self):
        alpha = 0.5
        reward = get_E(self.abc.layout,self.abc.points_now,alpha)
        res = 1 if self.past_reward + alpha < reward else 0
        self.past_reward = reward
        return res

    # 对状态使用np表示，同时缩放大小
    def get_state(self):
        res = np.array(self.abc.points_now).reshape(1,28)
        res = res/1500   #极限长宽w:1800, H:1500，这里除以1500，缩放状态
        return res

    # 主程序
    def step(self, action):
        self.update_state(action)
        reward = self.get_reward()
        return self.get_state(), reward, self.done, {}
    def render(self):
        pass
    # 重置环境
    def reset(self):
        self.done = False
        self.past_reward = 0
        self.abc.reset_ABC()
        # print(self.abc.points_now)
        return self.get_state()
if __name__ == '__main__':
    U = Env()
    # action = [1.3,2.8,2.8,3.7,1.0,0.3,6.2,2.4,
    #           1.3,2.8,2.8,3.7,1.0,0.3,6.2,2.4,
    #           1.3,2.8,2.8,3.7,1.0,0.3,6.2,2.4,
    #           1.3,2.8,2.8]
    action = [0,0,0,0,0,0,0,0,0,0,0,0,0,
              0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    U.reset()
    U.step(action)