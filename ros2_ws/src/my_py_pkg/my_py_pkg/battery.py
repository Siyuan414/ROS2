#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed

class BatteryNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("Battery") # MODIFY NAME
        self.last_time_battery_state_changed = self.get_current_time_seconds()
        self.battery_state_ = "full"
        self.battery_timer_= self.create_timer(0.1,self.check_battery_state)
        self.set_led_client = self.create_client(SetLed,"set_led")
        self.get_logger().info("Battery node has been started")

    def check_battery_state(self):
        time_now = self.get_current_time_seconds()
        if self.battery_state_ == "full":
            if time_now - self.last_time_battery_state_changed > 4.0:
                self.battery_state_ = "empty"
                self.get_logger().info("Battery is running low..")
                self.call_set_led(2,1)
                self.last_time_battery_state_changed = time_now
        else:
            if time_now - self.last_time_battery_state_changed > 6.0:
                self.battery_state_ = "full"
                self.get_logger().info("Battery is fully charged")
                self.call_set_led(2,0)
                self.last_time_battery_state_changed = time_now
    
    def call_set_led(self,led_number,state):
        while not self.set_led_client.wait_for_service(1.0):
            self.get_logger().warn("waiting for set led services")
        
        request = SetLed.Request()
        request.led_number = led_number
        request.state = state

        future = self.set_led_client.call_async(request)
        future.add_done_callback(self.callback_set_led)

    def callback_set_led(self,future):
        response: SetLed.Response = future.result()
        if response.success:
            self.get_logger().info("LED turned on")
        else:
            self.get_logger().info("LED turned off")
    def get_current_time_seconds(self):
        seconds,nanoseconds = self.get_clock().now().seconds_nanoseconds()
        return seconds + nanoseconds/ 10000000.0

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
