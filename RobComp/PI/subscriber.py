import rclpy
from rclpy.node import Node
from robcomp_interfaces.msg import PubSubAPS
from rclpy.qos import ReliabilityPolicy, QoSProfile


class Subscriber(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.current_delay = 0.0
        

        self.sub = self.create_subscription(
        PubSubAPS,
           '/publisher',
            self.odom_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        )

        self.timer = self.create_timer(0.25, self.control)
        self.current_msg = None

    def odom_callback(self, msg: PubSubAPS):
        current_time = self.get_clock().now().to_msg()
        current_time = float(current_time.sec) + float(current_time.nanosec)/10**9
        pub_time = float(msg.time)
        self.current_msg = msg.counter
        self.current_delay = current_time - pub_time
    def control(self):
        if not self.current_msg:
            return
        print(f'mensagem:{self.current_msg} que demorou {self.current_delay:.9f}segundos para ser recebida')
    


def main(args=None):
    rclpy.init(args=args)
    node = Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()