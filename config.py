class Config:
    n = 30
    point_size = 15
    border_size = 1
    fill_colors = []#'red', 'green', 'blue', 'yellow']
    outline_color = ['black']*n
    def __init__(self):
       self.random()
       
    def random(self):
        self.fill_colors = []
        from random import randint
        for i in range(self.n):
            self.fill_colors.append('#%06X' % randint(0, 0xFFFFFF))