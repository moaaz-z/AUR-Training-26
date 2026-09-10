import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class Task2Client(Node):

    def __init__(self):
        super().__init__('task2_client')

        self.client = self.create_client(
            SetBool,
            'toggle_movement'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.timer = self.create_timer(
            3.0,
            self.send_request
        )

        self.request_sent = False

    def send_request(self):

        if self.request_sent:
            return

        request = SetBool.Request()
        request.data = True

        self.future = self.client.call_async(request)
        self.future.add_done_callback(self.response_callback)

        self.request_sent = True
        self.timer.cancel()

    def response_callback(self, future):

        try:
            response = future.result()

            self.get_logger().info(
                f'Success: {response.success}'
            )

            self.get_logger().info(
                f'Message: {response.message}'
            )

        except Exception as e:
            self.get_logger().error(
                f'Service call failed: {e}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = Task2Client()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
