import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile

class SecondNode(Node): # A classe SecondNode herda da classe Node
    def __init__(self): # chama o método que inicializa cada objeto criado a partir da classe SecondNode
        super().__init__('second_node') # chama o metodo inicializador da classe pai Node e define o nome do nó como 'second_node'
        self.x = 0.0 # cria o atributo self.x e define a posicao inicial no eixo x
        self.y = 0.0 # cria o atributo self.y e define a posicao inicial no eixo y
        self.odom_sub = self.create_subscription(
            Odometry, # tipo das mensagens recebidas
            '/odom', # nome do topico que sera assinado
            self.odom_callback, # método executado sempre que uma mensagem chegar
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        ) # chama o método create_subscription (ASSINA algum topico) e atribui as informacoes retornadas (objeto) no atributo 'self.odom_sub"

        self.timer = self.create_timer(0.25, self.control)

    def odom_callback(self, msg: Odometry): # atualiza x e y com a posição do robô, esse método é chamado sempre que uma mensagem Odometry é recebida. "msg" é o parâmetro que receberá a mensagem.
    # : Odometry é uma anotação de tipo, indicando que se espera um objeto do tipo Odometry
    # O parâmetro msg recebe o objeto que contém a mensagem.
        self.x = msg.pose.pose.position.x # Atualiza o atributo self.x com a posição do robô no eixo x.
        self.y = msg.pose.pose.position.y # Atualiza o atributo self.y com a posição do robô no eixo y.

    def control(self): # método chamado periodicamente pelo timer para imprimir as posições
        print(f'Posição x: {self.x:.3f}')
        print(f'Posição y: {self.y:.3f}\n')


def main(args=None):
    rclpy.init(args=args)
    node = SecondNode() # cria um objeto da classe FirstNode.
    rclpy.spin(node) # mantém o nó processando callbacks até sua execução ser interrompida, quando um evento ocorre, ele executa o callback correspondente
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__': # executa main() somente quando este arquivo é executado diretamente
    main()

# NAO ESQUECER DE ATUALIZAR O ARQUIVO setup.py COM A CRIACAO DE UM NOVO NÓ:
# DEPOIS COMPILAR AS ATUALIZACOES NO TERMINAL ("DAR colcon build")
# SEMPRE ANTES DE RODAR