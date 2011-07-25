.. purpose:

*******
Purpose
*******

BBOS is designed to be a flexible, application-specific microkernel operating 
system for remote sensing, servo control, power management and security 
purposes.

Design challenges
-----------------

* **Long life**

  The device should be able to live as long as possible using its own power
  source. This goal can be achived only by applying a strict energy policy 
  which should be supported from the lowest level.

* **Small size and simplicity**

  The size of the device should be as small and lightweight as it possible 
  and therefore we have a limited computation power and memory.

* **Location independence**

  The behavior of communications should be independent of their location to 
  the extent possible. True location independence may not be achievable in all
  cases, for example, due to timing constraints or explicit coupling to 
  physical sensors or actuators. However, the implementation of object 
  functionality should be decoupled from the question of whether it accesses 
  other objects remotely or locally where appropriate.

* **Flexibility and scalability**

  The system should be flexible to be easily configured for any applications, 
  when scalability means, that additional CPUs or memory can be added to 
  (or removed from) the system without recompiling or even reconfiguring the
  kernel.

* **Single-processor and multi-processor devices**

  System works with multi-processor devices as well as with single-processor.

The main motivation behind BBOS development is that most of kernels provide 
too costly abstractions and restrict flexibility. We suppose that applications 
and so their developers know better than OSs waht the goal of their resource
management decisions should be and, therefore, they should be given as much 
control as possible over those decisions.

Remote Sensing
--------------

Remote sensing is the small or large-scal acquisition of information of an 
object or phenomenon, by the use if either recording or real-time sensing 
device(s) that are wireless, or not in physical or intimate contact with the 
object. BBOS is ideally suited for this sort of application due to its 
robustness, energy efuucuency, advanced logging, graceful degradation and 
sensor capabilities.

Distributed Servo Controller
----------------------------

A servo (servomechanism) is a devices that uses error-sensing feedback to 
correct its performance in real-time. There is a set of signals that provide 
feedback to asist in the control of the mechanical position of the device. 
Closed loop feedback is a common automatic control paradigm for a servo. BBOS 
is designed to operate servos efficiently, reliably and autonomously in 
applications such as robotics.
