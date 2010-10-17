import BBOSApplication
import BBOSBoard
import BBOSCompiler
import BBOSDriver
import BBOSProcess
import PropellerDemoBoard

class BBOSConfiguration:
    robot_compiler = BBOSCompiler.BBOSCompiler()
    
    gpio_driver = BBOSDriver.BBOSDriver(boot="gpio_driver_init",
                             main="gpio_driver",
                             exit="gpio_driver_exit",
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

    PropellerDemoBoard.PropellerDemoBoard(finger, 12)
    
    application = BBOSApplication.BBOSApplication(processes=[finger])

