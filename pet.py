import random

class Pet:
    def __init__(self, img):
        self.sprite = img
        self.position = None
        self.state = 'IDLE' # either IDLE, MOVING, LEAVE_SCREEN or ASLEEP.
        self.direction = 'EAST'
        self.next_time = 0

    def update_next_time(self, cur_time):
        match self.state:
            case 'IDLE':
                self.next_time = self.next_time + cur_time + random.randint(1000,5000)
            case 'ASLEEP':
                self.next_time = self.next_time + cur_time + random.randint(30000,120000)
            
    def update_state(self):
        if self.state == 'IDLE':
            states = ['IDLE', 'MOVING', 'ASLEEP']      
            self.state = random.choice(states)
        else:
            self.state = 'IDLE'
    