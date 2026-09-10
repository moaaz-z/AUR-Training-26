import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleController(Node):

    def __init__(self):
        super().__init__('task1_controller')

        self.declare_parameter('target_x', 8.0)
        self.declare_parameter('target_y', 8.0)
        self.declare_parameter('linear_gain', 1.0)
        self.declare_parameter('angular_gain', 4.0)
        self.declare_parameter('distance_tolerance', 0.1)
        self.declare_parameter('angle_tolerance', 0.05)
        self.declare_parameter('loop_rate_hz', 10.0)

        self.target_x = self.get_parameter('target_x').value
        self.target_y = self.get_parameter('target_y').value
        self.linear_gain = self.get_parameter('linear_gain').value
        self.angular_gain = self.get_parameter('angular_gain').value
        self.distance_tolerance = self.get_parameter('distance_tolerance').value
        self.angle_tolerance = self.get_parameter('angle_tolerance').value
        self.loop_rate_hz = self.get_parameter('loop_rate_hz').value

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.timer = self.create_timer(
            1.0 / self.loop_rate_hz,
            self.control_loop
        )

    def pose_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    def control_loop(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        target_angle = math.atan2(dy, dx)

        angle_error = target_angle - self.theta

        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        msg = Twist()

        if distance <= self.distance_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_pub.publish(msg)
            return

        msg.angular.z = self.angular_gain * angle_error

        if abs(angle_error) > self.angle_tolerance:
            msg.linear.x = 0.0
        else:
            msg.linear.x = self.linear_gain * distance

        self.cmd_vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
