#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyRobotPublisher(Node):
    def __init__(self):
        super().__init__('robot_publisher')  # node name shown in `ros2 node list`

        self.publisher_ = self.create_publisher(String, 'robot_chatter', 10)

        # joint angles (deg) to cycle through; simulated, no real robot connected
        self.angles = [0.0, 45.0, 90.0, 135.0]
        self.i = 0  # index of the next angle to send

        # calls timer_callback every 0.5s; kept as self.timer so it can be cancelled later
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = String()
        # format "joint:angle", e.g. "joint_1:45.0" — subscriber splits on the colon
        msg.data = f'joint_1:{self.angles[self.i]}'
        self.i = (self.i + 1) % len(self.angles)  # loop back to 0 after the last angle

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = MyRobotPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down publisher (Ctrl+C pressed)')
    finally:
        node.destroy_node()
        # avoid "rcl_shutdown already called": some ROS 2 versions shut down on Ctrl+C already
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
