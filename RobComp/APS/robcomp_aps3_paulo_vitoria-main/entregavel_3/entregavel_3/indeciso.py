import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist, Point

from robcomp_util.laser import Laser

class IndecisoNode(Node, Laser): 
    def __init__(self):
        super().__init__('indeciso_node') 
        Laser.__init__(self)
        

        self.robot_state = 'forward'
        self.state_machine = {
            'forward': self.forward,
            'backward': self.backward,
            'stop': self.stop
        }
        self.dmin = 0.95
        self.dmax = 1.05

        self.estados_clientes = []

        self.twist = Twist()
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.timer = self.create_timer(0.05, self.control)

    def forward(self):
        distancia = min(self.front)

        if distancia < self.dmin:
            self.robot_state = 'backward'
            self.twist = Twist()
        elif distancia <= self.dmax:
            self.robot_state = 'stop'
            self.twist = Twist()
        else:
            self.twist = Twist()
            self.twist.linear.x = 0.09


    def backward(self):
        distancia = min(self.front)

        if distancia > self.dmax:
            self.robot_state = 'forward'
            self.twist = Twist()
        elif distancia >= self.dmin:
            self.robot_state = 'stop'
            self.twist = Twist()
        else:
            self.twist = Twist()
            self.twist.linear.x = -0.09


    def stop(self):
        distancia = min(self.front)
        self.twist = Twist()

        if distancia < self.dmin:
            self.robot_state = 'backward'
        elif distancia > self.dmax:
            self.robot_state = 'forward'
    

    def done(self):
        self.twist = Twist()

    def control(self): 
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]() 
        if self.robot_state not in self.estados_clientes: 
            self.cmd_vel_pub.publish(self.twist) 
 
def main(args=None):
    rclpy.init(args=args) 
    ros_node = IndecisoNode()

    while not ros_node.robot_state == 'done': 
        rclpy.spin_once(ros_node) 

    ros_node.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()
