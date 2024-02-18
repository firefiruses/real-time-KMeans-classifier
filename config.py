class Config:
    n = 30
    point_size = 15
    center_size = 20
    border_size = 1
    fill_colors = []
    outline_color = ['black']*n
    center_outline_color = 'white'
    def __init__(self):
       self.random()
       
    def random(self):
        self.fill_colors = []
        from random import randint
        for i in range(self.n):
            self.fill_colors.append('#%06X' % randint(0, 0xFFFFFF))