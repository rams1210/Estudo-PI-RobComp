import rclpy
from math import pi

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import Twist

from robcomp_util.andar import Andar
from entregavel_3.girar import Girar


class QuadradoNode(Node):
    def __init__(self):
        super().__init__('quadrado_node')

        self.andar_node = Andar()
        self.girar_node = Girar()

        self.robot_state = 'andar'

        self.state_machine = {
            'andar': self.andar,
            'girar': self.girar,
            'done': self.done,
        }

        self.estados_clientes = ['andar', 'girar']

        self.lado = 1.7
        self.angulo =  pi / 2

        self.contador = 0

        self.andar_em_execucao = False
        self.girar_em_execucao = False

        self.twist = Twist()

        self.cmd_vel_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control
        )

    def andar(self):
        if not self.andar_em_execucao:
            print(f'\nIniciando lado {self.contador + 1}/4...')

            self.andar_node.reset(self.lado)
            self.andar_em_execucao = True

        if self.andar_node.robot_state == 'done':
            self.andar_em_execucao = False

            print('[ANDAR] Finalizada.')

            self.robot_state = 'girar'

    def girar(self):
        if not self.girar_em_execucao:
            print(f'\nIniciando giro {self.contador + 1}/4...')

            self.girar_node.reset(self.angulo)
            self.girar_em_execucao = True

        if self.girar_node.robot_state == 'done':
            self.girar_em_execucao = False
            self.contador += 1

            print(
                f'[GIRAR] Finalizada. '
                f'Ciclos completos: {self.contador}/4'
            )

            if self.contador >= 4:
                self.robot_state = 'done'
            else:
                self.robot_state = 'andar'

    def done(self):
        self.twist = Twist()
        self.cmd_vel_pub.publish(self.twist)

    def control(self):
        print(f'Estado atual: {self.robot_state}')

        funcao_estado = self.state_machine[self.robot_state]
        funcao_estado()

        if self.robot_state not in self.estados_clientes:
            self.cmd_vel_pub.publish(self.twist)


def main(args=None):
    rclpy.init(args=args)

    ros_node = QuadradoNode()

    executor = SingleThreadedExecutor()

    executor.add_node(ros_node.andar_node)
    executor.add_node(ros_node.girar_node)
    executor.add_node(ros_node)

    try:
        while rclpy.ok() and ros_node.robot_state != 'done':
            executor.spin_once(timeout_sec=0.1)

        ros_node.done()

    except KeyboardInterrupt:
        print('\nExecução interrompida.')

    finally:
        ros_node.cmd_vel_pub.publish(Twist())

        executor.remove_node(ros_node.andar_node)
        executor.remove_node(ros_node.girar_node)
        executor.remove_node(ros_node)

        ros_node.andar_node.destroy_node()
        ros_node.girar_node.destroy_node()
        ros_node.destroy_node()

        executor.shutdown()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
