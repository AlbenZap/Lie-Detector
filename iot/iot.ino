

#define USE_ARDUINO_INTERRUPTS true   
#include <PulseSensorPlayground.h>       
#include <Adafruit_MLX90614.h>
#include <Wire.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
const int PulseWire = 0;
const int GSR=A1;
int sensorValue=0;
int gsr_average=0;            
int Threshold = 550;                                        
PulseSensorPlayground pulseSensor;

  
void setup() {   

  Serial.begin(9600);          
  mlx.begin();
  pulseSensor.analogInput(PulseWire); 
  pulseSensor.setThreshold(Threshold);   
 
   if (pulseSensor.begin()) {
    //Serial.println("We created a pulseSensor Object !");  
     long sum=0;
  for(int i=0;i<500;i++)           //Average the 10 measurements to remove the glitch
      {
      sensorValue=analogRead(GSR);
      sum += sensorValue;
      delay(5);
      }
   gsr_average = sum/10;
  }
}



void loop() {

  int myBPM = pulseSensor.getBeatsPerMinute();  
  float amb = mlx.readAmbientTempC();
  float obj = mlx.readObjectTempC();
  int temp;
  sensorValue=analogRead(GSR);
  
  temp = gsr_average - sensorValue;
  if(abs(temp)>60)
  {
    sensorValue=analogRead(GSR);
    temp = gsr_average - sensorValue;
    if(abs(temp)>60){

    //Serial.println("Emotion Changes Detected!");
    
 
    delay(1000);
  }
 }
   
  //Serial.print(amb);
  Serial.print(obj); Serial.print(" , ");
  Serial.print(myBPM); Serial.print(" , ");
  Serial.print(sensorValue); Serial.print("\n");
  
  delay(500);                  

}
