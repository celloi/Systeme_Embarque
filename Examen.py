import datetime, time


class Task:

    def __init__(self, NAME, IS_INTERRUPTIBLE, PERIOD, EXECUTION_TIME, PRIORITY=0):
        self.NAME = NAME
        self.IS_INTERRUPTIBLE = IS_INTERRUPTIBLE
        self.PERIOD = PERIOD
        self.EXECUTION_TIME = EXECUTION_TIME
        self.PRIORITY = PRIORITY  # 0 by default

        self.NEXT_DEADLINE = datetime.datetime.now()
        self.LAST_EXECUTED_TIME = datetime.datetime.now()

        if self.IS_INTERRUPTIBLE == True:
            self.EXECUTION_DONE = 0
        else:
            self.EXECUTION_DONE = 100  # Big number by default

    def need_to_run(self):

        if datetime.datetime.now() > self.NEXT_DEADLINE + datetime.timedelta(seconds=self.PERIOD):
            print("\tTask " + self.NAME + "\ŧFAILED deadline.\t" + str(
                self.EXECUTION_DONE / self.EXECUTION_TIME) + "% done.")
            self.NEXT_DEADLINE += datetime.timedelta(seconds=self.PERIOD)
            self.EXECUTION_DONE = 0

        if datetime.datetime.now() > self.NEXT_DEADLINE:
            return True

        return False

    def run(self):

        global timer

        if self.IS_INTERRUPTIBLE == False:
            print(str(timer) + "\t=> " + self.NAME + " completed without interruption.")
            time.sleep(self.EXECUTION_TIME)
            self.NEXT_DEADLINE = self.NEXT_DEADLINE + datetime.timedelta(seconds=self.PERIOD)

        else:
            print(str(timer) + "\t=> " + self.NAME + " " + str(self.EXECUTION_DONE / self.EXECUTION_TIME) + "%")
            time.sleep(1)
            self.EXECUTION_DONE += 1

            if self.EXECUTION_DONE == self.EXECUTION_TIME:
                print(str(timer) + "\tTask " + self.NAME + " finished his job : 100%")
                self.EXECUTION_DONE = 0
                self.NEXT_DEADLINE = self.NEXT_DEADLINE + datetime.timedelta(seconds=self.PERIOD)
                return

            if self.NEXT_DEADLINE > datetime.datetime.now():
                print(str(timer) + "\tTask " + self.NAME + " finished his job : " + str(
                    self.EXECUTION_DONE / self.EXECUTION_TIME) + "%")
                self.EXECUTION_DONE = 0
                self.NEXT_DEADLINE = self.NEXT_DEADLINE + datetime.timedelta(seconds=self.PERIOD)
                return


if __name__ == "__main__":

    # Definition of all tasks and instanciation
    task_list = [
        Task(NAME='Pump1', IS_INTERRUPTIBLE=False, PERIOD=5, EXECUTION_TIME=2),
        Task(NAME='Pump2', IS_INTERRUPTIBLE=False, PERIOD=15, EXECUTION_TIME=3),
        Task(NAME='Machine1', IS_INTERRUPTIBLE=False, PERIOD=5, EXECUTION_TIME=5),
        Task(NAME='Machine2', IS_INTERRUPTIBLE=False, PERIOD=5, EXECUTION_TIME=3)]

    global timer
    timer = -1

    # Global scheduling loop
    while (True):

        task_to_run = None
        task_priority = 0
        timer += 1

        # Choose the task to be run
        for current_task in task_list:

            current_task_need_to_run = current_task.need_to_run()

            # Always priority to tasks that is not interruptible : Round Robin
            if current_task.IS_INTERRUPTIBLE == False and current_task_need_to_run == True:
                task_to_run = current_task
                break

            # Else choose among tasks using priority
            if current_task.IS_INTERRUPTIBLE == True and current_task_need_to_run == True and current_task.PRIORITY > task_priority:
                task_priority = current_task.PRIORITY
                task_to_run = current_task

        if task_to_run == None:
            time.sleep(1)
            print(str(timer) + "\tIdle")
        else:
            task_to_run.run()
