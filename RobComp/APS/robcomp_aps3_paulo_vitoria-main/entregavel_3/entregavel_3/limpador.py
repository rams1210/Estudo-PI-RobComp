import rclpy
import random
import numpy as np
from rclpy.node import Node
from robcomp_util.laser import Laser
from entregavel_3.girar import Girar
from geometry_msgs.msg import Twist, Point
from rclpy.qos import ReliabilityPolicy, QoSProfile
from rclpy.executors import SingleThreadedExecutor
from math import pi



class LimpadorNode(Node, Laser):

    def __init__(self):
        super().__init__('limpador_node')
        Laser.__init__(self)
        self.girar_node = Girar()

        self.girar_em_execucao = False

        self.opening = 25

        self.robot_state = 'procurar'

        self.state_machine = {
            'procurar': self.procurar,
            'esperar': self.esperar,
            'girar': self.girar,
            'limpar': self.limpar,
        }

        self.distancia_minima = 0.5

        self.distancia_maxima = 0.6

        self.v_linear_x = 0.1
        self.v_angular_z = 0.3

        self.alvo_rot = None

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.twist = Twist()

        self.timer = self.create_timer(0.1, self.control)


    def procurar(self):
        self.twist = Twist()
        self.twist.linear.x = self.v_linear_x
        self.twist.angular.z = self.v_angular_z

        if (min(self.front) < self.distancia_minima) or (min(self.right) < self.distancia_minima) or (min(self.left) < self.distancia_minima):
            self.twist = Twist()
            self.robot_state = 'esperar'

    def esperar(self):
        self.twist = Twist()

        dir_livres = []
        if min(self.right) > self.distancia_maxima:
            dir_livres.append((-pi/2)) 

        if min(self.left) > self.distancia_maxima:
            dir_livres.append((+pi/2))

        if min(self.back) > self.distancia_maxima:
            dir_livres.append((pi)) 

        if not dir_livres:
            return

        self.alvo_rot = random.choice(dir_livres)
        self.robot_state = 'girar'

    def girar(self):
        self.twist = Twist()

        if not self.girar_em_execucao:
            print(f'Iniciando giro de {np.degrees(self.alvo_rot):.2f} graus')
            self.girar_node.reset(self.alvo_rot)
            self.girar_em_execucao = True

        if self.girar_node.robot_state == 'done':
            print('Giro finalizado')

            self.girar_em_execucao = False
            self.alvo_rot = None

            if self.girar_node.timer is not None:
                self.girar_node.timer.cancel()
                self.girar_node.timer = None

            self.robot_state = 'limpar'

    def limpar(self):
        self.twist = Twist()
        self.twist.linear.x = self.v_linear_x

        if min(self.front) < self.distancia_minima:
            self.twist = Twist()
            self.robot_state = 'esperar'

    def control(self):
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()

        if self.robot_state != 'girar':
            self.cmd_vel_pub.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    ros_node = LimpadorNode()

    executor = SingleThreadedExecutor()
    executor.add_node(ros_node)
    executor.add_node(ros_node.girar_node)

    try:
        while rclpy.ok():
            executor.spin_once(timeout_sec=0.1)

    except KeyboardInterrupt:
        pass

    finally:
        ros_node.cmd_vel_pub.publish(Twist())

        executor.remove_node(ros_node.girar_node)
        executor.remove_node(ros_node)

        ros_node.girar_node.destroy_node()
        ros_node.destroy_node()

        executor.shutdown()

        if rclpy.ok():
            rclpy.shutdown()


    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 
