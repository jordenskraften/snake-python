class TimedObject:
    def __init__(self, lifetime):
        self.lifetime = lifetime
        self.enter()

    def timer_tick(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.death()

    def enter():
        pass  

    def death():
        pass 


class GlobalTimer:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def tick(self):
        for observer in self.observers:
            observer.timer_tick()
 