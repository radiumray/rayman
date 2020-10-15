```c++

void setup() {
  Serial.begin(115200);
}

void loop() {
    int value = pulseIn(7, HIGH);
    Serial.println(value);
    delay(20);
}


```
