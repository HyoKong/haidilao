# **About the Competition**

## src folder
* the code of the competition

## huawei2019-with-visualization
* the simulator of the judgement of this competition

# Workflow:

1.提高代码效率，提升运行速度：
 
 原版代码的运行效率略低，导致跑map1时非常容易程序运行超时。比如utils.py中读取文件的方法是先将整个txt放入一个list里，然后再存入dataframe中，如果调成读一行存一行会不会好一些；
或者比如CodeCraft-2019.py中，第63-77行（找节点路径并转为道路id路径）是先找到所有路径，然后再统一写入文件，边找边写也可能是个提升效率的方法。

因为今晚10点以后就不能再提交代码查看成绩了，且初赛的数据集量级要比训练赛数据集量级大非常多，为了防止运行时间超时，要提高代码运行效率。

从本地跑代码的情况来看，读三个txt文档的时间很长。

2.统计每条道路上车辆数量：

在每个时间片发若干辆车之后，统计每条道路上车辆数量，以便更新邻近矩阵权值，且道路上车辆数目也可与下一个时间片出发车辆数目成反比关系。

Pseudo Code：

```
initial：
按照计划发车时间/最大运行速度对car_df进行重排；
初始发车数量：num=10

while not 所有车到达目的地：
    for 每个时间片T：
        读取已发车的所有车辆位置信息，确定位置，更新道路车辆数目  
        根据每条道路上车辆数量，更新邻近矩阵权重，修改T+1时刻邻近矩阵权重和下一时刻发车数量
        计算T+1时间片内，num辆车的最短路径
```
