

```c++



// #define DECODE_NEC          // Includes Apple and Onkyo
#include <Arduino.h>
#include <IRremote.hpp>
#include <Adafruit_NeoPixel.h>

#define IR_RECEIVE_PIN  36

#define WS_PIN 17
#define WS_NUM 64

boolean color_en=false;

Adafruit_NeoPixel pixels(WS_NUM, WS_PIN, NEO_GRB+NEO_KHZ800);


void rainbow(int wait) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this loop:
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    // strip.rainbow() can take a single argument (first pixel hue) or
    // optionally a few extras: number of rainbow repetitions (default 1),
    // saturation and value (brightness) (both 0-255, similar to the
    // ColorHSV() function, default 255), and a true/false flag for whether
    // to apply gamma correction to provide 'truer' colors (default true).
    if(color_en) {
      pixels.rainbow(firstPixelHue);
      // Above line is equivalent to:
      // strip.rainbow(firstPixelHue, 1, 255, 255, true);
      pixels.show(); // Update strip with new contents
    }else {
      pixels.clear();
      pixels.show();
    }

    delay(wait);  // Pause for a moment
  }
}


void task_ws2812(void *pvParam) {
  while(true) {
    if(color_en) {
      rainbow(10);
      } else {
          pixels.clear();
          pixels.show();
          Serial.println("task_ws2812......");
          vTaskDelay(500/portTICK_PERIOD_MS);
        }
    } 
  }


void setup() {
    Serial.begin(115200);

    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);

    Serial.print(F("Ready to receive IR signals of protocols: "));
    printActiveIRProtocols(&Serial);
    Serial.print("接收来自引脚:D");
    Serial.println(IR_RECEIVE_PIN);


    pixels.begin();
    pixels.clear();
    pixels.show();

    xTaskCreate(task_ws2812, "task_ws2812", 1000, NULL, 1, NULL);

}

void loop() {

    if (IrReceiver.decode()) {

        // Print a short summary of received data
//        IrReceiver.printIRResultShort(&Serial);
        IrReceiver.printIRSendUsage(&Serial);
        if (IrReceiver.decodedIRData.protocol == UNKNOWN) {
            Serial.println(F("Received noise or an unknown (or not yet enabled) protocol"));
            // We have an unknown protocol here, print more info
            IrReceiver.printIRResultRawFormatted(&Serial, true);
        }
        Serial.println();

         // * !!!Important!!! Enable receiving of the next value,
         // * since receiving has stopped after the end of the current received data packet.
        IrReceiver.resume(); // Enable receiving of the next value

        switch (IrReceiver.decodedIRData.command)
        {
            case 0x45:
                Serial.println("1");

                  color_en=true;

                break;
            case 0x46:
                Serial.println("2");

                  color_en=false;
                break;
            case 0x47:
                Serial.println("3");
                break;
            case 0x44:
                Serial.println("4");
                break;
            case 0x40:
                Serial.println("5");
                break;
            case 0x43:
                Serial.println("6");
                break;
            case 0x07:
                Serial.println("7");
                break;
            case 0x15:
                Serial.println("8");
                break;
            case 0x09:
                Serial.println("9");
                break;
            case 0x16:
                Serial.println("*");
                break;
            case 0x19:
                Serial.println("0");
                break;
            case 0x0D:
                Serial.println("#");
                break;
            case 0x18:
                Serial.println("上");
                break;
            case 0x1C:
                Serial.println("OK");
                break;
            case 0x52:
                Serial.println("下");
                break;
            case 0x08:
                Serial.println("左");
                break;
            case 0x5A:
                Serial.println("右");
                break;

            default:
                Serial.println("没有这个键");
        }
    }
}



```
