import datetime
import time
import threading
import random

global tank
global stocks_roues
global stocks_moteur


################################################################################
#   Watchdog to stop tasks
################################################################################
class Watchdog(threading.Thread):
    period = -1
    current_cpt = -1

    ############################################################################
    def __init__(self, period):

        self.period = period

        threading.Thread.__init__(self)

    ############################################################################
    def run(self):

        print(" : Starting watchdog")

        self.current_cpt = self.period

        while (1):

            if (self.current_cpt >= 0):

                self.current_cpt -= 1
                time.sleep(1)

            else:
                print("!!! Watchdog stops tasks.")
                global watchdog
                watchdog = True
                self.current_cpt = self.period


################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():
    name = None
    priority = -1
    period = -1
    execution_time = -1
    last_deadline = -1
    last_execution_time = None

    ############################################################################
    def __init__(self, name, priority, period, execution_time, last_execution):

        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.last_execution_time = last_execution

    ############################################################################
    def run(self):

        # Update last_execution_time
        self.last_execution_time = datetime.datetime.now()

        global watchdog

        execution_time = self.execution_time

        print(self.name + " : Starting task (" + self.last_execution_time.strftime(
            "%H:%M:%S") + ") : execution time = " + str(execution_time))

        while (watchdog == False):

            execution_time -= 1

            time.sleep(1)

            if (execution_time <= 0):
                print(self.name + " : Terminating normally (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
                return

        print(self.name + " : Pre-empting task (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':

    # Init and instanciation of watchdog
    global watchdog
    watchdog = False

    stocks_roues = 0
    stocks_moteur = 0
    tank = 0

    ISPUMP = True
    ISMACH = False
    nbrou = 0;

    my_watchdog = Watchdog(period=10)  # Watchdog 10 seconds
    my_watchdog.start()

    last_execution = datetime.datetime.now()

    # Instanciation of task objects
    task_list = []
    task_list.append(my_task(name="pump1", priority=1, period=5, execution_time=2, last_execution=last_execution))
    task_list.append(my_task(name="pump2", priority=1, period=15, execution_time=3, last_execution=last_execution))
    task_list.append(my_task(name="machine1", priority=1, period=5, execution_time=5, last_execution=last_execution))
    task_list.append(my_task(name="machine2", priority=1, period=5, execution_time=3, last_execution=last_execution))

    # Global scheduling loop
    while (1):

        print("\nScheduler tick : " + datetime.datetime.now().strftime("%H:%M:%S"))

        # Reinit watchdog
        watchdog = False
        my_watchdog.current_cpt = 10

        for task_to_run in task_list:
            # Reinit watchdog
            watchdog = False
            my_watchdog.current_cpt = 10
            # le principe utilisee consiste à creer 4 Roues et un moteur tou en remplissant equitable les reservoires
            if ISPUMP:
                if task_to_run.name == "pump1":
                    task_to_run.run()
                    tank += 10
                elif task_to_run.name == "pump2":
                    task_to_run.run()
                    tank += 20
                    ISPUMP = False
                else:
                    continue
            elif not ISPUMP:
                if task_to_run.name == "machine2" and nbrou <4:
                    task_to_run.run()
                    stocks_roues += 1
                    tank -= 5
                    nbrou += 1
                    if nbrou == 4:
                        ISPUMP = True
                elif task_to_run.name == "machine1" and nbrou ==4:
                    task_to_run.run()
                    stocks_moteur += 1
                    tank -= 25
                    ISPUMP = True
                    nbrou = 0
                else:
                    continue

        print("Nombres de roues produits :" + str(stocks_roues))

        print("Nombres de moteurs :" + str(stocks_moteur))
