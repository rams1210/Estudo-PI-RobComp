import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from sensor_msgs.msg import LaserScan

# MÓDULO REUTILIZÁVEL

class Laser():
    def __init__(self):
        self.opening = 5 # armazenar a abertura do sensor laser, ao mudar esse valor, podemos modificar o que consideramos como "frente" do robô
        self.scan_sub = self.create_subscription(
            LaserScan, # tipo das mensagens recebidas
            '/scan', # nome do topico que sera assinado
            self.scan_callback,  # método executado sempre que uma mensagem chegar
            QoSProfile(depth=10, reliability=reliability=ReliabilityPolicy.RELIABLE) # para o robô real é necessário alterar RELIABLE para BEST_EFFORT, por limitações de hardware.
        )
        rclpy.spin_once(self) # processar as mensagens recebidas pela primeira vez

    # def scan_callback(self, robcompehlegal: LaserScan):
    def scan_callback(self, msg: LaserScan): # esse método é chamado sempre que uma mensagem LaserScan é recebida.
        self.laser_msg = np.array(msg.ranges).round(decimals=2) # converter a lista em um array numpy
        self.laser_msg[self.laser_msg == 0] = np.inf
        self.laser_msg = self.laser_msg.tolist() # converter self.laser_msg para uma lista novamente
        # Fatiamento na lista self.laser_msg:
        self.left = self.laser_msg[90-self.opening:90+self.opening]
        self.right = self.laser_msg[270-self.opening:270+self.opening]
        self.back = self.laser_msg[180-self.opening:180+self.opening]
        self.front = self.laser_msg[-self.opening:0] + self.laser_msg[0:self.opening]

# CODIGO ADAPTADO DO criando_no_subscriber.py
# Não é necessário adicionar laser.py ao setup.py, porque ele foi criado para ser um módulo REUTILIZÁVEL, e não um nó executável diretamente.
# Um módulo reutilizável so fornecerá uma classe para outros nós importarem (nao tem os blocos def main(), nem if __name__ == '__main__')
# COMPILAR E ATUALIZAR NO TERMINAL (cb) após:
#   1) Alterar laser.py (reutilizável)
#   2) Alterar test_laser.py (nó "completo)
#   3) Alterar setup.py (incluindo test_laser.py)
#   4) Salvar arquivos modificados
# RODAR APENAS DEPOIS DE COMPILAR E ATUALIZAR TERMINAL
#   ros2 run robcomp_util test_laser

# COMANDO para ver o conteudo do tópico scan: ros2 topic echo /scan
# INTERPRETANDO OUTPUT:
#   header: cabeçalho com info de tempo de envio e frame de referencia
#   angle_min: 0.0: Ângulo inicial do sensor. O valor 0.0 corresponde a leiura do sensor diretamente para frente do robô.
#   angle_max: 6.28...: Ângulo final do sensor. O valor 6.28... equivale a uma volta completa (360 graus = 3pi).
#   angle_increment: 0.017...: Incremento angular entre cada leitura do sensor. O valor 0.017... equivale a um ângulo de 1 grau.
#   scan_time & time_increment: 0.0: Tempo de varredura do sensor e tempo entre cada leitura. O valor 0.0 indica que o sensor está configurado para enviar as leituras o mais rápido possível.
#   range_min: 0.119... [m]: Distância mínima que o sensor consegue detectar. O valor 0.119... equivale a 11.9 cm.
#   range_max: 3.5 [m]: Distância máxima que o sensor consegue detectar. O valor 3.5 equivale a 3.5 m.
#   ranges: [inf, inf, inf, ...]: Vetor com as leituras do sensor. O tamanho do vetor é igual a angle_max/angle_increment = 6.28/0.017, ou seja, a lista de leituras é composta por 360 elementos que representam as leituras do sensor a cada 1 grau. As medições são no sentido anti-horário, sendo 0 graus na parte de frente do robô. Na simulação, inf indica que o sensor não detectou nada naquela direção, no robô real, o valor 0 indica que o sensor não conseguiu fazer a leitura.
#   intensities: [...]: Vetor com as intensidades das leituras do sensor. Nosso sensor não possui essa informação, portanto, pode desconsiderar esse campo.
# Pergunta: Qual o indice do vetor ranges que representa a leitura do sensor diretamente para frente do robô? E da esquerda? E da direita? E para trás?
# Resposta:
    # frente = msg.ranges[0]
    # esquerda = msg.ranges[90]
    # direita = msg.ranges[270]
    # tras = msg.ranges[180]
