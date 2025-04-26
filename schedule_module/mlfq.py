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
        self.priority = priority
        return priority
        
    
    def set_waiting_type (self, waiting_type : int) -> bool | int:
        if not self._waiting_type:
            self._waiting_type = waiting_type
            return waiting_type
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
            return True
        return False
    
    def finish(self):
        self._clock_count = 0
        self.update_turnaround()
        self._state = 4

class Queue():
    def __init__(self, qtype, quantum : int, clock = 0.1):
        self.__quantum = quantum
        self.__queue = deque()
        self.__running = None
        self.__clock = clock

        if qtype not in range(1, 4):
            raise AttributeError("qtype must be in range 1-3")
        else: self.__type = qtype # 1 : fifo , 2 : execute , 3 : wait 

    @property
    def qtype(self):
        return self.__type
    
    @property
    def quantum(self):
        return self.__quantum

    def __len__(self):
        return len(self.__queue)

    def run(self):
        if self.__type == 2:
            if self.__running != None:
                process = self.__running

                if process.check_event():
                    process.wait(self.__clock, waiting = False)
                    return self.remove()
            
                elif not process.execute(self.__clock):
                    process.finish()
                    return self.remove()
                
                elif process.clock_count == self.__quantum:
                    process.ready()
                    return self.remove()
                
                else: return process
            
            elif len(self.__queue) > 0:
                process = self.__queue[0]
                self.__running = process
            
            else: return None


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
        return self.__queue.popleft()

    def add(self, process : object) -> object:
        return self.__queue.append()


class schedule_simulator:
    def __init__(self):
        self.__processes_ids = list()
        self.__clock = 1

        self.__new = Queue(1)
        self.__finish = Queue(1)
        self.__ready = {1: Queue(2), 2: Queue(2), 3: Queue(2)}
        self.__waiting = {1: Queue(3), 2: Queue(3), 3: Queue(3)}

    def initialize(self):
        while True:
            try:
                process = self.__new.popleft()
                self.__gotoready(process)
                print(f"id : {process.pid}, priority : {process.priority} - ready!")
                print(f"execution_time : {process._execution_time} - event_time {process._event_time} - event_at {process._event_at}")
            except IndexError:
                break       

    def one_three(number : int) -> int:
        if number < 1: return 1
        elif number > 3 : return 3
        else: return number

    def len_dict_queue(dict : dict):
        total = 0
        for key, value in enumerate(dict):
            total += len(value)
        
        return total

    def set_clock(self, clock : float) -> float:
        self.__clock = clock
        return self.__clock

    def create_process(self, priority = randint(1,3), waiting_type = randint(1,3)) -> None:
        process = Process()
        pid = False
        while type(pid) != int: 
            pid = randint(100,1000)
            if pid in self.__processes_ids: pid = False
        process.set_pid(pid)

        process.set_priority(self.one_three(priority))
        process.set_waiting_type(self.one_three(waiting_type))

        self.__processes_ids.append(pid)
        self.__new.append(process)
        print(f"process {process.pid} created")

    def __gotoready(self, process : object) -> bool:
        return self.__ready[process.priority].add(process)
    
    def __gotowait(self, process : object)  -> bool:
        return self.__waiting[process.waiting_type].add(process)
    
    def __gotofinish(self, process : object) -> bool:
        return self.__finish.add(process)

    def check_finish(self) -> None:
        if self.__executing == None \
        and len(self.__waiting) == 0 \
        and len(self.__ready) == 0:
             return True
        return False
    
    def execute(self) -> None:
        if self.len_dict_queue(self.__ready) > 0:
            for key, queue in enumerate(self.__ready):
                process = queue.run()
                if not process:
                    continue
                else:
                    if process.state == 1:
                        if queue.qtype == 2: process.set_priority(1 if process.priority == 3 else (process.priority - 1))
                        self.__gotoready(process)

                    elif process.state ==  2:
                        self.__gotowait(process)
                    
                    elif process.state == 4:
                        self.__gotofinish(process)
                    break

            return True
        
        return False
    
    def wait(self) -> None:
        if self.len_dict_queue(self.__ready) > 0:
            for key, queue in enumerate(self.__waiting):
                process = queue.run()

                if not process:
                    continue
                else:
                    if process.state ==  1:
                        self.__gotoready(process)
            return True
        
        return False

    def simulation_report(self) -> dict:
        def filas_para_lista(dicionario_deques):
            return [list(dicionario_deques[p]) for p in range(1, 4)]

        def process_to_dict(p):
            d = {
                "PID": p.pid,
                "Exec": p.execution_time,
                "Wait": p.event_time,
            }
            return d

        executing = None
        for priority, queue in self.__ready:
            if len(queue) > 0:
                executing = queue[0]
                break

        return {
            "ready_1": [process_to_dict(p) for p in self.__ready[1] if p != executing],
            "ready_2": [process_to_dict(p) for p in self.__ready[2] if p != executing],
            "ready_3": [process_to_dict(p) for p in self.__ready[3] if p != executing],
            "execute": process_to_dict(executing),
            "waiting_1": [process_to_dict(p) for p in self.__waiting],
            "waiting_2": [process_to_dict(p) for p in self.__waiting],
            "waiting_3": [process_to_dict(p) for p in self.__waiting],
            "finish": [process_to_dict(p) for p in self.__finish],
        }
    
if __name__ == "__main__":
    fcfs = schedule_simulator()
    
    for i in range(5):
        fcfs.create_process()
    
    fcfs.start_simulation()
    print(fcfs.simulation_report())
