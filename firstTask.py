from tkinter import *
import math


# вычисление значения функции
def func(x):
    # return x*x
    # return x
    return x*math.sin(x*x)


# нахождение максимального и минимального значения функции
def max_min():
    ymin = ymax = func(a)
    for xx in range(800):
        x = a + xx*(b - a)/800
        y = func(x)
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    return ymin, ymax


# вычисление у по х, масштабирование
def calculate(xx, flag):

    x = a + xx*(b - a)/800
    y = func(x)
    yy = (y - ymax)*800/(ymin - ymax)
    if y < 0:
        flag[1] = True
    if y > 0:
        flag[2] = True
    if y == 0:
        flag[0] = True
        flag[3] = yy
    return yy, flag


# поиск координаты х для отрисовки оси ОУ, отрисовка
def find_ordinate_coord():
    drawn_axis_OY = False
    if a == 0:
        canvas.create_line(0, 800, 0, 0, fill="black", arrow=LAST)
        drawn_axis_OY = True
    else:
        for xx in range(800):
            x = a + xx * (b - a) / 800
            if (x == 0) and (drawn_axis_OY is False):
                canvas.create_line(xx, 800, xx, 0, fill="black", arrow=LAST)
                drawn_axis_OY = True
            if x > 0:
                x_old = a + (xx - 1) * (b - a) / 800
                if (0 - x_old < x) and (drawn_axis_OY is False):
                    canvas.create_line(xx - 1, 800, xx - 1, 0, fill="black", arrow=LAST)
                    drawn_axis_OY = True
                elif drawn_axis_OY is False:
                    canvas.create_line(xx, 800, xx, 0, fill="black", arrow=LAST)
                    drawn_axis_OY = True


# поиск координаты y для отрисовки оси ОX, отрисовка
def find_abscissa_coord(flag, y_min, y_max):
    if flag[0] is True:
        canvas.create_line(0, flag[3] + 2, 800, flag[3] + 2, fill="black", arrow=LAST)
    else:
        if (flag[1] is True) and (flag[2] is True):
            old_y = y_min
            diff = y_max - y_min
            for xx in range(800):
                x = a + xx * (b - a) / 800
                y = func(x)
                yy = (y - ymax) * 800 / (ymin - ymax)
                if (((old_y < 0) and (y > 0)) or ((old_y > 0) and (y < 0))) and (math.fabs(y - old_y) < diff):
                    yy_old = (old_y - ymax) * 800 / (ymin - ymax)
                    diff = math.fabs(old_y - y)
                    if math.fabs(old_y) < math.fabs(y):
                        coord = yy_old
                    else:
                        coord = yy
                old_y = y
            canvas.create_line(0, coord + 2, 800, coord + 2, fill="black", arrow=LAST)



def main():
    global ymin
    global ymax
    ymin, ymax = max_min()
    a = ymin
    yy = (func(a) - ymin)*800/(ymax - ymin)
    yy_old = yy
    # y = 0, y < 0, y > 0, yy(if y = 0)
    y_0_flag = [False, None, None, None]
    for xx in range(0, 800):
        yy, flag = calculate(xx, y_0_flag)
        canvas.create_line(xx, yy_old + 2, xx + 1, yy + 2, fill="#ff0000")

        # if yy == 0:
        #     print(yy, xx)
        #     canvas.create_line(0, 1, 800, 1, fill="green")

        yy_old = yy
        y_0_flag = flag
    find_ordinate_coord()
    find_abscissa_coord(y_0_flag, ymin, ymax)


if __name__ == "__main__":
    global a
    global b
    print("введите 2 числа:")
    a = int(input())
    b = float(input())
    root = Tk()
    canvas = Canvas(root, width=802, height=802, bg='white')
    canvas.pack()
    main()
    root.mainloop()



