application = BBOSApplication([finger, finger])

robot_compiler = BBOSCompiler("../../src",
                              ["../../include"],
                              "-I",
                              "gcc",
                              ["-O"])

finger_ports = ["gpio_driver", "finger"]

gpio_driver = BBOSDriver("gpio_driver",
                         ["/hardware/driver/gpio.c", "/hardware/driver/propeller.c"],
                         "gpio",
                         0,
                         2)

finger = BBOSProcess(robot_compiler, 
                     [gpio_driver],                         
                     ["finger.c"],
                     False,
                     finger_ports,
                     ["move"])
