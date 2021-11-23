import math
from tkinter import *
import time
import random
from tkinter import messagebox
from abc import ABCMeta, abstractmethod

window = Tk()
app_running = True

size_canvas_x = 800
size_canvas_y = 500
x = 50  # amount of Person objects


def on_closing():
    global app_running
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        app_running = False
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("Simulation")
window.resizable(0, 0)

canvas = Canvas(window, width=size_canvas_x, height=size_canvas_y, bd=0,
                highlightthickness=0)

canvas.pack()
window.update()
list_ids = []


# class State(metaclass=ABCMeta):
#     @abstractmethod
#     def infect(self):
#         pass
#
#
# class NotInfectedState(State):
#
#     def infect(self):
#         pass
#
#
# class InfectedState(State):
#
#     def infect(self):
#         if len(population) >= 2:
#             for element in population:
#                 if self != element:
#                     if element in self.distance_log.keys():
#                         time_diff = abs(self.distance_log[element] - time.process_time())
#                         if time_diff >= 3:
#                             element.infected = True
#                             element.time_of_infection = time.process_time()
#                             self.canvas.itemconfig(element.ball, fill='red')
#
#
# class ImmuneState(State):
#
#     def infect(self):
#         pass


class Person:

    def __init__(self, curr_canvas, x_coord, y_coord, module, angle, infected, flag=1):
        self.canvas = curr_canvas

        if infected == 1:
            self.infected = True
            self.ball = canvas.create_oval(x_coord - 10, y_coord - 10, x_coord + 10, y_coord + 10, fill="red")
            self.time_of_infection = 0.0
        else:
            self.infected = False
            self.ball = canvas.create_oval(x_coord - 10, y_coord - 10, x_coord + 10, y_coord + 10, fill="white")
            self.time_of_infection = None

        list_ids.append(self.ball)
        self.current_x_coord = x_coord    # x coordinate of the center
        self.current_y_coord = y_coord    # y coordinate of the center
        self.module = module
        self.curr_angle = angle
        self.x_speed = module * math.cos(math.radians(angle))
        self.y_speed = module * math.sin(math.radians(angle))
        self.flag = 1
        self.distance_log = {}
        self.is_immune = None

    # def change_state(self, state: State) -> None:
    #     self._state = state

    def move_ball(self):
        if self.canvas.coords(self.ball)[1] <= 0:
            if self.flag == 1:
                if random.randint(0, 2) == 1:
                    if self.curr_angle > 270:
                        self.curr_angle = 90 - (self.curr_angle % 90)
                    else:
                        self.curr_angle = 180 - (self.curr_angle % 90)

                    self.x_speed = self.module * math.cos(math.radians(self.curr_angle))
                    self.y_speed = self.module * math.sin(math.radians(self.curr_angle))
                else:
                    self.flag = False

            self.canvas.move(self.ball, self.x_speed, self.y_speed)
            # self.canvas.after(20, lambda: self.move_ball())

        elif self.canvas.coords(self.ball)[1] >= size_canvas_y - 20:
            if self.flag == 1:
                if random.randint(0, 2) == 1:
                    if self.curr_angle > 90:
                        self.curr_angle = 270 - (self.curr_angle % 90)
                    else:
                        self.curr_angle = 360 - (self.curr_angle % 90)
                    self.x_speed = self.module * math.cos(math.radians(self.curr_angle))
                    self.y_speed = self.module * math.sin(math.radians(self.curr_angle))
                else:
                    self.flag = False
            self.canvas.move(self.ball, self.x_speed, self.y_speed)
            # self.canvas.after(20, lambda: self.move_ball())

        elif self.canvas.coords(self.ball)[0] <= 0:
            if self.flag == 1:
                if random.randint(0, 2) == 1:
                    if self.curr_angle > 180:
                        self.curr_angle = 360 - (self.curr_angle % 90)
                    else:
                        self.curr_angle = 90 - (self.curr_angle % 90)
                    self.x_speed = self.module * math.cos(math.radians(self.curr_angle))
                    self.y_speed = self.module * math.sin(math.radians(self.curr_angle))
                else:
                    self.flag = False
            self.canvas.move(self.ball, self.x_speed, self.y_speed)
            # self.canvas.after(20, lambda: self.move_ball())

        elif self.canvas.coords(self.ball)[0] >= size_canvas_x - 20:
            if self.flag == 1:
                if random.randint(0, 2) == 1:
                    if self.curr_angle > 180:
                        self.curr_angle = 270 - (self.curr_angle % 90)
                    else:
                        self.curr_angle = 180 - (self.curr_angle % 90)
                    self.x_speed = self.module * math.cos(math.radians(self.curr_angle))
                    self.y_speed = self.module * math.sin(math.radians(self.curr_angle))
                else:
                    self.flag = False
            self.canvas.move(self.ball, self.x_speed, self.y_speed)
            # self.canvas.after(20, lambda: self.move_ball())

        else:
            if random.randint(0, 20) < 1:
                self.module = random.uniform(1, 2.5)
                self.curr_angle = random.uniform(self.curr_angle - 30, self.curr_angle + 30)
                self.x_speed = self.module * math.cos(math.radians(self.curr_angle))
                self.y_speed = self.module * math.sin(math.radians(self.curr_angle))

            self.canvas.move(self.ball, self.x_speed, self.y_speed)
            # self.canvas.after(20, lambda: self.move_ball())
        self.current_x_coord = self.canvas.coords(self.ball)[0]
        self.current_y_coord = self.canvas.coords(self.ball)[1]

    def delete_if_off_screen(self):
        if self.flag == 0:
            if (self.canvas.coords(self.ball)[0] < -30 or self.canvas.coords(self.ball)[0] > size_canvas_x + 10) or (
                    self.canvas.coords(self.ball)[1] < -30 or self.canvas.coords(self.ball)[1] > size_canvas_y + 10):
                population.remove(self)
                list_ids.remove(self.ball)

    @staticmethod
    def create_new_if_needed():
        amount_to_create = x - len(population)
        if amount_to_create > 0:

            for _ in range(amount_to_create):
                side = random.randint(1, 5)
                if side == 1:
                    population.append(
                        Person(canvas, random.uniform(100, size_canvas_x - 100), -20,
                               2,
                               random.uniform(80, 100), random.randint(1, 11), 2))
                elif side == 2:
                    population.append(
                        Person(canvas, -20, random.uniform(100, size_canvas_y - 100),
                               2,
                               random.uniform(190, 170), random.randint(1, 11), 2))
                elif side == 3:
                    population.append(
                        Person(canvas, random.uniform(100, size_canvas_x - 100), size_canvas_y,
                               2,
                               random.uniform(260, 280), random.randint(1, 11), 2))
                elif side == 4:
                    population.append(
                        Person(canvas, size_canvas_x, random.uniform(100, size_canvas_y - 100),
                               2,
                               random.uniform(350, 370 % 360), random.randint(1, 11), 2))

    def check_distance(self):
        if len(population) >= 2:
            for element in population:
                if self != element:
                    distance = math.sqrt(((element.current_x_coord - self.current_x_coord) ** 2) + ((element.current_y_coord - self.current_y_coord) ** 2))
                    if distance <= 80:
                        if element not in self.distance_log.keys():
                            self.distance_log[element] = time.process_time()
                    else:
                        if element in self.distance_log.keys():
                            self.distance_log.pop(element)

    def clear_deleted(self):
        list_el = list(self.distance_log.keys())
        for element in list_el:
            if element not in population:
                self.distance_log.pop(element)

    def infect(self):
        if len(population) >= 2:
            for element in population:
                if self != element:
                    if element in self.distance_log.keys():
                        time_diff = abs(self.distance_log[element] - time.process_time())
                        if time_diff >= 3:
                            element.infected = True
                            element.time_of_infection = time.process_time()
                            self.canvas.itemconfig(element.ball, fill='red')


if __name__ == "__main__":
    # not_infecting = NotInfectedState()
    # infecting = InfectedState()
    # immune = ImmuneState()

    population = [
        Person(canvas, random.uniform(10, size_canvas_x - 10), random.uniform(10, size_canvas_y - 10),
               random.uniform(1, 2.5),
               random.uniform(0, 360), random.randint(1, 11)) for _ in range(x)]

    while app_running:
        if app_running:
            window.update_idletasks()
            for pers in population:
                pers.move_ball()
                pers.delete_if_off_screen()
                pers.create_new_if_needed()
                pers.check_distance()
                pers.clear_deleted()
                pers.infect()
            print(len(list_ids))
            window.update()

        # time.sleep(0.005)
        # print(time.process_time())
