import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Este script define uma estrutura para ações com início, meio e fim.
# A ação inicia quando reset() é chamada e termina quando o estado chega a 'done'.
# Representa uma tarefa específica com começo, execução e fim.
# Exemplos: andar 2m, girar 90 graus, estacionar, abrir uma porta...
# IDEIA CENTRAL: parado → ação iniciada → ação em andamento → ação concluída
# Ex do mundo real - maquina de lavar (executa uma tarefa com começo, meio e fim): ela sabe como lavar, mas não necessariamente decide quando alguém precisa lavar uma roupa. Outra pessoa ou sistema dá a ordem de início.
# Ex robótica - nó girar:
# Aguardando
#    ↓ reset(90°)
# Calcular ângulo desejado
#    ↓
# Girar e observar odometria
#    ↓
# Atingiu o ângulo
#    ↓
# Parar
#    ↓
# done
# A característica principal é: a tarefa possui uma condição clara de conclusão.

class Acao(Node): # Mude o nome da classe
    def __init__(self, node = 'node_name_here'): # Mude o nome do nó
        super().__init__(node)
        self.timer = None
        self.robot_state = 'done' # Estado inicial. Comece em 'done' - reset iniciará a ação
        self.state_machine = { # Adicione quantos estados forem necessários
            'acao': self.acao,
            'stop': self.stop,
            'done': self.done,
        }

        # Inicialização de variáveis
        # ...

        # Publishers
        # Obs.: por padrão, o publisher do cmd_vel já está definido.
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers
        # ...

    # Quando mais de um nó forem utilizar a mesma ação, será necessário mudar o nome do nó para algo mais específico.
    def reset(self): # INICIO DA ACAO
        self.twist = Twist() # inicializa a vari;avel self.twist
        self.robot_state = 'acao' # Inicie a ação
        if self.timer is None:
            self.timer = self.create_timer(0.25, self.control) # inicia o timer, self.timer que chama a funcao control() a. acada 0.25s
        ### Iniciar variaveis necessarias para a ação
        # 1. Tempo inicial

    def acao(self):
        # 1. Definar a velocidade linear do robô na variável twist
        # 2. Recolher o tempo atual
        # 3. Calcular o delta de tempo
        # 4. Se o delta é maior ou igual a t segundos, pare o robô
        pass

    def stop(self): # ao final de uma ação, o estado do robô deve ser alterado para stop
        self.twist = Twist() # Zera a velocidade
        print("Parando o robô.")
        self.timer.cancel() # Finaliza o timer
        self.timer = None # Reseta a variável do timer
        self.robot_state = 'done' # Ação finalizada

    def done(self):
        self.twist = Twist() # Zera a velocidade

    def control(self): # Controla a máquina de estados - é chamado pelo timer a cada 0.25s
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]() # Chama o método do estado atual na maquina de estados
        self.cmd_vel_pub.publish(self.twist) # Publica a velocidade do robo no topico cmd_vel
        # OBS.: a funcao control deve ser a unica que publica no tópico cmd_vel, isso evitara comandos

def main(args=None):
    rclpy.init(args=args) # Inicia o ROS2
    ros_node = Acao() # Cria o nó

    rclpy.spin_once(ros_node) # Processa as callbacks uma vez
    ros_node.reset() # Reseta o nó para iniciar a ação

    while not ros_node.robot_state == 'done': # Enquanto a ação não estiver finalizada
        rclpy.spin_once(ros_node) # Processa os callbacks e o timer

    ros_node.destroy_node() # Destroi o nó
    rclpy.shutdown()    # Finaliza o ROS2

if __name__ == '__main__': # Executa apenas se for o arquivo principal
    main()