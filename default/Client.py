import  multiprocessing
import logic
import body

class Client():
    def __init__(self,myID,input,output):
        self.myID = myID
        self.input = input
        self.output = output
        self.Processes = []

    def doStuff(self, bodylist, delta_time, system):

        for body in bodylist:
            body.move(delta_time,system)

        return bodylist

    def work(self):
        while(True):
            stuff = self.input.get()
            bodylist = stuff[0]
            delta_time = stuff[1]
            system = stuff[2]
            self.output.put(self.doStuff(bodylist,delta_time,system))
            self.input.task_done()

    def createJob(self):
        p = multiprocessing.Process(target=self.work)
        self.Processes.append(p)
        p.start()