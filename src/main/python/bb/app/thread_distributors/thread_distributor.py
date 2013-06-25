class ThreadDistributor(object):
  """Base class for thread distributors."""

  def distribute(self, threads, processor):
    """Distributes threads over the processor's cores.

    :param threads: A list of :class:`~bb.app.os.thread.Thread` instances.
    :param processor: A
      :class:`~bb.app.hardware.devices.processors.processor.Processor` instance.
    """
    raise NotImplementedError()

  def __call__(self, threads, processor):
    return self.distribute(threads, processor)
