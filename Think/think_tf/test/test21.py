# -*- coding: utf-8 -*-
import tensorflow as tf

a = tf.constant(5, name="input_a")
b = tf.constant(3, name="input_b")
# tf.mul 被弃用 需要使用 tf.multiply
c = tf.multiply(a, b, name="mul_c")
d = tf.add(a, b, name="add_d")
e = tf.add(c, d, name="add_e")
# 上面的代码只是建立了一个数据流图，并不会进行计算

# Session 对象在运行时负责对数据流图进行监督，并且是运行数据流图的主要接口 还有一个 InteractiveSession
sess = tf.Session()
result = sess.run(e)

# a = {Tensor} Tensor("input_a:0", shape=(), dtype=int32)
# b = {Tensor} Tensor("input_b:0", shape=(), dtype=int32)
# c = {Tensor} Tensor("mul_c:0", shape=(), dtype=int32)
# d = {Tensor} Tensor("add_d:0", shape=(), dtype=int32)
# e = {Tensor} Tensor("add_e:0", shape=(), dtype=int32)
# result 为 23

# SummaryWriter 改为 tf.summary.FileWriter
# 在 Pycharm 测试的时候发现 run 无法生成数据 可能是 Pycharm 的 bug
writer = tf.summary.FileWriter('./my_graph', graph=sess.graph)

# 关闭以释放资源
writer.close()
sess.close()