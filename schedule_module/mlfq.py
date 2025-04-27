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
        self._priority = 0 # 1 - 3
        self._clock_count = 0
        self._waiting_type = 0 # 1 - 3
        self._event_time = 1 if randint(1,5) >= 2 else 0
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
    def priority(self) -> int:
        return self._priority
    
    @property
    def clock_count(self):
        return self._clock_count
    
    @property
    def waiting_type(self) -> int:
        return self._waiting_type
     
    @property
    def event_time(self) -> float:
        return self._event_time
    
    @property
    def event_at(self) -> float:
        return self._event_at
    
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

    def set_priority(self, priority : int) -> int:
        self._priority = priority
        return priority
    
    def set_waiting_type (self, waiting_type : int) -> bool | int:
        if not self._waiting_type:
            self._waiting_type = waiting_type
            if self._event_time > 0:
                self._event_time = (5 if self._waiting_type == 1 else (3 if self._waiting_type == 2 else 1))
            return waiting_type
        return False

    def update_turnaround(self):
        self._turnaround_time = time() - self.__created

    def update_wait_time(self):
        self._wait_time += time() - self.__ready_since

    def check_event(self):
        if self._event_time > 0 and self._event_at >= self._execution_time:
            return True
        return False

    def ready(self) -> None:
        self._state = 1
        self._clock_count = 0
        self.__ready_since = time()

    def wait(self, clock, waiting = True) -> bool:
        self._state = 2
        self._clock_count = 0
        if waiting:
            if self._event_time > 0:
                self._event_time -= clock
                return True
        return False

    def execute(self, clock) -> bool:
        self.update_wait_time()
        self._state = 3
        if self._execution_time > 0:
            self._clock_count += 1
            self._execution_time -= clock
            if self._execution_time == 0: return False
            return True
        return False
    
    def finish(self):
        self._clock_count = 0
        self.update_turnaround()
        self._state = 4

class Queue():
    def __init__(self, qtype : int, clock = 1):
        self.__queue = deque()
        self.__running = None
        self.__clock = clock
        self.__type = qtype # 1 : fifo , 2 : execute , 3 : wait 

    def __getitem__(self, index):
        return self.__queue[index]

    def __len__(self):
        return len(self.__queue)
    
    @property
    def qtype(self):
        return self.__type

    def run(self):
        if self.__type == 2:
            
            process = self.__queue[0]

            if process.check_event():
                process.wait(self.__clock, waiting = False)
                return self.remove()
        
            elif not process.execute(self.__clock):
                process.finish()
                return self.remove()
            
            elif process.clock_count == process.priority*2:
                process.ready()
                return self.remove()
            
            else: return process


        elif self.__type == 3:
            if self.__running != None:
                process = self.__running

                if not process.wait(self.__clock):
                    process.ready()
                    return self.remove()
                
                else:
                    return process

            elif len(self.__queue) > 0:
                process = self.__queue[0]
                self.__running = process
            
            else:
                return None

        else:
            return self.remove()


    def remove(self) -> object:
        self.__running = None
        if len(self.__queue) > 0:
            return self.__queue.popleft()
        return None
    
    def add(self, process : object) -> object:
        return self.__queue.append(process)


class schedule_simulator:
    def __init__(self):
        self.__processes_ids = list()
        self.__clock = 1

        self.__new = Queue(1)
        self.__finish = Queue(1)
        self.__executing = Queue(2)
        self.__ready = {1: Queue(1), 2: Queue(1), 3: Queue(1)}
        self.__waiting = {1: Queue(3), 2: Queue(3), 3: Queue(3)}

    def initialize(self):
        for i in range(len(self.__new)):
            process = self.__new.remove()
            self.__gotoready(process)

    def len_dict_queue(self, dictionary : dict):
        total = 0
        for key, value in dictionary.items():
            total += len(value)
        
        return total

    def set_clock(self, clock : float) -> float:
        self.__clock = clock
        return self.__clock

    def create_process(self, priority = None, waiting_type = None) -> None:
        def one_three(number : int) -> int:
            if number < 1: return 1
            elif number > 3 : return 3
            else: return number

        if priority is None:
            priority = randint(1, 3)
        if waiting_type is None:
            waiting_type = randint(1, 3)

        process = Process()
        pid = False
        while type(pid) != int: 
            pid = randint(100,1000)
            if pid in self.__processes_ids: pid = False
        process.set_pid(pid)

        process.set_priority(one_three(priority))
        process.set_waiting_type(one_three(waiting_type))

        self.__processes_ids.append(pid)
        self.__new.add(process)

    def __gotoready(self, process : object) -> object:
        return self.__ready[process.priority].add(process)
    
    def __gotowait(self, process : object)  -> object:
        return self.__waiting[process.waiting_type].add(process)
    
    def __gotoexecuting(self, process : object) -> object:
        if len(self.__executing) > 0: raise RuntimeError("Erro de algoritmo, fila de execução ocupada.")
        return self.__executing.add(process)

    def __gotofinish(self, process : object) -> object:
        return self.__finish.add(process)

    def check_finish(self) -> None:
        if len(self.__executing) == 0 \
        and self.len_dict_queue(self.__waiting) == 0 \
        and self.len_dict_queue(self.__ready) == 0:
             return True
        return False
    
    def execute(self) -> None:
        if len(self.__executing) == 0:
            if self.len_dict_queue(self.__ready) > 0:
                for key, queue in self.__ready.items():
                    process = queue.run()
                    if not process:
                        continue
                    else:
                        self.__gotoexecuting(process)
                    return True
            
        else:
            process = self.__executing.run()
            if process.state == 1:
                process.set_priority(1 if process.priority == 3 else (process.priority + 1))
                self.__gotoready(process)

            elif process.state ==  2:
                self.__gotowait(process)

            elif process.state == 4:
                self.__gotofinish(process)

            return True
        
        return False
    
    def wait(self) -> None:
        if self.len_dict_queue(self.__waiting) > 0:
            for key, queue in self.__waiting.items():
                process = queue.run()

                if not process:
                    continue
                else:
                    if process.state ==  1:
                        self.__gotoready(process)

            return True
        
        return False

    def simulation_report(self) -> dict:

        def process_to_dict(p):
            d = {
                "PID": p.pid,
                "Exec": p.execution_time,
                "Quantum": p.clock_count,
                "Wait": p.event_time,
                "Event_at": p.event_at
            }
            return d

        return {
            "ready_1": [process_to_dict(p) for p in self.__ready[1]],
            "ready_2": [process_to_dict(p) for p in self.__ready[2]],
            "ready_3": [process_to_dict(p) for p in self.__ready[3]],
            "executing": [process_to_dict(p) for p in self.__executing],
            "waiting_1": [process_to_dict(p) for p in self.__waiting[1]],
            "waiting_2": [process_to_dict(p) for p in self.__waiting[2]],
            "waiting_3": [process_to_dict(p) for p in self.__waiting[3]],
            "finish": [process_to_dict(p) for p in self.__finish],
        }
    
if __name__ == "__main__":
    mlfq = schedule_simulator()
    
    for i in range(5):
        mlfq.create_process()
    
    mlfq.initialize()

    print(mlfq.simulation_report())

    mlfq.execute()
    mlfq.wait()

    print(mlfq.simulation_report())
