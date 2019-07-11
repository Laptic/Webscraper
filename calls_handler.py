#!/bin/python

import subprocess
import time


class ProcessObject(object):

    def __init__(self, call_in):
        # makes call into a list
        self.call = call_in.split()
        self.subprocess = None
        self.out = b""

    def execute(self):
        self.subprocess = subprocess.Popen(
            self.call,
            stdout=subprocess.PIPE)

    def poll(self):
        if not self.subprocess:
            return None
        else:
            return self.subprocess.poll()

    def get_out(self):
        if not self.out:
            stream_out = self.subprocess.stdout
            # reads in data from stream
            self.out = b"".join(stream_out.readlines())
        return self.out


class Result(object):

    def __init__(self, str_in):
        self.output = str_in
        self.parse()

    def __str__(self):
        return str(self.output)

    def parse(self):
        # do something with output
        pass


class SubprocessPool(object):
    def __init__(self, proc_num):
        self.cap = proc_num
        self.active_processes = []
        self.process_queue = []
        self.result_list = []

    def subprocess(self, os_call):
        process_temp = ProcessObject(os_call)
        self.process_queue.append(process_temp)

    def execute(self):
        # could theoretically be changed to process results simultaneously using threads
        # currently only performs multiprocessing to make multiple system calls
        while len(self.process_queue) > 0 or len(self.active_processes) > 0:
            if len(self.active_processes) < self.cap and len(self.process_queue) > 0:
                proc_temp = self.process_queue.pop(0)
                proc_temp.execute()
                self.active_processes.append(proc_temp)
            else:
                for proc in self.active_processes:
                    # if process not none, proc complete and can be removed from live list
                    if proc.poll() is not None:
                        result = Result(proc.get_out())
                        self.result_list.append(result)
                        # proc is removed from live list
                        self.active_processes.remove(proc)
                    else:
                        time.sleep(.1)
        # when all queued processes are complete, process results
        self.process_results()

    def process_results(self):
        while self.result_list:
            # do something with results
            result = self.result_list.pop(0)
            print(str(result))


# populate with system calls desired
calls_list = ["curl -ss google.com", "curl -ss reddit.com"]
sub_pool = SubprocessPool(5)

for call in calls_list:
    sub_pool.subprocess(call)
sub_pool.execute()
