import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class FirstNode(Node): # A classe FirstNode herda da classe Node
    def __init__(self): # metodo de inicializacao do objeto
        super().__init__('first_node') # chama o __init__ da classe pai Node e define o nome do nó como 'first_node'
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10) # atribuindo nome self.vel_pub à chamada do método create_publisher que recebe 3 argumentos / cria um publisher e armazena o objeto retornado no atributo self.vel_pub
        self.timer = self.create_timer(0.25, self.control) # atribuindo nome self.timer ao objeto retornado por create_timer que recebe 2 argumentos: 0.25s é o tempo entre as execuçoes da funcao/metodo self.control (sera chamada a cada 0.25s)
        # OBS.: self.vel_pub e self.timer sao ATRIBUTOS da instância (começam com self) -> permite que outros métodos do mesmo objeto, como control, acessem esses valores

    def control(self): # metodo control cria a cada vez que é chamada:
        msg = Twist() # cria um objeto da classe Twist e o atribui à variável local msg
        msg.linear.x = 0.2  # atribui uma velocidade linear de 0.2 m/s ao robo na direcao x
        self.vel_pub.publish(msg) # publica essa mensagem no topico /cmd_vel


def main(args=None):
    rclpy.init(args=args) # inicializa biblioteca rclpy
    node = FirstNode() # cria um objeto que pertence a classe FirstNode e o nomeia de node
    rclpy.spin(node) # mantem o no em execucao ate que ele seja finalizado
    node.destroy_node() # finaliza o no
    rclpy.shutdown() # finaliza o modulo rclpy

if __name__ == '__main__':     # Executa main() somente quando este arquivo é executado diretamente.
    main()

# NAO ESQUECER DE ATUALIZAR O ARQUIVO setup.py COM A CRIACAO DE UM NOVO NÓ: cria o comando first_node que executa a funcao main em dentro da pasta my _package
# DEPOIS COMPILAR AS ATUALIZACOES NO TERMINAL ("DAR colcon build")