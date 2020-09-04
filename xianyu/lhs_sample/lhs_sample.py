#coding=utf-8
#author:
#date:2020/09/04

from __future__ import division
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter
import matplotlib.pyplot as plt

def LHSample( D,bounds,N):
    '''
    :param D:维度
    :param bounds:采样范围
    :param N:采样数
    :return:样本数据
    '''
    result = np.empty([N, D])
    temp = np.empty([N])
    d = 1.0 / N
    for i in range(D):
        for j in range(N):
            temp[j] = np.random.uniform(
                low=j * d, high=(j + 1) * d, size = 1)[0]
        np.random.shuffle(temp)
        for j in range(N):
            result[j, i] = temp[j]
    #对样本数据进行拉伸
    b = np.array(bounds)
    lower_bounds = b[:,0]
    upper_bounds = b[:,1]
    if np.any(lower_bounds > upper_bounds):
        print('out of boundary')
        return None
    #   sample * (upper_bound - lower_bound) + lower_bound
    np.add(np.multiply(result,
                       (upper_bounds - lower_bounds),
                       out=result),
           lower_bounds,
           out=result)
    return result


if __name__ =='__main__':
    D = input("Please choose sample dimension: ")
    while D != '2' and D != '3':
        print("Dimension should be 2 or 3!")
        D = input("Please choose sample dimension: ")
    D = int(D)

    # gen figure
    fig = plt.figure()
    if (D == 3):
        ax1 = fig.add_subplot(221, projection='3d')
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)    
    else:
        ax1 = fig.add_subplot(111)
 
    # gen data
    N = 100
    XYZ_limit = 90
    bounds = [[0,XYZ_limit] for i in range(D)]
    samples = LHSample(D, bounds,N)
    for sample in samples:
        if(D == 3):
            ax1.scatter(sample[0], sample[1], sample[2], c='blue', marker='o')
            ax2.scatter(sample[1], sample[2], c='blue', marker = 'o')
            ax3.scatter(sample[0], sample[2], c='blue', marker = 'o')
            ax4.scatter(sample[0], sample[1], c='blue', marker = 'o')
        else:
            ax1.scatter(sample[0], sample[1], c='blue', marker = 'o')
    
    if(D == 3):
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax1.set_zlabel('Z axis')
    
        ax2.set_xlabel('Y axis')
        ax2.set_ylabel('Z axis')
    
        ax3.set_xlabel('X axis')
        ax3.set_ylabel('Z axis')
    
        ax4.set_xlabel('X axis')
        ax4.set_ylabel('Y axis')
    else:
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')

    # show figure
    plt.show()
    