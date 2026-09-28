import rclpy
from rclpy.node import Node
from robcomp_interfaces.msg import PubSubAPS

class Publisher(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.vel_pub = self.create_publisher(PubSubAPS, '/publisher', 10)
        self.timer = self.create_timer(0.25, self.control)
        self.count = 0
    def control(self):
        msg = PubSubAPS()
        self.count+=1 
        msg.counter= self.count
        current_time = self.get_clock().now().to_msg()
        current_time = float(current_time.sec) + float(current_time.nanosec)/10**9
        msg.time = current_time  # m/s
        self.vel_pub.publish(msg)
        print(f"Olá, são {current_time} e estou publicando pela {self.count}ª vez")

def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()