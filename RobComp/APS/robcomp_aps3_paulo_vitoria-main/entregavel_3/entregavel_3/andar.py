import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Andar(Node):

    def __init__(self):
        super().__init__('andar_node')

        self.timer = None
        self.robot_state = 'done'
        self.state_machine = {
            'andar': self.andar,
            'stop': self.stop,
            'done': self.done,
        }

        self.velocidade = 0.2
        self.threshold = 0.0
        self.tempo_inicial = None
        self.dt = 0.0
        self.twist = Twist()

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def reset(self, distancia):
        self.twist = Twist()
        self.threshold = distancia / self.velocidade
        self.tempo_inicial = self.get_clock().now()
        self.robot_state = 'andar'

        if self.timer is None:
            self.timer = self.create_timer(0.1, self.control)

    def andar(self):
        tempo_decorrido = (self.get_clock().now() - self.tempo_inicial).to_msg()
        self.dt = tempo_decorrido.sec + tempo_decorrido.nanosec / 10**9
        print(f'Tempo decorrido: {self.dt:.2f} s')

        if self.dt >= self.threshold:
            self.twist.linear.x = 0.0
            self.robot_state = 'stop'
        else:
            self.twist.linear.x = self.velocidade

    def stop(self):
        self.twist = Twist()
        print('Parando o robo.')

        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

        self.robot_state = 'done'

    def done(self):
        self.twist = Twist()

    def control(self):
        print(f'Estado atual: {self.robot_state}')
        self.state_machine[self.robot_state]()
        self.cmd_vel_pub.publish(self.twist)


def main(args=None):
    rclpy.init(args=args)
    ros_node = Andar()
    ros_node.reset(distancia=1.0)

    try:
        while rclpy.ok() and ros_node.robot_state != 'done':
            rclpy.spin_once(ros_node)
    except KeyboardInterrupt:
        pass
    finally:
        ros_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
