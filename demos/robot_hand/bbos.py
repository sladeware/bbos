application = BBOSApplication([finger])

robot_compiler = BBOSCompiler("../../src",
                              ["../../include"],
                              "-I",
                              "gcc",
                              ["-O"])

gpio_driver = BBOSDriver("gpio_driver",
                         ["/hardware/driver/gpio.c",
                          "/hardware/driver/propeller.c"],
                         "gpio",
                         "GPIO_DRIVER_PORT",
                         2)

finger = BBOSProcess(robot_compiler, 
                     [gpio_driver],                         
                     ["finger.c"],
                     False,
                     ["MOVE_PORT"],
                     ["move"])
