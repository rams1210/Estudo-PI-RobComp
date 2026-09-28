# IMPORTAÇÃO DE BIBLIOTECAS:
#---------------------------------------------------
# Importa a biblioteca principal do ROS2 para Python
import rclpy
# Importa o módulo 'random' para seleção aleatória de direções
import random
# Importa o 'numpy' para manipulações numéricas, como o uso de pi
import numpy as np
# Importa a classe base para criar um nó ROS2
from rclpy.node import Node
# Importa as classes customizadas para lidar com dados do laser e controle de giro
from robcomp_util.laser import Laser
from entregavel_3.girar import Girar
# Importa as mensagens ROS2 para controle de velocidade (Twist) e pontos (Point)
from geometry_msgs.msg import Twist, Point
# Importa os perfis de qualidade de serviço (QoS)
from rclpy.qos import ReliabilityPolicy, QoSProfile
#---------------------------------------------------

# Definição da classe principal do nó, herdando de Node e Laser
class LimpadorNode(Node, Laser):

    def __init__(self):
        # Chama o construtor da classe base 'Node', nomeando o nó como 'limpador_node'
        super().__init__('limpador_node')
        # Inicializa o mixin 'Laser' para processar dados do sensor de laser
        Laser.__init__(self)
        # Processa callbacks pendentes para garantir que os dados do laser estejam prontos
        rclpy.spin_once(self)
        # Cria uma instância do nó 'Girar' para controlar a rotação do robô
        self.girar_node = Girar(node = 'girar_node')

        self.opening = 15

        # Define o estado inicial da máquina de estados do robô
        self.robot_state = 'procurar'

        # Dicionário que mapeia o nome de cada estado para seu método correspondente
        self.state_machine = {
            'procurar': self.procurar,
            'esperar': self.esperar,
            'girar': self.girar,
            'limpar': self.limpar,
        }

        # Inicialização de variáveis de configuração do robô:

        # Define a distância mínima segura para evitar colisões
        self.distancia_minima = 0.4
        
        # Define a distância máxima para considerar um caminho como livre
        self.distancia_maxima = 0.6

        # Define a velocidade linear e angular padrão do robô
        self.v_linear_x = 0.1
        self.v_angular_z = 0.3

        # Variável para armazenar o ângulo de rotação alvo
        self.alvo_rot = None

        # --- Publishers ---
        # Cria um 'publisher' para o tópico 'cmd_vel' para enviar comandos de velocidade
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        # Cria uma mensagem Twist que será publicada para mover o robô
        self.twist = Twist()

        # Inicializa o timer que chamará a função 'control' a cada 0.1 segundos
        self.timer = self.create_timer(0.1, self.control)

    # --- Lógica da Máquina de Estados ---

    def procurar(self):
        """
        Estado 'procurar': O robô se move para a frente e gira levemente
        para a esquerda para buscar um obstáculo ou uma parede a seguir.
        """
        self.twist = Twist()
        self.twist.linear.x = self.v_linear_x
        self.twist.angular.z = self.v_angular_z

        # Se um obstáculo for detectado à frente ou à direita, o robô para
        # e muda para o estado 'esperar' para reavaliar a rota.
        if (min(self.front) < self.distancia_minima) or (min(self.right) < self.distancia_minima):
            self.robot_state = 'esperar'

    def esperar(self):
        """
        Estado 'esperar': O robô para e decide para qual direção irá girar.
        Ele verifica se os lados (direita, esquerda e trás) estão livres.
        """
        self.twist = Twist()

        dir_livres = []
        # Verifica se o lado direito está livre (maior que a distância máxima)
        if min(self.right) > self.distancia_maxima:
            dir_livres.append((-90)) # Adiciona um giro de -90 graus (direita)

        # Verifica se o lado esquerdo está livre
        if min(self.left) > self.distancia_maxima:
            dir_livres.append((+90)) # Adiciona um giro de +90 graus (esquerda)

        # Verifica se a parte de trás está livre
        if min(self.back) > self.distancia_maxima:
            dir_livres.append((180)) # Adiciona um giro de 180 graus (trás)

        if not dir_livres:
            return
        
        self.alvo_rot = random.choice(dir_livres)
        # Reinicia o nó de giro com o ângulo alvo selecionado
        # Transiciona para o estado 'girar' para executar a rotação
        self.robot_state = 'girar'

    def girar(self):
        """
        Estado 'girar': Controla a rotação do robô para o ângulo alvo.
        A rotação é gerenciada pelo nó 'girar_node'.
        """
        # Chama a função 'spin_once' do nó de giro para processar seu estado
        rclpy.spin_once(self.girar_node)
        self.girar_node.reset(self.alvo_rot)
        self.twist = Twist()
        # Se o nó de giro indicar que a rotação foi concluída,
        # o robô transiciona para o estado 'limpar'.
        while not self.girar_node.robot_state == 'done':  # Enquanto a rotação não terminar
            rclpy.spin_once(self.girar_node)

        self.alvo_rot = None
        self.robot_state = 'limpar'

    def limpar(self):
        """
        Estado 'limpar': O robô se move em linha reta para a frente.
        A lógica de 'limpeza' é simplificada, sendo apenas o movimento frontal.
        """
        self.twist = Twist()
        self.twist.linear.x = self.v_linear_x

        # Se um obstáculo for detectado à frente, o robô para
        # e retorna ao estado 'esperar' para recalcular a rota.
        if min(self.front) < self.distancia_minima:
            self.twist = Twist()
            self.robot_state = 'esperar'

    def control(self):
        """
        Função de controle principal: Gerencia a máquina de estados.
        É chamada periodicamente pelo timer.
        """
        print(f'Estado Atual: {self.robot_state}')
        # Chama o método associado ao estado atual do robô
        self.state_machine[self.robot_state]()

        # Publica o comando de velocidade, exceto quando o robô está no estado 'girar',
        # pois o controle de velocidade do giro é responsabilidade do 'girar_node'
        if self.robot_state != 'girar':
            self.cmd_vel_pub.publish(self.twist)

# --- Funções de Execução ---

def main(args=None):
    """
    Função principal que inicia e executa o nó.
    """
    # Inicializa a infraestrutura do ROS2
    rclpy.init(args=args)
    # Cria uma instância do nó 'LimpadorNode'
    ros_node = LimpadorNode()

    # Loop principal que mantém o nó ativo
    while not ros_node.robot_state == 'done':
        # Processa os callbacks e o timer do nó
        rclpy.spin_once(ros_node)

    # Quando o loop terminar, destrói o nó e encerra o ROS2
    ros_node.destroy_node()
    rclpy.shutdown()

# Garante que a função 'main' seja chamada ao executar o script
if __name__ == '__main__':
    main() 