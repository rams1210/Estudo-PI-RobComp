import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from robcomp_util.odom import Odom # importa a classe Odom do arquivo odom.py


class TestOdomNode(Node, Odom): # heranca multipla: a primeira-classe pai indicada é Node
    # classe Odom: fornece a inscrição no tópico /odom e os atributos x, y e yaw.
    def __init__(self):
        super().__init__('node_name_here') # inicializa a parte de Node (primeira classe-pai) presente no objeto, super() permite acessar a prox classe da hierarquia
        Odom.__init__(self) # chama diretamente o inicializador da outra classe-pai: Odom
        self.timer = self.create_timer(0.25, self.control) # Por fim, inicialize o timer

    def control(self):
        print("\n")
        print("self.x: ", self.x)
        print("self.y: ", self.y)
        print("self.yaw: ", self.yaw)

def main(args=None):
    rclpy.init(args=args)
    ros_node = TestOdomNode() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# CODIGO ADAPTADO DO base.py
# COMPILAR E ATUALIZAR NO TERMINAL (cb) após:
#   1) Alterar odom.py (reutilizável)
#   2) Alterar test_odom.py (nó "completo)
#   3) Alterar setup.py (incluindo test_odom.py)
#   4) Salvar arquivos modificados
# RODAR APENAS DEPOIS DE COMPILAR E ATUALIZAR TERMINAL
#   ros2 run robcomp_util test_odom