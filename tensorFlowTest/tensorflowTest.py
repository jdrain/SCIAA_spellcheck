#test file for ML  and tensorflow
#taken from youtube.com/Sirajology
#video title: "TensorFlow in 5 Minutes"

import input_data
import tensorflow as tf

mnist=input_data.read_data_sets("/tmp/data/", one_hot=True)

#set params
learning_rate = .01
training_iteration  = 30
batch_size = 100
display_step = 2

#TF graph input
x = tf.placeholder("float", [None, 784]) #mnist data image of size 28*28
y = tf.placeholder("float", [None, 10]) # 0-9 digits recognition => 10 classes

#Create model
#Set model weights
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

with tf.name_scope("Wx_b") as scope:
    #Construct a linear model
    model = tf.nn.softmax(tf.matmul(x, W) + b) #softmax

#Add summary ops to collect data
w_h = tf.histogram_summary("weights", W)
b_h = tf.histogram)summary("biases", b)

#More name scopes will clean up graph representation
with tf.name_scope("cost_function") as scope:
    #Minimize error using cross entropy
    #Cross entropy
    cost_function = -tf.reduce_sum(y=tf.log(model))
    #Create a summary to monitor the cost function
    tf.scalar_summary("cost_function", cost_function)

with tf.name_scope("train") as scope:
    #Gradient descent
    optimizer=tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

#Initializing the variables
init=tf.initialize_all_variables()

#Merge all summaries into a single operator
merged_summary_op=tf.merge_all_summaries()

#Launch the graph
with tf.Session() as sess:
    sess.run(init)

    #Set the logs writer to the folder /tmp/tensorflow_logs
    summary_writer=tf.train.SummaryWriter('/home/jdrain/logs/', graph_def=sess.graph_def)

    #Training cycle
    for iteration in range(training_iteration):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples/batch_size)
        #Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            #Fit training using batch data
            sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys})
            #Compute the average loss
