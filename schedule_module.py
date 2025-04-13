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
        self._creating_time = float()

        #stastics
        self.__created = time()
        self._turnaround_time = float()
        self._wait_time = float()
    
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
        pass
    
    @property
    def wait_time(self):
        pass

    def set_pid(self, pid) -> bool | int:
        if not self._id:
            self._pid = pid
            return pid
        else:
            return False

    def set_priority(self, priority : int) -> bool | int:
        if not self._priority:
            self.priority = priority
            return priority
        return False

    def ready(self) -> None:
        self._state = 1

    def wait(self) -> None:
        self._state = 2

    def executing(self, clock) -> bool:
        self._state = 3
        if self._execution_time > 0:
            self._execution_time -= clock
            return True
        return False
    
    def finish(self):
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
        while type(pid) != int: pid = process.set_pid(randint)
        self.__processes_ids.append(pid)
        self.__new.put(process)

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
            while process.execute():
                continue
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
            print("Executando...")

        while True:
            try:
                process = self.__finish.popleft()
                print(f"id : {process.pid} - finish!")
            except IndexError:
                break
