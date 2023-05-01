class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 1
        self.direction = "right"
    
    def move(self):
        if self.direction == "right":
            self.x += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
