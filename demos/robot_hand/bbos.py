import BBOSApplication
import BBOSCompiler
import BBOSDriver
import BBOSProcess

robot_compiler = BBOSCompiler.BBOSCompiler("../../src",
                                           ["../../include"],
                                           "-I",
                                           "gcc",
                                           ["-O"])
    
gpio_driver = BBOSDriver.BBOSDriver("gpio_driver_init",
                                    "gpio_driver",
                                    "gpio_driver_exit",
                                    ["/hardware/driver/gpio.c",
                                     "/hardware/driver/propeller.c"],
                                    "gpio",
                                    "GPIO_DRIVER_PORT",
                                    2)

finger = BBOSProcess.BBOSProcess(robot_compiler, 
                                 [gpio_driver],                         
                                 ["finger.c"],
                                 False,
                                 ["MOVE_PORT"],
                                 ["move"])

application = BBOSApplication.BBOSApplication([finger])

