import BBOSApplication
import BBOSCompiler
import BBOSDriver
import BBOSProcess

class BBOSConfiguration:
    robot_compiler = BBOSCompiler.BBOSCompiler(base="../../src",
                                  includes=["../../include"],
                                  include_argument="-I",
                                  name="gcc",
                                  options=["-O"])
    
    gpio_driver = BBOSDriver.BBOSDriver(boot_function="gpio_driver_init",
                             entry_function="gpio_driver",
                             exit_function="gpio_driver_exit",
                             files=["/hardware/driver/gpio.c",
                                    "/hardware/driver/propeller.c"],
                             name="gpio",
                             port="GPIO_DRIVER_PORT",
                             version=2)

    finger = BBOSProcess.BBOSProcess(compiler=robot_compiler, 
                         drivers=[gpio_driver],                         
                         files=["finger.c"],
                         ipc=True,
                         mempools=["MOVE_MESSAGES"],
                         ports=["MOVE_PORT"],
                         threads=["move"])
    
    application = BBOSApplication.BBOSApplication(processes=[finger])

