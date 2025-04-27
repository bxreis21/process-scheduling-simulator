from time import sleep
from time import time
from collections import deque
from random import randint, random
from threading import Lock, Condition, Thread

class Process:
    def __init__(self):
        #atribute
        self._pid = 0
        self._state = 0 # ready : 1, waiting : 2, executing : 3, finish : 4
        self._execution_time = randint(1, 10)
        self._priority = 0
        self._event_time = randint(1,5) if randint(1,5) >= 4 else 0
        self._event_at = self.execution_time // 2

        #stastics
        self.__created = time()
        self.__ready_since = 0
        self._turnaround_time = 0
        self._wait_time = 0
    
    @property
    def pid(self) -> int:
        return self._pid
    
    @property
    def state(self) -> int:
        return self._state
    
    @property
    def event_time(self) -> float:
        return self._event_time
    
    @property
    def execution_time(self) -> float:
        return self._execution_time
    
    @property
    def turnaround_time(self) :
        return round(self._turnaround_time, 2)
    
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

    def check_event(self):
        if self._event_time > 0 and self._event_at > self._execution_time:
            return True
        return False

    def ready(self) -> None:
        self._state = 1
        self.__ready_since = time()

    def wait(self, clock) -> bool:
        self._state = 2
        if self._event_time > 0:
            self._event_time -= clock
            return True
        return False

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

class schedule_simulator:
    def __init__(self):
        self.__processes_ids = list()
        self.__clock = 1

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

    def __get_out(self, process : object) -> bool:
        state = process.state
        if state == 1: self.__ready.remove(process)
        elif state == 2: self.__waiting.remove(process)
        elif state == 3: self.__executing = None
        else:
            return False
        return True

    def __gotoready(self, process : object) -> bool:
        if self.__get_out(process) or process.state == 0: 
            self.__ready.append(process)
            process.ready()
            return True
        return False
    
    def __gotowait(self, process : object)  -> bool:
        if self.__get_out(process):
            self.__waiting.append(process)
            return True
        return False
    
    def __gotofinish(self, process : object) -> bool:
        if self.__get_out(process):
            self.__finish.append(process)
            process.finish()
            return True
        return False

    def execute(self) -> None:
        status = bool()

        if self.__executing != None:
            process = self.__executing
            if process.check_event():
                self.__gotowait(process)
            
            elif not process.execute(self.__clock):
                self.__gotofinish(process)

        elif len(self.__ready) > 0:
            process = self.__ready.popleft()
            self.__executing = process
    
    def wait(self) -> None:
        if len(self.__waiting) > 0:
            for process in self.__waiting:
                temp = process.wait(self.__clock)
                if not temp:
                    self.__gotoready(process)

    def check_finish(self) -> None:
        if self.__executing == None \
        and len(self.__waiting) == 0 \
        and len(self.__ready) == 0:
             return True
        return False

    def initialize(self) -> None:
        
        while True:
            try:
                process = self.__new.popleft()
                self.__gotoready(process)
                
            except IndexError:
                break

    def simulation_report(self) -> dict:
        def process_to_dict(p):
            d = {
                "PID": p.pid,
                "Exec": p.execution_time,
                "Wait": p.event_time,
            }
        
            return d

        return {
            "ready": [process_to_dict(p) for p in self.__ready],
            "execute": [process_to_dict(self.__executing)] if self.__executing else [],
            "waiting": [process_to_dict(p) for p in self.__waiting],
            "finish": [process_to_dict(p) for p in self.__finish],
        }
    
if __name__ == "__main__":
    fcfs = schedule_simulator()
    
    for i in range(5):
        fcfs.create_process()
    
    fcfs.start_simulation()
    print(fcfs.simulation_report())
