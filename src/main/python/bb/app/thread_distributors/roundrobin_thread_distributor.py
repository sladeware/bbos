# Copyright (c) 2013 Sladeware LLC

from bb.app.os.thread import Thread
from bb.app.thread_distributors.thread_distributor import ThreadDistributor

class RoundrobinThreadDistributor(ThreadDistributor):
  """Default thread distributor provides round-robin distribution of threads
  between all cores within the processors.
  """

  def distribute(self, threads, processor):
    """Distributes `threads` over `processor`'s cores.

    :param threads: A list of :class:`~bb.app.os.thread.Thread` instances.
    :param processor: A
      :class:`~bb.app.hardware.devices.processors.processor.Processor` instance.

    :returns: A `dict` instance, where key is a core and value is a list of
      :class:`~bb.app.os.thread.Thread` instances.
    """
    distribution = {}
    for core in processor.get_cores():
      distribution[core] = []
    c = 0
    for thread in threads:
      if not isinstance(thread, Thread):
        raise TypeError("thread must be derived from Thread")
      core = processor.get_cores()[c]
      c = (c + 1) % len(processor.get_cores())
      distribution[core].append(thread)
    return distribution
