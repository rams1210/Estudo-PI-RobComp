import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from robcomp_util.laser import Laser # importa a classe Laser do arquivo laser.py


class TestLaser(Node, Laser): # heranca multipla: a primeira-classe pai indicada é Node
    def __init__(self):
        super().__init__('test_laser_node') # inicializa a parte de Node (primeira classe-pai) presente no objeto, super() permite acessar a prox classe da hierarquia
        Laser.__init__(self) # chama diretamente o inicializador da outra classe-pai: Laser
        self.opening = 10

        # Por fim, inicialize o timer
        self.timer = self.create_timer(1, self.control)

    def control(self):
        print("self.front: ", self.front)
        print("Tem coisa perto? ", min(self.front) < 1.0)


def main(args=None):
    rclpy.init(args=args)
    ros_node = TestLaser() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# CODIGO ADAPTADO DO base.py
# COMPILAR E ATUALIZAR NO TERMINAL (cb) após:
#   1) Alterar laser.py (reutilizável)
#   2) Alterar test_laser.py (nó "completo)
#   3) Alterar setup.py (incluindo test_laser.py)
#   4) Salvar arquivos modificados
# RODAR APENAS DEPOIS DE COMPILAR E ATUALIZAR TERMINAL
#   ros2 run robcomp_util test_laser