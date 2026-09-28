import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
# Adicion

# NÓ BASE: é útil para módulos que ASSINAM um tópico, processam os dados e publicam o resultado em outro tópico (ex: um nó de visão computacional).

class BaseNode(Node): # Mude o nome da classe
    def __init__(self):
        super().__init__('node_name_here') # Mude o nome do nó
        # Outra Herança que você queira fazer
        # Inicialização de variáveis

        # Subscribers
        ## Coloque aqui os subscribers

        # Publishers
        ## Coloque aqui os publishers

        # Por fim, inicialize o timer
        self.timer = self.create_timer(0.25, self.control)

    def control(self):
        print('running...')


def main(args=None):
    rclpy.init(args=args)
    ros_node = BaseNode() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()