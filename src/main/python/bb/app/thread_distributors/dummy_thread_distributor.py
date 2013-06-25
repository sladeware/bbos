# Copyright (c) 2013 Sladeware LLC

from bb.app.thread_distributors.thread_distributor import ThreadDistributor

class DummyThreadDistributor(ThreadDistributor):
  """This thread distributor simply puts all threads to the first processor's
  core.
  """

  def distribute(self, threads, processor):
    core = processor.get_cores()[0]
    return {
      core: threads
    }
