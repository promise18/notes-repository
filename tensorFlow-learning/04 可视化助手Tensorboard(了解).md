使用Tensorboard，我们首先要定义变量的命名空间name_scope，只有定义了name_scope，我们在tensorboard中的Graph才会看起来井然有序。

```python
import tensorflow as tf
import numpy as np

tf.set_random_seed(1)
np.random.seed(1)

# fake data
x = np.linspace(-1, 1, 100)[:, np.newaxis]          # shape (100, 1)
noise = np.random.normal(0, 0.1, size=x.shape)
y = np.power(x, 2) + noise    # np.power:对数组元素进行平方运算  # shape (100, 1) + some noise

with tf.variable_scope('Inputs'):   # 定义输入变量的命名空间
    tf_x = tf.placeholder(tf.float32, x.shape, name='x_in') # input x
    tf_y = tf.placeholder(tf.float32, y.shape, name='y_in') # input y

with tf.variable_scope('layer'): # 定义隐藏层和输出层的命名空间
    l1 = tf.layers.dense(tf_x, 10, tf.nn.relu, name='hidden_layer') # hidden layer
    output = tf.layers.dense(l1, 1, name='output_layer') # output layer

    # histogram：显示直方图信息，用来显示训练过程中这两个变量在每一期的分布变化，
    tf.summary.histogram('hidden_out', l1)
    tf.summary.histogram('pred', output)

loss = tf.losses.mean_squared_error(tf_y, output, scope='loss') # 定义损失函数的命名空间
train_op = tf.train.GradientDescentOptimizer(learning_rate=0.5).minimize(loss)
tf.summary.scalar('loss', loss) # add loss to scalar summary：loss是一个单个的数，也就是标量scalaer

sess = tf.Session()
sess.run(tf.global_variables_initializer())

writer = tf.summary.FileWriter('./log', sess.graph)     # write to file
merge_op = tf.summary.merge_all()                       # operation to merge all summary

for step in range(100):
    # train and net output
    _, result = sess.run([train_op, merge_op], {tf_x: x, tf_y: y})
    writer.add_summary(result, step)

```

