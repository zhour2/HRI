import tensorflow as tf
print(tf.__version__)

with tf.compat.v1.Session() as sess:
    c = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    d = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    e = tf.matmul(c, d)

    result = sess.run(e)

    print(result)