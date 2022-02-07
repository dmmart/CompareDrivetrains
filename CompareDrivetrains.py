from tkinter import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

CASSETTE_FILE = 'cassettes.txt'
CHAINRING_FILE = 'cranksets.txt'

STANDARD = { "road": {'max_speed': 50, 'min_speed': 10, 'range': 300},
             "mtb": {'max_speed': 40, 'min_speed': 5, 'range': 400},
             "gravel": {'max_speed': 45, 'min_speed': 7, 'range': 350} }

root = Tk()
root.title('Drivetrain Comparison')
root.resizable(width=False, height=False)
app = Frame(root, pady=10)
app.pack(expand=1, fill=BOTH)

def read_file(filename):
    try:
        file = open(filename)
    except:
        print("File not found...")
        return
    
    doc = file.read().splitlines()
    file.close()
    for i in range(len(doc)):
        doc[i] = doc[i].split('-')
        doc[i] = [int(j) for j in doc[i]]
    return doc

def gear_ratios(cassette, crankset):
    temp = list()
    ratios = list()
    for i in crankset:
        for j in cassette:
            temp.append(round(i/j, 3))
    for i in temp:
        if i not in ratios:
            ratios.append(i)
    return sorted(ratios)

def str_to_int_list(string):
    string = string.strip('()')
    string = string.split(', ')
    
    for i in range(len(string)):
        if string[i].isdigit() == True:
            string[i] = int(string[i])
        else:
            string[i] = int(string[i].strip(','))
            
    return string

def gear_range(ratios):
    return int(round((ratios[len(ratios)-1]/ratios[0])*100, 0))

def speed(ratio, wheel_size, cadence, units = 'kph'):
    speed_mph = 0.002975*cadence*ratio*wheel_size
    if units == 'kph':
        return int(round(1.60934 * speed_mph, 0))
    else:
        return int(round(speed_mph, 0))

def average_step(ratios):
    steps = list()
    for i in range(len(ratios)-2):
        steps.append(round((ratios[i+1]/ratios[i]-1)*100, 2))
    average = round(sum(steps) / len(steps), 2)
    return average

def greater_than_15(ratios):
    steps = list()
    for i in range(len(ratios)-2):
        steps.append(round((ratios[i+1]/ratios[i]-1)*100, 2))
    
    counter = 0
    for i in steps:
        if i > 15.0:
            counter += 1
    return counter

def display_chart(gearRatios_1, gearRatios_2):
    #Plot
    fig, ax = plt.subplots()
    #index = np.arange(max(len(gearRatios_1), len(gearRatios_2)))
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(np.arange(len(gearRatios_1)), gearRatios_1, bar_width,
    alpha=opacity,
    color='#0088E3',
    label='Drivetrain 1')

    rects2 = plt.bar(np.arange(len(gearRatios_2)) + bar_width, gearRatios_2, bar_width,
    alpha=opacity,
    color='#B682C7',
    label='Drivetrain 2')
    
    plt.xlabel('Gear')
    plt.ylabel('Gear Ratios')
    plt.title('Drivetrain Comparison')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
def display_values(gearRatios, style, wheel_size, col):
    max_speed = speed(gearRatios[len(gearRatios)-1], wheel_size, 100)
    min_speed = speed(gearRatios[0], wheel_size, 50)
    gearRange = gear_range(gearRatios)
    avgStep = average_step(gearRatios)
    greaterThan15 = greater_than_15(gearRatios)
    
    if max_speed >= STANDARD[style]['max_speed']:
        max_speed_value = Label(app, text=str(max_speed) + " km/h", font=12, fg='#00E433')
        max_speed_value.grid(row=4, column=col, sticky=W)
    elif max_speed >= STANDARD[style]['max_speed'] * 0.85:
        max_speed_value = Label(app, text=str(max_speed) + " km/h", font=12, fg='#E3C700')
        max_speed_value.grid(row=4, column=col, sticky=W)
    else:
        max_speed_value = Label(app, text=str(max_speed) + " km/h", font=12, fg='red')
        max_speed_value.grid(row=4, column=col, sticky=W)
    
    if min_speed <= STANDARD[style]['min_speed']:
        min_speed_value = Label(app, text=str(min_speed) + " km/h", font=12, fg='#00E433')
        min_speed_value.grid(row=5, column=col, sticky=W)
    elif min_speed <= STANDARD[style]['min_speed'] * 1.15:
        min_speed_value = Label(app, text=str(min_speed) + " km/h", font=12, fg='#E3C700')
        min_speed_value.grid(row=5, column=col, sticky=W)
    else:
        min_speed_value = Label(app, text=str(min_speed) + " km/h", font=12, fg='red')
        min_speed_value.grid(row=5, column=col, sticky=W)
    
    if gearRange >= STANDARD[style]['range']:
        range_value = Label(app, text=str(gearRange) + "%", font=12, fg='#00E433')
        range_value.grid(row=6, column=col, sticky=W)
    elif gearRange >= STANDARD[style]['range'] * 0.85:
        range_value = Label(app, text=str(gearRange) + "%", font=12, fg='#E3C700')
        range_value.grid(row=6, column=col, sticky=W)
    else:
        range_value = Label(app, text=str(gearRange) + "%", font=12, fg='red')
        range_value.grid(row=6, column=col, sticky=W)
    
    if avgStep <= 15.0:
        avg_step_value = Label(app, text=str(avgStep) + "%", font=12, fg='#00E433')
        avg_step_value.grid(row=7, column=col, sticky=W)
    elif avgStep <= 15.0 * 1.15:
        avg_step_value = Label(app, text=str(avgStep) + "%", font=12, fg='#E3C700')
        avg_step_value.grid(row=7, column=col, sticky=W)
    else:
        avg_step_value = Label(app, text=str(avgStep) + "%", font=12, fg='red')
        avg_step_value.grid(row=7, column=col, sticky=W)
    
    if greaterThan15 == 0:
        greaterThan15_value = Label(app, text=str(greaterThan15), font=12, fg='#00E433')
        greaterThan15_value.grid(row=8, column=col, sticky=W)
    elif greaterThan15 < 5:
        greaterThan15_value = Label(app, text=str(greaterThan15), font=12, fg='#E3C700')
        greaterThan15_value.grid(row=8, column=col, sticky=W)
    else:
        greaterThan15_value = Label(app, text=str(greaterThan15), font=12, fg='red')
        greaterThan15_value.grid(row=8, column=col, sticky=W)


def show_calculations(gearRatios_1, gearRatios_2, style, wheel_size):
    max_speed_label = Label(app, text="Approximate max speed:", font=12)
    max_speed_label.grid(row=4, column=0, padx=20, columnspan=2, sticky=W)
    min_speed_label = Label(app, text="Approximate min speed:", font=12)
    min_speed_label.grid(row=5, column=0, padx=20, columnspan=2, sticky=W)
    range_label = Label(app, text="Drivetraine range:", font=12)
    range_label.grid(row=6, column=0, padx=20, columnspan=2, sticky=W)
    avg_step_label = Label(app, text="Average gear step:", font=12)
    avg_step_label.grid(row=7, column=0, padx=20, columnspan=2, sticky=W)
    greater_15_label = Label(app, text="Gear steps over 15%:", font=12)
    greater_15_label.grid(row=8, column=0, padx=20, columnspan=2, sticky=W)
    
    display_values(gearRatios_1, style, wheel_size, 2)
    display_values(gearRatios_2, style, wheel_size, 3)
    
    green_label = Label(app, text=" Excelent result ", font=("bold", 12), bg='#00E433')
    green_label.grid(row=9, column=0, pady=20, padx=20, sticky=W)
    
    yellow_label = Label(app, text=" Acceptable result ", font=("bold", 12), bg='#E3C700')
    yellow_label.grid(row=9, column=0, pady=20, columnspan=4)
    
    red_label = Label(app, text=" Bad result ", font=("bold", 12), bg='red')
    red_label.grid(row=9, column=3, pady=20, padx=20, sticky=E)
    

def clicked_button():
    style = clicked_ridingStyle.get()
    size = clicked_wheelSize.get()
    cassette_1 = str_to_int_list(clicked_cassette_1_drop.get())
    chainring_1 = str_to_int_list(clicked_crankset_1_drop.get())
    cassette_2 = str_to_int_list(clicked_cassette_2_drop.get())
    chainring_2 = str_to_int_list(clicked_crankset_2_drop.get())
    
    gearRatios_1 = gear_ratios(cassette_1, chainring_1)
    gearRatios_2 = gear_ratios(cassette_2, chainring_2)
    
    show_calculations(gearRatios_1, gearRatios_2, style, size)
    
    display_chart(gearRatios_1, gearRatios_2)

''' MAIN '''

frame_1 = Frame(app, padx=20)
frame_1.grid(row=1, column=0, columnspan=2, sticky=W+E)
frame_2 = Frame(app, padx=20)
frame_2.grid(row=1, column=2, columnspan=2, sticky=W+E)

ridingStyle_options = ["road","mtb","gravel"]
crankset_options = read_file(CHAINRING_FILE)
cassette_options = read_file(CASSETTE_FILE)
wheelSize_options = [26.0,27.5,28.0,29.0]

# datatype of menu text
clicked_ridingStyle = StringVar()
clicked_crankset_1_drop = StringVar()
clicked_cassette_1_drop = StringVar()
clicked_wheelSize = DoubleVar()
clicked_crankset_2_drop = StringVar()
clicked_cassette_2_drop = StringVar()

# initial menu text
clicked_ridingStyle.set(ridingStyle_options[0])
clicked_crankset_1_drop.set(crankset_options[0])
clicked_cassette_1_drop.set(cassette_options[0])
clicked_wheelSize.set(wheelSize_options[0])
clicked_crankset_2_drop.set(crankset_options[0])
clicked_cassette_2_drop.set(cassette_options[0])

# Labels
riding_style_label = Label(frame_1, text="Choose a Riding Style:",font=12)
riding_style_label.grid(row=0, column=0, sticky=W)

wheelSize_label = Label(frame_2, text="Choose a Wheel Size:",font=12)
wheelSize_label.grid(row=0, column=0, sticky=W)

drivetrain1_label = Label(frame_1, text="Drivetrain 1", font=("bold", 16), fg='#0088E3')
drivetrain1_label.grid(row=1, column=0, columnspan=2, sticky=W)

crankset_1_label = Label(frame_1, text="Choose a Crankset:", font=12)
crankset_1_label.grid(row=2, column=0, sticky=W)

cassette_1_label = Label(frame_1, text="Choose a Cassette:", font=12)
cassette_1_label.grid(row=3, column=0, columnspan=2, sticky=W)

drivetrain2_label = Label(frame_2, text="Drivetrain 2", font=("bold", 16), fg='#B682C7')
drivetrain2_label.grid(row=1, column=0, columnspan=2, sticky=W)

crankset_2_label = Label(frame_2, text="Choose a Crankset:", font=12)
crankset_2_label.grid(row=2, column=0, sticky=W)

cassette_2_label = Label(frame_2, text="Choose a Cassette:", font=12)
cassette_2_label.grid(row=3, column=0, columnspan=2, sticky=W)

# Create Dropdown menus
ridingStyle_drop = OptionMenu(frame_1, clicked_ridingStyle , *ridingStyle_options)
ridingStyle_drop.grid(row=0, column=1, sticky=E)

wheelSize_drop = OptionMenu(frame_2, clicked_wheelSize , *wheelSize_options)
wheelSize_drop.grid(row=0, column=1, sticky=E)

crankset_1_drop = OptionMenu(frame_1, clicked_crankset_1_drop , *crankset_options)
crankset_1_drop.grid(row=2, column=1, sticky=W+E)

crankset_2_drop = OptionMenu(frame_2, clicked_crankset_2_drop , *crankset_options)
crankset_2_drop.grid(row=2, column=1, sticky=W+E)

cassette_1_drop = OptionMenu(frame_1, clicked_cassette_1_drop , *cassette_options )
cassette_1_drop.grid(row=4, column=0, columnspan=2, sticky=W+E)

cassette_2_drop = OptionMenu(frame_2, clicked_cassette_2_drop , *cassette_options )
cassette_2_drop.grid(row=4, column=0, columnspan=2, sticky=W+E)

#button
button = Button(app, text="Display Results", font = 20, command=clicked_button)
button.grid(row=3, column=0, sticky=W+E, columnspan=4, pady=20, padx=20)

# Execute tkinter
app.mainloop()