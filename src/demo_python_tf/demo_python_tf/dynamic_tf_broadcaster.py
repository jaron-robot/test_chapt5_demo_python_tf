import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster  #坐标发布器
from geometry_msgs.msg import TransformStamped  #消息接口
from tf_transformations import quaternion_from_euler  #欧拉角转四元数函数
import math  #角度转弧度函数

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.broadcaster_ = TransformBroadcaster(self)
        #self.publish_static_tf()
        self.timer_ = self.create_timer(0.01,self.publish_tf) 

    def publish_tf(self):
        """
        发布静态TF 从camera_link到bottle_link之间的关系
        """
        transform = TransformStamped()
        transform.header.frame_id = 'camera_link'
        transform.child_frame_id = 'bottle_link'
        transform.header.stamp = self.get_clock().now().to_msg()

        #  x,y,z
        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5

        #角度  先将角度转弧度，然后再将而欧拉角转换为四元数
        q = quaternion_from_euler(0,0,0)  #欧拉角转四元数x,y,z,w
        #旋转部分赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]

        #发布静态坐标关系
        self.broadcaster_.sendTransform(transform)
        self.get_logger().info(f'发布TF{transform}')

def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

