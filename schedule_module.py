from time import sleep
from time import time
from collections import deque
from random import randint, random

class Process():
    def __init__(self, execution_time_level = 1):
        #atribute
        self._pid = 0
        self._state = 0 # ready : 1, waiting : 2, executing : 3, finish : 4
        self._execution_time = random()*5*execution_time_level
        self._priority = 0

        #stastics
        self.__created = time()
        self.__ready_since = float(0)
        self._turnaround_time = float(0)
        self._wait_time = float(0)
    
    @property
    def pid(self) -> int:
        return self._pid
    
    @property
    def state(self) -> int:
        return self._state
    
    @property
    def execution_time(self) -> float:
        return self._execution_time
    
    @property
    def turnaround_time(self) :
        return round(self._turnaround_time * 10**6, 2)
    
    @property
    def wait_time(self):
        return round(self._wait_time  * 10**6, 2)

    def set_pid(self, pid) -> bool | int:
        if not self._pid:
            self._pid = pid
            return pid
        else:
            return False

    def set_priority(self, priority : int) -> bool | int:
        if not self._priority:
            self.priority = priority
            return priority
        return False

    def update_turnaround(self):
        self._turnaround_time = time() - self.__created

    def update_wait_time(self):
        self._wait_time += time() - self.__ready_since

    def ready(self) -> None:
        self._state = 1
        self.__ready_since = time()

    def wait(self) -> None:
        self._state = 2

    def execute(self, clock) -> bool:
        self.update_wait_time()
        self._state = 3
        if self._execution_time > 0:
            self._execution_time -= clock
            return True
        return False
    
    def finish(self):
        self.update_turnaround()
        self._state = 4

class Fcfs_simulator():
    def __init__(self):
        self.__processes_ids = list()
        self.__clock = 0.1
        self.__new = deque()
        self.__ready = deque()
        self.__waiting = list()
        self.__executing = None
        self.__finish = deque()

    def set_clock(self, clock : float) -> float:
        self.__clock = clock
        return self.__clock

    def create_process(self) -> None:
        process = Process()
        pid = False
        while type(pid) != int: 
            pid = randint(100,1000)
            if pid in self.__processes_ids: pid = False
        process.set_pid(pid)
        self.__processes_ids.append(pid)
        self.__new.append(process)
        print(f"process {process.pid} created")

    def get_out(self, process : object) -> bool:
        state = process.state
        if state == 1: self.__ready.remove(process)
        elif state == 2: self.__waiting.remove(process)
        elif state == 3: self.__executing = None
        else:
            return False
        return True

    def gotoready(self, process : object)  -> bool:
        if self.get_out(process) or process.state == 0: 
            self.__ready.append(process)
            process.ready()
            return True
        return False
    
    def gotowait(self, process : object)  -> bool:
        if self.get_out(process):
            self.__finish.append(process)
            process.wait()
            return True
        return False

    def execute(self) -> None:
        if len(self.__ready) > 0:
            process = self.__ready.popleft()
            self.__executing = process
            print(f"Executing {self.__executing.pid}", end='')
            while process.execute(self.__clock):
                print(".", end='')
            if self.get_out(process): self.gotofinish(process)
            else: raise RuntimeError("deu ruim")
            return True
        return False
    
    def gotofinish(self, process : object) -> bool:
        if self.get_out(process):
            self.__finish.append(process)
            process.finish()
            return True
        return False

    def start_simulation(self):
        
        print("Creating processes...")
        while True:
            try:
                process = self.__new.popleft()
                self.gotoready(process)
                print(f"id : {process.pid} - ready!")
            except IndexError:
                break

        while self.execute():
            print("finish")

        print("Simulation Report")
        while True:
            try:
                process = self.__finish.popleft()
                print(f"id : {process.pid} - success - turnaround: {process.turnaround_time} us - wait time: {process.wait_time} us")
            except IndexError:
                break


if __name__ == "__main__":
    fcfs = Fcfs_simulator()
    
    for i in range(5):
        fcfs.create_process()
    
    fcfs.start_simulation()



