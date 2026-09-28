import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile

# Nó base: modelo para criar um programa ROS que funciona continuamente:
    #1. recebe informações -> subscriber recebe os dados e manda para funcao de callback
    #2. processa essas informações -> funcao de callback guarda a informação mais recente em um atributo, como self.valor
    #3. toma uma decisão -> timer chama funcao control periodicamente
    #4. publica algum resultado -> publisher
    #5. repete o processo.

# Ex de uso dessa estrutura fora da robotica:
    # CONTROLE DE UM AR-CONDICIONADO AUTOMATICO: Sensor → temperatura atual → decisão → comando do ar-condicionado: não tem necessariamente uma tarefa única com começo e fim. Seu trabalho é monitorar e controlar CONTINUAMENTE.

class MeuNode(Node):

    def __init__(self):
        super().__init__('meu_node')

        self.sub = self.create_subscription(
            TipoDaMensagem,
            '/sensor',
            self.sensor_callback,
            10
        )

        self.pub = self.create_publisher(
            TipoDaMensagem,
            '/resultado',
            10
        )

        self.timer = self.create_timer(
            0.25,
            self.control
        )

    def sensor_callback(self, msg):
        # Guarda a informação recebida
        self.valor = msg.valor

    def control(self): # usa self.valor (recebida do callback) -> deicide o que fazer -> publica o resultado
        # Usa a informação e decide o que fazer
        ...


# EX. DE USO 1: ROBO QUASE INDECISO:
# Laser → callback guarda a distância → control decide → publica velocidade
# Versao simplificada:

# class Indeciso(Node):
#     def __init__(self):
#         super().__init__('indeciso_node')

#         self.distancia_frente = float('inf')

#         self.laser_sub = self.create_subscription(
#             LaserScan,
#             '/scan',
#             self.laser_callback,
#             10
#         )

#         self.cmd_vel_pub = self.create_publisher(
#             Twist,
#             '/cmd_vel',
#             10
#         ) # envia a velocidade para /cmd_vel

#         self.timer = self.create_timer(
#             0.25,
#             self.control
#         )

#     def laser_callback(self, msg): # recebe e guarda a distancia
#         self.distancia_frente = msg.ranges[0]

#     def control(self): # decide se o robo avanca, afasta ou para
#         twist = Twist()

#         if self.distancia_frente > 1.05:
#             twist.linear.x = 0.1

#         elif self.distancia_frente < 0.95:
#             twist.linear.x = -0.1

#         else:
#             twist.linear.x = 0.0

#         self.cmd_vel_pub.publish(twist)



# EX. DE USO 2: NO QUE EVITA OBSTACULOS:
# nó recebe as leituras do laser -> verifica se existe algo proximo -> manda robo parar ou virar
# /scan → nó anticolisão → /cmd_vel
# Versao simplificada:
# def control(self): # exemplo de decisao
#     if self.distancia_frente < 0.5:
#         self.twist.linear.x = 0.0
#         self.twist.angular.z = 0.3
#     else:
#         self.twist.linear.x = 0.2
#         self.twist.angular.z = 0.0

#     self.cmd_vel_pub.publish(self.twist)




# EX. DE USO 3: PROCESSAMENTO DE ODOMETRIA:
# nó recebe a posição pelo tópico /odom -> realiza um cálculo -> publica um resultado.
# /odom → calcula distância percorrida → /distancia
# Versao simplificada:
# def odom_callback(self, msg): # callback guardaria as coordenadas:
#     self.x = msg.pose.pose.position.x
#     self.y = msg.pose.pose.position.y

# def control(self): # calcula distancia: útil para acompanhar quanto o robô se afastou da posição inicial.
#     distancia = math.sqrt(self.x**2 + self.y**2)



# EX. DE USO 4: PROCESSAMENTO DE IMAGENS:
# nó recebe imagens da camera -> procura uma cor/objeto -> piublica a posicao encontrada
# /camera/image_raw → detector de objeto → /posicao_objeto
# Versao simplificada:
# def image_callback(self, msg): # recebe a imagem
#     self.imagem = converter_para_opencv(msg)

# def control(self): # realiza o processamento periodicamente
#     posicao = encontrar_objeto(self.imagem)
#     self.posicao_pub.publish(posicao)
