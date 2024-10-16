struct Device {
  const byte pin;
  bool is_on;
};
// In the test. Low side relay is used, you may need to change the code logic
// Declare devices with pin numbers
Device fan = {8, true};
Device light = {9, true};
Device tv = {10, true};


/*

Switch mappings:
'A' == fan on
'a' == fan off

'B' == light on
'b' == light off

'C' == your_device on
'c' == your_device off

*/



void setup() {
  

  pinMode(fan.pin, OUTPUT);
  pinMode(light.pin, OUTPUT);
  pinMode(tv.pin, OUTPUT);
  digitalWrite(fan.pin, HIGH);
  digitalWrite(light.pin, HIGH);
  digitalWrite(tv.pin, HIGH);

  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for serial port to connect. Needed for native USB port only
  }
}
void loop() {
  fan.is_on = digitalRead(fan.pin);
  light.is_on = digitalRead(light.pin);
  tv.is_on = digitalRead(tv.pin);
  if (Serial.available()>0) {
    char ch = Serial.read();

    if (ch == 'A') { // for Turning on the fan
          if(!fan.is_on){ //check state
            Serial.write('X');
          }
          else{
            Serial.write(ch);
            digitalWrite(fan.pin, LOW);
          }
    }
    else if (ch == 'B') { //For Turning on the light
          if(!light.is_on){
            Serial.write('Y');
          }
          else{
            Serial.write(ch);
            digitalWrite(light.pin, LOW);
          }
    }
    else if (ch == 'C') { //For Turning on the tv
          if(!tv.is_on){
            Serial.write('Z');
          }
          else{
            Serial.write(ch);
            digitalWrite(tv.pin, LOW);
          }
    }
    else if (ch == 'a') { //For Turning off the fan

          if(fan.is_on){
            Serial.write('x');
          }
          else{
            Serial.write(ch);
            digitalWrite(fan.pin, HIGH);
          }

    }
    else if (ch == 'b') { //For Turning off the light

          if(light.is_on){
            Serial.write('y');
          }
          else{
            Serial.write(ch);
            digitalWrite(light.pin, HIGH);
          }
    }
    else if (ch == 'c') { //  your device

          if(tv.is_on){ 
            Serial.write('z');
          }
          else{
            Serial.write(ch);
            digitalWrite(tv.pin, HIGH);
          }
    }
}
}
