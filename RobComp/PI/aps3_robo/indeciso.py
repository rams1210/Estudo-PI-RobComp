import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist, Point
# Importar a classe da andar do arquivo, como por exemplo
from robcomp_util.laser import Laser



class Indeciso(Node, Laser): # Mude o nome da classe

    def __init__(self):
        super().__init__('indeciso_node') # Mude o nome do nó
        Laser.__init__(self)
        # Outra Herança que você queira fazer
        #rclpy.spin_once(self) # Roda pelo menos uma vez para pegar os valores

        self.robot_state = 'forward'
        self.state_machine = {
            'forward': self.forward, # Estado para GERENCIAR a ação
            'stop': self.stop,
            'backward': self.backward,
        }

        # Inicialização de variáveis
        self.twist = Twist()
    
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        

        ## Por fim, inicialize o timer
        self.timer = self.create_timer(0.1, self.control)
    
    def backward(self):
        self.twist.linear.x = -0.3
        min_front = min(self.front)
        if min_front > 1.05:
            self.robot_state = 'forward'
        elif min_front > 0.95:
            self.robot_state ='stop'
            

    def forward(self):
        self.twist.linear.x = 0.3
        min_front = min(self.front)
        if min_front < 0.95:
            self.robot_state = 'backward'
        elif min_front < 1.05:
            self.robot_state ='stop'

            
    def stop(self):
        self.twist = Twist()
        self.robot_state = 'backward'


    
    def control(self): # Controla a máquina de estados - eh chamado pelo timer
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]() # Chama o método do estado atual 
        self.cmd_vel_pub.publish(self.twist) # Publica a velocidade
 
def main(args=None):
    rclpy.init(args=args) # Inicia o ROS2
    ros_node = Indeciso() # Cria o nó

    while not ros_node.robot_state == 'done': # Enquanto o robô não estiver parado
        rclpy.spin_once(ros_node) # Processa os callbacks e o timer

    ros_node.destroy_node() # Destroi o nó
    rclpy.shutdown() # Encerra o ROS2
    
if __name__ == '__main__':
    main()
    
    
    
    
    