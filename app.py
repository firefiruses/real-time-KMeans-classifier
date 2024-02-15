import tkinter as tk
import numpy as np
import config as cf
from tkinter import Menu, messagebox
from sklearn.cluster import KMeans
class App():
    def __init__(self):
        self.n_clusters = 2
        self.config = cf.Config()
        self.win = tk.Tk()
        self.win.geometry('700x600')
        self.win.title('Real time Knn')
        self.points = np.array([[100, 100], [100,200], [300, 100], [300, 200]])
        self.classes = np.array([0, 1, 0, 1])
        self.canv = tk.Canvas(self.win, borderwidth=4, relief='solid', background='#D3D3D3')
        self.canv.pack(expand=True, fill='both', padx=10, pady=10)
        self.clusters = tk.StringVar(value='2')
        self.k_means = KMeans(n_clusters=int(self.clusters.get()))
        tk.Label(self.win, text='Количество кластеров:', height=2, font=('arial', 10)).pack(side='left')
        self.clusters_input = tk.Entry(self.win, textvariable=self.clusters, font=('arial', 10))
        self.clusters_input.pack(side='left')
        self.button = tk.Button(self.win, command=lambda:self.random(), text='Случайные цвета', font=('arial', 10))
        self.button.pack(side='left')
        self.clusters.trace("w", lambda *args: self.try_change())
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
    def random(self):
        self.config.random()
        self.draw()

    def try_change(self):
        if self.check_inputs():
            self.n_clusters = int(self.clusters.get())
        self.k_means.set_params(**{'n_clusters' : self.n_clusters})
        self.classes = self.k_means.fit_predict(self.points)
        self.draw()

    def mainloop(self):
        self.predict_points()
        self.draw()
        self.win.mainloop()

    def check_inputs(self):
        str = self.clusters_input.get()
        try:
            int(str)
        except:
            return False
        return True
    
    def click_on_b1(self, event):
        self.points = np.append(self.points, [[event.x-self.config.point_size//2, event.y-self.config.point_size//2]], axis=0)
        self.predict_points()
        self.draw()

    def click_on_b2(self, event):
        from math import sqrt
        x = event.x
        y = event.y
        r = lambda arr: sqrt(((arr[0]-x)**2+(arr[1]-y)**2))
        indexes = []
        for i, item in enumerate(self.points):
            print(r(item))
            if r(item)<self.config.point_size:
                indexes.append(i)
        self.points = np.delete(self.points, indexes, axis=0)
        self.predict_points()
        self.draw()

    def predict_points(self):
        if self.check_inputs():
            self.n_clusters = int(self.clusters.get())
        self.k_means.set_params(**{'n_clusters' : self.n_clusters})
        self.classes = self.k_means.fit_predict(self.points)

    def draw_points(self):
        for ind, item in enumerate(self.points):
            self.canv.create_oval(item[0], item[1], 
                                  item[0]+self.config.point_size, item[1]+self.config.point_size, 
                                  fill=self.config.fill_colors[self.classes[ind]],
                                  width=self.config.border_size, 
                                  outline=self.config.outline_color[self.classes[ind]])
    
    def draw(self):
        self.canv.delete('all')
        self.draw_points()
        
