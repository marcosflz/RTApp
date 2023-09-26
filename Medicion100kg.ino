# include <Arduino .h>
# include " HX711 .h"
# include " max6675 .h"
# define cellPin A0

// HX711
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
HX711 scale ;

// Relay
const int RELAY_PIN = 4;

// MAX6675
int i = 0;

int thermoDO_1 = 5;
int thermoCS_1 = 6;
int thermoCLK_1 = 7;
float itTemp_1 ;

int thermoDO_2 = 10;
int thermoCS_2 = 11;
int thermoCLK_2 = 12;
float itTemp_2 ;

MAX6675 pressure_chamber( thermoCLK_1 , thermoCS_1 , thermoDO_1);
MAX6675 exit_nozzle( thermoCLK_2 , thermoCS_2 , thermoDO_2);


void setup() {

Serial.begin(9600);
Serial.setTimeout(1);

Serial. println(" HX711 ");
scale.begin( LOADCELL_DOUT_PIN , LOADCELL_SCK_PIN );
scale.set_scale( -45.57692308);
scale.tare();

Serial.println(" MAX6675 test ");
itTemp_1 = pressure_chamber.readCelsius();
itTemp_2 = exit_nozzle.readCelsius();
delay(500) ;

pinMode( RELAY_PIN , OUTPUT );
digitalWrite( RELAY_PIN , LOW );

}

void loop() {

    Serial . print("W");
    Serial . print( scale . get_units() , 5) ;

    if(i <= 2) {
        Serial . print("C");
        Serial . print( itTemp_1 );
        Serial . print("N");
        Serial . println( itTemp_2 );
    }

    if(i > 2) {
        itTemp_1 = pressure_chamber.readCelsius() ;
        itTemp_2 = exit_nozzle.readCelsius() ;
        Serial.print("C");
        Serial.print( itTemp_1 );
        Serial.print("N");
        Serial.println( itTemp_2 );
        i = 0;
    }

    i = ++ i;

    while( Serial . available() > 0) {
        // Lee el caracter recibido
        char cmd = Serial . read() ;
        // Si el caracter es '1', enciende el rele
        if( cmd == '1') {
            digitalWrite( RELAY_PIN , HIGH ) ;
        }
        // Si el caracter es '0', apaga el rele
        else if( cmd == '0') {
            digitalWrite( RELAY_PIN , LOW );
        }
    }
}