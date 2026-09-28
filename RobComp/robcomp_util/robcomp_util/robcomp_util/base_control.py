import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist, Point
# Importar a classe da acao do arquivo, como por exemplo
from robcomp_util.base_action import Acao
# Adicione aqui os imports necessários


# NO "CLIENTE" DA ACAO: este script é um GERENCIADOR que pode ou não chamar a ação definida no nó de ação. Normalmente, ele é o NÓ PRINCIPAL do pacote que decide quando iniciar/parar uma ação (é o gerente ou coordenador).
# Ele não precisa saber todos os detalhes de como uma ação é realizada. Ele decide:
# - qual ação deve começar;
# - quando ela deve começar;
# - quais parâmetros serão usados;
# - quando deve esperar;
# - o que acontece depois que a ação terminar.
# FLUXO SIMPLES: Inicie → aguarde → verifique o término → escolha a próxima tarefa
# O cliente sabe QUAL É A SEQUENCIA. Cada ação sabe COMO EXECUTAR sua própria tarefa.

class BaseControlNode(Node): # Mude o nome da classe
    def __init__(self):
        super().__init__('node_name_here') # Mude o nome do nó
        # Outra Herança que você queira fazer
        self.acao_node = Acao() # Cria o nó da Acao

        self.robot_state = 'acao'
        self.state_machine = {
            'acao': self.acao, # Estado para GERENCIAR a ação
            'done': self.done
        }

        self.estados_clientes = ['acao'] # Coloque aqui os estados que são "cliente de ação".

        # Inicialização de variáveis
        self.twist = Twist()

        # Subscribers
        ## Coloque aqui os subscribers

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        ## Coloque aqui os publishers

        ## Por fim, inicialize o timer
        self.timer = self.create_timer(0.1, self.control)


    def acao(self): # função que aciona a ação
        if self.acao_node.robot_state == 'done': # Se a ação NÂO FOI INICIADA
            print("\nIniciando [ACAO]...")
            rclpy.spin_once(self.acao_node, timeout_sec=0.5) # Processa as callbacks uma vez
            self.acao_node.reset() # Reseta o nó para iniciar a ação
        rclpy.spin_once(self.acao_node, timeout_sec=0.5) # Processa os callbacks e o timer
        if self.acao_node.robot_state == 'done': # Se a ação FOI FINALIZADA
            self.acao_node.control() # Garante que o robo é parado antes de finalizar a ação
            print("[ACAO] Finalizada.")
            self.robot_state = 'done' # Muda para o próximo estado da máquina de estados, nesse caso, 'done'.
        # a ação só será iniciada uma vez e só passará para o próximo estado quando a ação for finalizada internamente, ou seja, quando o nó de ação mudar seu estado para 'done'. Assim, o controle da ação é delegado para o nó de ação, enquanto o nó "cliente" apenas gerencia quando iniciar/parar a ação.


    def done(self):
        self.twist = Twist()

    def control(self): # Controla a máquina de estados - é chamado pelo timer
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]() # Chama o método do estado atual
        if self.robot_state not in self.estados_clientes: # Se o estado atual não é um estado "cliente de ação"
            self.cmd_vel_pub.publish(self.twist) # Publica a velocidade
        # Aqui, o nó "cliente" só publicará no cmd_vel se o estado atual não for um estado cliente de ação. Isso é importante para evitar conflitos de publicação entre o nó "cliente" e o nó de ação, garantindo que o nó de ação tenha controle total sobre o cmd_vel durante a execução da ação.

def main(args=None):
    rclpy.init(args=args) # Inicia o ROS2
    ros_node = BaseControlNode() # Cria o nó

    while not ros_node.robot_state == 'done': # Enquanto o robô não estiver parado
        rclpy.spin_once(ros_node) # Processa os callbacks e o timer

    ros_node.destroy_node() # Destroi o nó
    rclpy.shutdown() # Encerra o ROS2

if __name__ == '__main__':
    main()