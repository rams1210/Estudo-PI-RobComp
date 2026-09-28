import rclpy
import numpy as np
from math import degrees, pi, radians
from rclpy.node import Node
from geometry_msgs.msg import Twist
from robcomp_util.odom import Odom


class Girar(Node, Odom):

    def __init__(self):
        super().__init__('girar_node')
        Odom.__init__(self)

        self.timer = None
        self.robot_state = 'done'
        self.state_machine = {
            'girar': self.girar,
            'stop': self.stop,
            'done': self.done,
        }

        self.twist = Twist()
        self.goal_yaw = self.yaw
        self.tolerancia = radians(2.0)
        self.velocidade_angular = 0.2

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def reset(self, rotacao):
        self.twist = Twist()
        self.goal_yaw = self.ajuste_angulo(self.yaw + rotacao)
        self.robot_state = 'girar'

        if self.timer is None:
            self.timer = self.create_timer(0.1, self.control)

    def ajuste_angulo(self, angulo):
        return np.arctan2(np.sin(angulo), np.cos(angulo))

    def girar(self):
        erro = self.ajuste_angulo(self.goal_yaw - self.yaw)
        print(f'Erro: {degrees(erro):.2f} graus')

        if abs(erro) <= self.tolerancia:
            self.twist = Twist()
            self.robot_state = 'stop'
            return

        self.twist.linear.x = 0.0
        if erro < 0.0:
            self.twist.angular.z = -self.velocidade_angular
        else:
            self.twist.angular.z = self.velocidade_angular

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
    ros_node = Girar()

    rclpy.spin_once(ros_node, timeout_sec=1.0)
    ros_node.reset(pi / 2)

    while rclpy.ok() and ros_node.robot_state != 'done':
        rclpy.spin_once(ros_node)

    ros_node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
