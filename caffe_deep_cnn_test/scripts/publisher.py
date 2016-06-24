#!/usr/bin/env python
import roslib
roslib.load_manifest('caffe_deep_cnn_test')

from datetime import datetime
import cv2
from cv_bridge import CvBridge, CvBridgeError

import rospy
import rospkg

from sensor_msgs.msg import Image as ImageMsg

import nets

# def talker():
#     pub = rospy.Publisher('chatter', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#
#     while not rospy.is_shutdown():
#
#         hello_str = "hello world %s" % rospy.get_time()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()

class image_converter:
    def __init__(self):
        self.bridge = CvBridge()
        #topic = "/camera/rgb/image_color"
        topic = "/blackened_image"
        self.image_sub = rospy.Subscriber(topic, ImageMsg, self.callback)
        self.not_received = True

        self.rospack = rospkg.RosPack()
        self.prefix = self.rospack.get_path('caffe_deep_cnn_test')

        self.net = nets.caffenet()

        pass

    def callback(self, data):
        if (self.not_received):
            # self.not_received = False
            image = self.read_image_from_msg(data)
            #image = self.read_image_from_file()

            start_time = datetime.now()
            self.net.forward_pass(image)
            end_time = datetime.now()
            delta_time = end_time - start_time
            print "Time consumed: ", delta_time
            self.net.get_words()
            #out = self.net.caffe_net.blobs['score'].data[0].argmax(axis=0)
            #cv2.imshow('input', out)
            #if cv2.waitKey(1) == 27:
                #return
    def read_image_from_msg(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, "bgr8")  # bgr or rgb it is no matter, it will be in bgr in both cases
            return image
        except CvBridgeError as e:
            print e
    def read_image_from_file(self):
        image_path = self.prefix + '/images/mouse.jpg'
        image = cv2.imread(image_path)
        return image
        pass

if __name__ == '__main__':

    ic = image_converter()
    rospy.init_node('listener', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")



