#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyRobotSubscriber(Node):
    # allowed joint range (deg); replace with real limits for your robot
    MIN_ANGLE_DEG = -360.0
    MAX_ANGLE_DEG = 360.0

    def __init__(self):
        super().__init__('robot_subscriber')  # node name shown in `ros2 node list`
        self.subscription = self.create_subscription(
            String, 'robot_chatter', self.listener_callback, 10)

    def listener_callback(self, msg):
        # expected format "joint:angle", e.g. "joint_1:45.0"
        if not msg.data:
            self.get_logger().warn('Received an empty message, ignoring')
            return

        try:
            # split "joint:angle" into its two parts; wrong part count -> bad format
            parts = msg.data.split(':')
            if len(parts) != 2:
                raise ValueError(f'expected one colon, got {len(parts) - 1}')

            joint = parts[0].strip()
            if not joint:
                raise ValueError('joint name is empty')

            angle = float(parts[1])  # raises ValueError on non-numeric text

            # reject out-of-range values; chained comparison also rejects nan/inf
            if not (self.MIN_ANGLE_DEG <= angle <= self.MAX_ANGLE_DEG):
                raise ValueError(f'angle {angle} outside '
                                  f'[{self.MIN_ANGLE_DEG}, {self.MAX_ANGLE_DEG}] deg')

            self.get_logger().info(f'Received: {joint} target = {angle} deg')

        except ValueError as e:
            # only ValueError is caught, so real bugs elsewhere aren't hidden by this
            self.get_logger().error(f'Malformed message "{msg.data}": {e}')


def main(args=None):
    rclpy.init(args=args)
    node = MyRobotSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down subscriber (Ctrl+C pressed)')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
