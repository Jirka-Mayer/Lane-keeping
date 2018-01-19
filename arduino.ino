byte pwmPin = 7;
 
void setup() {
  pinMode(pwmPin, INPUT);
  Serial.begin(9600);
}
 
void loop() {
  Serial.println(String(pulseIn(pwmPin, HIGH), DEC));
  delay(50);
}
