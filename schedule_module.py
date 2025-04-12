from time import sleep
from time import time
from collections import deque

class Process():
    def __init__(self):
        #atribute
        self._id = 0
        self._state = int() #unborn, ready, waiting, executing, finish 
        self.time = int() #execution time
        self.priority = int()
        self.creating_time = float()

        #stastics
        self.__created = time()
        self._turnaround_time = float()
        self._wait_time = float()


    def set_id(self, id):
        if not self._id:
            self._id = id
            return id
        else:
            return False
        
    def get_id(self):
        return self._id
    
    def get_turnaround_time(self):
        return self._turnaround_time
    
    def get_wait_time(self):
        return self._wait_time

    def wait(self):
        self._state = 2

    def ready(self):
        self._state = 3

    def finish(self):
        self._state = 4

    def execute(self, quantum = 0):
        self._state = 1
        clock = 0.1
        timer =  quantum/clock if quantum else self.time

        for i in range(timer):
            self.time -= clock
            quantum -= clock
            sleep(clock)
            if self.time == 0:
                break
        
        return True if self.time == 0 else False

class Fcfs_simulator():
    def __init__(self):
        self.process = deque()
        self.ready = list()
        self.waiting = list()
        self.executing = None
        self.finish = list()

    def create_process(self):
        process = Process()
        process.set_id(2)
        self.process.put()

    def new_to_ready():
        pass

    def processing():
        pass
    
    def finish():
        pass

    def wait():
        pass

    def wait_to_ready():
        pass

    def start_simulation():
        pass


    

        
    
