import tkinter as tk
import numpy as np
from math import sqrt
import config as cf
from tkinter import Menu, messagebox
from sklearn.cluster import KMeans

def dist(x, y):
    return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def hex_to_rgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def lighter(tup, delta):
    result = [0,0,0]
    for i in range(3):
        temp = tup[i]+delta
        if temp>255:
            temp = 255
        result[i] = int(temp)
    return tuple(result)

def make_hex_lighter(hex, delta):
    return rgb_to_hex(lighter(hex_to_rgb(hex), delta))

class App():
    def __init__(self):
        self.max_lighter = 100
        self.descredetation = 20
        self.n_clusters = 3
        self.config = cf.Config()
        self.win = tk.Tk()
        self.win.geometry('850x600')
        self.win.title('Real time KMeans')
        self.points = np.array([[100, 100], [100,200], [300, 100], [300, 200], [200, 500], [300, 500]])
        self.classes = np.array([0, 1, 0, 1])
        self.canv = tk.Canvas(self.win, borderwidth=4, relief='solid', background='#D3D3D3')
        self.canv.pack(expand=True, fill='both', padx=10, pady=10)
        self.clusters = tk.StringVar(value='3')
        self.k_means = KMeans(n_clusters=int(self.clusters.get()))
        tk.Label(self.win, text='Количество кластеров:', height=2, font=('arial', 10)).pack(side='left')
        self.clusters_input = tk.Entry(self.win, textvariable=self.clusters, font=('arial', 10))
        self.clusters_input.pack(side='left', padx=10)
        self.button = tk.Button(self.win, command=lambda:self.random(), text='Случайные цвета', font=('arial', 10))
        self.button.pack(side='left', padx=10)
        self.clusters.trace("w", lambda *args: self.try_change())

        tk.Label(self.win, text='Дискретизация фона: ', height=2, font=('arial', 10)).pack(side='left')
        self.discr = tk.StringVar(value='20')
        self.discr_input = tk.Entry(self.win, textvariable=self.discr, font=('arial', 10))
        self.discr_input.pack(side='left', padx=10)
        self.discr.trace("w", lambda *args: self.try_change())

        self.redraw_button = tk.Button(self.win, command=lambda:self.redraw(), text='Нарисовать', font=('arial', 10))
        self.redraw_button.pack(side='left', padx=10)

        self.canv.bind("<Button-1>", lambda event : self.click_on_b1(event))
        self.canv.bind("<Button-3>", lambda event : self.click_on_b2(event))
        self.help = Menu()
        self.help.add_command(label='Справка', command= lambda: self.Help())
        self.win.config(menu=self.help)
        
    def Help(self):
        s ="""Для добавления новых точек используется левая кнопка мыши.
        Для удаления уже существующих точек используется правая кнопка мыши.
        Число калестеров можно измнеить снизу в спецаильно отведенной графе ввода
        Цвета точек можно зарандомить специально отведенной кнопкой снизу."""
        messagebox.showinfo('Справка', s)
        pass

    def get_max_cluster_distances(self):
        centers = self.k_means.cluster_centers_
        labels = self.k_means.predict(centers)
        result = {}
        for ic, c in enumerate(centers):
            max = 0
            for i, p in enumerate(self.points):
                if labels[ic] == self.classes[i]:
                    d = dist(p, c)
                    if d >= max:
                        max = d
                        result[labels[ic]] = d
        return result

    def random(self):
        self.config.random()
        #self.draw()

    def try_change(self):
        if self.check_inputs():
            self.n_clusters = int(self.clusters.get())
            self.descredetation = int(self.discr.get())
        self.k_means.set_params(**{'n_clusters' : self.n_clusters})
        
        #self.classes = self.k_means.fit_predict(self.points)
        #self.draw()

    def mainloop(self):
        self.redraw()
        self.win.mainloop()

    def check_inputs(self):
        str = self.clusters_input.get()
        try:
            if int(str) < 0:
                return False
        except:
            return False
        str = self.discr.get()
        try:
            if int(str) < 0:
                return False
        except:
            return False
        return True
    
    def click_on_b1(self, event):
        self.points = np.append(self.points, [[event.x-self.config.point_size//2, event.y-self.config.point_size//2]], axis=0)
        self.canv.create_oval(self.points[-1][0], self.points[-1][1], 
                                  self.points[-1][0]+self.config.point_size, self.points[-1][1]+self.config.point_size, 
                                  fill='white',
                                  width=self.config.border_size, 
                                  outline=self.config.outline_color[0])

    def click_on_b2(self, event):
        from math import sqrt
        x = event.x
        y = event.y
        r = lambda arr: sqrt(((arr[0]-x)**2+(arr[1]-y)**2))
        indexes = []
        for i, item in enumerate(self.points):
            if r(item)<self.config.point_size:
                indexes.append(i)
        self.points = np.delete(self.points, indexes, axis=0)
        #self.predict_points()
        self.draw()

    def predict_points(self):   
        if self.check_inputs():
            self.n_clusters = int(self.clusters.get())
        self.k_means.set_params(**{'n_clusters' : self.n_clusters})
        self.classes = self.k_means.fit_predict(self.points)

    def draw_centers(self):
        centers = self.k_means.cluster_centers_
        labels = self.k_means.predict(centers)
        for ind, item in enumerate(centers):
            self.canv.create_oval(item[0], item[1], 
                                  item[0]+self.config.center_size, item[1]+self.config.center_size, 
                                  fill=self.config.fill_colors[labels[ind]],
                                  width=self.config.border_size, 
                                  outline=self.config.center_outline_color)

    def draw_background(self):
        center_dist = self.get_max_cluster_distances()
        self.canv.update()
        hght = self.canv.winfo_height()
        wdth = self.canv.winfo_width()
        centers = self.k_means.cluster_centers_
        labels = self.k_means.predict(centers)
        centers = list(zip(centers, labels))
        for i in range(0, hght, self.descredetation):
            for j in range(0, wdth, self.descredetation):
                cord = [j, i]
                l = lambda x : (x[0],x[1],dist(x[0], cord))
                arr = list(sorted(list(map(l, list(centers))), key = lambda x : x[2]))
                color = self.config.fill_colors[arr[0][1]]
                d = arr[0][2]
                clss = arr[0][1]
                coef = 2
                if clss in center_dist.keys():
                    center_d = center_dist[clss]*coef
                    if center_d <= 0:
                        center_d = coef*100
                    if d <= (center_d):
                        color = make_hex_lighter(color, (self.max_lighter* d/(center_d)))
                    else:
                        color = make_hex_lighter(color, (self.max_lighter))
                    self.canv.create_rectangle(j, i, j+self.descredetation-1, i+self.descredetation-1,
                                            fill= color,
                                            outline= color,
                                            width=0)

    def draw_points(self):
        for ind, item in enumerate(self.points):
            fill = None
            if ind >= len(self.classes):
                fill = 'white'
            else:
                fill = self.config.fill_colors[self.classes[ind]]
            self.canv.create_oval(item[0], item[1], 
                                  item[0]+self.config.point_size, item[1]+self.config.point_size, 
                                  fill=fill,
                                  width=self.config.border_size, 
                                  outline=self.config.outline_color[0])
    
    def redraw(self):
        self.predict_points()
        self.draw(with_background=True)

    def draw(self, with_background = False):
        self.canv.delete('all')
        if with_background:
                    self.draw_background()
        self.draw_centers()
        self.draw_points()
        
