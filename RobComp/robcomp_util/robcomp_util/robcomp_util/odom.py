import numpy as np
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile

# MÓDULO REUTILIZÁVEL

class Odom():
    def __init__(self):
        self.odom_sub = self.create_subscription(
            Odometry, # tipo das mensagens recebidas
            '/odom', # nome do topico que sera assinado
            self.odom_callback, # método executado sempre que uma mensagem chegar
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        ) # chama o método create_subscription (ASSINA o topico) e atribui as informacoes retornadas (objeto) no atributo 'self.odom_sub"
        rclpy.spin_once(self) # processar as mensagens recebidas pela primeira vez

    def euler_from_quaternion(self, orientation): # converte quaternion para angulos de Euler
        """Converte quaternion (formato [x, y, z, w]) para roll, pitch, yaw."""
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw # retorna tupla com as posicoes em angulos

    def odom_callback(self, msg: Odometry): # atualiza x, y e yaw com a posição do robô, esse método é chamado sempre que uma mensagem Odometry é recebida.
        self.x = msg.pose.pose.position.x # Atualiza o atributo self.x com a posição do robô no eixo x
        self.y = msg.pose.pose.position.y # Atualiza o atributo self.y com a posição do robô no eixo y.
        self.yaw = self.euler_from_quaternion(msg.pose.pose.orientation)[-1] # retorna a orientação do robô no espaço global. Valor em radianos e no intervalo de -pi a pi.

# CODIGO ADAPTADO DO criando_no_subscriber.py
# Não é necessário adicionar odom.py ao setup.py, porque ele foi criado para ser um módulo REUTILIZÁVEL, e não um nó executável diretamente.
# Um módulo reutilizável so fornecerá uma classe para outros nós importarem (nao tem os blocos def main(), nem if __name__ == '__main__')
# COMPILAR E ATUALIZAR NO TERMINAL (cb) após:
#   1) Alterar odom.py (reutilizável)
#   2) Alterar test_odom.py (nó "completo)
#   3) Alterar setup.py (incluindo test_odom.py)
#   4) Salvar arquivos modificados
# RODAR APENAS DEPOIS DE COMPILAR E ATUALIZAR TERMINAL
#   ros2 run robcomp_util test_odom