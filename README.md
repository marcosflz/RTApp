# RTApp
UI to monitor data from a test platform for rocket engines.

This project was developed during my degree´s final thesis which consisted of a comparision between the analytical, simulated and experimental procedures of rocket engine noozles. This app consits of a user interface where you can see in real time how the data is been collected. Once the test is completed you can stop the sensors reading and all the results will be written and exported to a csv file. It will also show 3 graphics with variable-time charts so you can have a quickview of the results. 

The app works with the serial comunication between python and an arduino nano to which all the sensors are conected. The arduino itself has its own code as well so it ensures the correct print to serial of the data collected from the sensors. It also has a port comunication list to select the activated one in each PC.

The modules connected to the protoboard and which are used in the .ino code are the HX711 amplificator for the Load Cell and the MAX6675 thermocouple amplificator. The pressure sensor was initially planned to be installed but due to logistic and lack of time issues it wasn´t included. On the other hand the RTApp code includes the pressure section for data collection and chart printing so in the future if this system is neede again it can be updated easily.


![alt text](https://github.com/marcosflz/RTApp/blob/main/Images/RApp_Results.png)
![alt text](https://github.com/marcosflz/RTApp/blob/main/Images/EsquemaConexiones.jpg)
![alt text](https://github.com/marcosflz/RTApp/blob/main/Images/CajaProtoboardREAL_Abierta.jpg)
![alt text](https://github.com/marcosflz/RTApp/blob/main/Images/Ensayo7.jpg)
