# CODIGO DE LA APLICACION ROCKET TESTER APP PARA EL ENSAYO DE MOTORES COHETE

import  tkinter as      tk
from    tkinter import  ttk
from    tkinter import  scrolledtext

import  matplotlib.pyplot                   as plt
from    matplotlib.backends.backend_tkagg   import FigureCanvasTkAgg
from    matplotlib.figure                   import Figure

import  numpy as np
import  pandas as pd
import  datetime
import  time
import  serial

# BUCLE PRINCIPAL PARA LA RECOLECCION DE DATOS
# MAIN LOOP FOR DATA RECORDING

def start_loop():

    try:                                                    # Se intentara conectar con el puerto seleccionado. 
        port = serial.Serial(input_port, 9600)             
        check_label.config(text='MODULE CONNECTED')
        port.readline()
        time.sleep(2)                                       # Esto ayuda a estabilizar la conexion con el puerto.
    except:                                                 # Si se da cualquier error la funcion se para.
        check_label.config(text='NO CONNEXION')
        return

    text_box.delete(1.0, tk.END)                            # Se reinicia el cuadro de texto para que aparezcan los nuevos resultados.

    port.write(b'1')                                        # Sennal de activacion del rele para armar el motor.
    time.sleep(1)
                                                            
    i = 0                                                   # Se definen las listas de datos.
    iterations = []     
    thrust_Lecture = []
    temp1_Lecture = []
    temp2_Lecture = []
    press_lecture = []
    times = []

    running_label.config(text='SAMPLING')                   # Configuraciones para los cuadros de informacion.
    armed_label['text'] = 'IGNITION\nREADY'
    armed_label.config(bg='red',fg='white')
    

    global is_running                                       # La variable global is_running mantiene el bucle activo para seguir grabando.
    is_running = True

    while is_running:
        
        line = port.readline()                              # Lectura de la linea del puerto serial de Arduino. 
        
        if i == 5:                                          # Se dejan unas pocas iteraciones para estabilizar la medida.
            
            startingTime = time.time()
            text_box.delete(1.0, tk.END)


        if i > 5:      

            thrustLine = line[line.find(b'W')+1:line.find(b'C')].decode()
            temp1Line = line[line.find(b'C')+1:line.find(b'N')].decode()
            temp2Line = line[line.find(b'N')+1:line.find(b'\r')].decode()
                   
            thrustRead = float(thrustLine)/1000
            temp1Read = float(temp1Line) + 273.15
            temp2Read = float(temp2Line) + 273.15 
            pressRead = 0                                        

            iterations.append(i-5)
            thrust_Lecture.append(thrustRead)
            temp1_Lecture.append(temp1Read)
            temp2_Lecture.append(temp2Read)
            press_lecture.append(pressRead)
            times.append(np.round(time.time() - startingTime, 3))
            
            text_box.insert(tk.END,                         # Se formatea y muestra por pantalla los resultados en la caja de texto.                                  
                'IT'        + str(i-5)                                      + '\t' + 
                't(s) = '   + str('{:.3f}'.format(times[-1]))               + '\t' + 
                'F(kg) = '  + str('{:.4f}'.format(thrust_Lecture[-1]))      + '\t' +
                'T1(K) = '  + str('{:.4f}'.format(temp1_Lecture[-1]))       + '\t' +
                'T2(K) = '  + str('{:.4f}'.format(temp2_Lecture[-1]))       + '\t' +
                'P(Pa) = '  + '0'                                           + '\t' +
                '\n')
            text_box.see(tk.END)
            root.update()

        i += 1

    port.write(b'0')                                        # Sennal de desactivacion del rele.
    time.sleep(1)

    # CONFIGURACION DE LA GRAFICA DE EMPUJE DESPUES DE GRABAR LOS DATOS

    thrust_plot = Figure()
    thrust_plot.set_figheight(2.5)
    thrust_ax = thrust_plot.add_subplot(111)
    thrust_ax.plot(times,thrust_Lecture)
    thrust_ax.grid(True, linestyle='--', color='lightgray')
    thrust_ax.set_xlabel('Time (s)')
    thrust_ax.set_ylabel('Thrust (kg)')
    thrust_plot.tight_layout()
    canvas = FigureCanvasTkAgg(thrust_plot, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=2, sticky="nsew")

    # CONFIGURACION DE LA GRAFICA DE TEMPERATURA DESPUES DE GRABAR LOS DATOS

    temp_plot = Figure()
    temp_plot.set_figheight(2.5)
    temp_ax = temp_plot.add_subplot(111)
    temp_ax.plot(times,temp1_Lecture, label='T1')
    temp_ax.plot(times,temp2_Lecture, label='T2')
    temp_ax.legend(loc='upper right')
    temp_ax.grid(True, linestyle='--', color='lightgray')
    temp_ax.set_xlabel('Time (s)')
    temp_ax.set_ylabel('Temperature (K)')
    temp_plot.tight_layout()
    canvas = FigureCanvasTkAgg(temp_plot, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=2, sticky="nsew")

    # CONFIGURACION DE LA GRAFICA DE PRESION DESPUES DE GRABAR LOS DATOS

    press_plot = Figure()
    press_plot.set_figheight(2.5)
    press_ax = press_plot.add_subplot(111)
    press_ax.plot(times,press_lecture)
    press_ax.grid(True, linestyle='--', color='lightgray')
    press_ax.set_xlabel('Time (s)')
    press_ax.set_ylabel('Pressure (Pa)')
    press_plot.tight_layout()
    canvas = FigureCanvasTkAgg(press_plot, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=2, sticky="nsew")

    # RESULTADOS PARA EXPORTAR

    results = pd.DataFrame(list(zip(iterations, times, thrust_Lecture, temp1_Lecture, temp2_Lecture, press_lecture)),columns=['IT', 't(s)', 'F(kg)', 'T1(K)', 'T2(K)', 'P(pa)'])               
    now = datetime.datetime.now()
    results.to_csv('TestsFiles\\test_'+ now.strftime('%H_%M') +'.csv', index=False)

    # SE VUELVE A REINICIAR LAS ETIQUETAS DE INFORMACION PARA INDICAR EL CESE DE LA GRABACION Y SE CIERRA LA CONEXION CON EL PUERTO

    armed_label['text'] = 'CHECK LIST\nPROCEDURE'
    armed_label.config(bg='green',fg='white')
    port.close()

    
# FUNCION PARA PARAR EL BUCLE PRINCIPAL Y CAMBIAR INFORMACION DE CUADROS INDICATIVOS 

def stop_loop():    
    global is_running
    is_running = False
    running_label.config(text="DATA SAMPLING STOPPED")
    running_label.config(font=('Arial', 20, 'bold'))

    
# CONFIGURACION GRAFICA DE LA APP

root = tk.Tk()
screenWidth = root.winfo_screenwidth()/1.1
screenHeight = root.winfo_screenheight()/1.1
root.geometry("%dx%d" % (screenWidth,screenHeight))
root.title("Rocket tester App")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)


# FUNCION PARA OBTENER LA ID DEL PUERTO

def get_port(event):
    global input_port
    input_port = port_combobox.get()

input_port = ""                                         # Inicializacion de la Variable.
ports = ["COM" + str(i) for i in range(0, 257)]          # Creacion de la lista de puertos.

port_combobox = ttk.Combobox(root, values=ports)        # Creacion de la lista desplegable de puertos.
port_combobox.grid(row=0, column=0, sticky='nwse')      
port_combobox.config(font=('Arial', 20))
port_combobox.bind("<<ComboboxSelected>>", get_port)
port_combobox.focus_set()


# CONFIGURACION DE ETIQUETAS INDICATIVAS.

check_label = tk.Label(root, text="CONNECTING...")
check_label.grid(row=0, column=1, sticky='nwse')
check_label.config(font=('Arial', 20, 'bold'))

running_label = tk.Label(root, text="DATA SAMPLING STOPPED")
running_label.grid(row=0, column=2, sticky='nwse')
running_label.config(font=('Arial', 20, 'bold'))

armed_label = tk.Label(root, text='CHECK LIST\nPROCEDURE',bg='green',fg='white')
armed_label.grid(row=3, column=0, sticky='nwse')
armed_label.config(font=('Arial', 30, 'bold'))


# CONFIGURACION DE BOTONES

start_button = tk.Button(root, text='Read\nSensors', command=start_loop)
start_button.grid(row=1, column=0, sticky='nwse')
start_button.config(font=('Arial', 30, 'bold'))

stop_button = tk.Button(root, text='Stop\nReading', command=stop_loop)
stop_button.grid(row=2, column=0, sticky='nwse')
stop_button.config(font=('Arial', 30, 'bold'))


# CONFIGURACION DE LA CAJA DE TEXTO

text_box = scrolledtext.ScrolledText(root, height=20, width=90)
text_box.grid(row=1, column=1, rowspan=3, sticky="nsew")


# INICIALIZACION DE LAS GRAFICAS

thrust_plot = Figure()
thrust_plot.set_figheight(2.5)
thrust_ax = thrust_plot.add_subplot(111)
thrust_ax.plot(0,0)
thrust_ax.grid(True, linestyle='--', color='lightgray')
thrust_ax.set_xlabel('Time (s)')
thrust_ax.set_ylabel('Thrust (kg)')
thrust_plot.tight_layout()
canvas = FigureCanvasTkAgg(thrust_plot, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=2, sticky="nsew")

temp_plot = Figure()
temp_plot.set_figheight(2.5)
temp_ax = temp_plot.add_subplot(111)
temp_ax.plot(0,0)
temp_ax.grid(True, linestyle='--', color='lightgray')
temp_ax.set_xlabel('Time (s)')
temp_ax.set_ylabel('Temperature (K)')
temp_plot.tight_layout()
canvas = FigureCanvasTkAgg(temp_plot, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=2, column=2, sticky="nsew")

press_plot = Figure()
press_plot.set_figheight(2.5)
press_ax = press_plot.add_subplot(111)
press_ax.plot(0,0)
press_ax.grid(True, linestyle='--', color='lightgray')
press_ax.set_xlabel('Time (s)')
press_ax.set_ylabel('Pressure (Pa)')
press_plot.tight_layout()
canvas = FigureCanvasTkAgg(press_plot, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=3, column=2, sticky="nsew")





root.mainloop() # INICIA LA VENTANA GRAFICA DE USUARIO. 
