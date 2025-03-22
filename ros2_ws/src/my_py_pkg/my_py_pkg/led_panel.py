#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedStateArray
from my_robot_interfaces.srv import SetLed

class LedPanelNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("led_panel") # MODIFY NAME
        self.led_states_ = [0,0,0]
        self.led_states_pub_ = self.create_publisher(
            LedStateArray,"led_panel_state",10
        )
        self.led_states_timer_ = self.create_timer(
            5.0, self.publish_led_states
        )
        self.set_led_service_ = self.create_service(SetLed,"set_led",self.call_back_set_led)
        self.get_logger().info("LED panel node has been started")

    def publish_led_states(self):
        msg = LedStateArray()
        msg.led_states = self.led_states_ 
        self.led_states_pub_.publish(msg)

    def call_back_set_led(self,request:SetLed.Request, repsonse:SetLed.Response):
        led_number = request.led_number
        state = request.state

        if led_number >= len(self.led_states_) or led_number < 0:
            repsonse.success = False
            return repsonse
        if state not in [0,1]:
            repsonse.success = False
            return repsonse
        self.led_states_[led_number] = state
        self.publish_led_states()
        repsonse.success = True
        return repsonse  

def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
