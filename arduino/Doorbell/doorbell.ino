#include <ESP8266WiFi.h>

int INDICATOR_PIN = D0;
int RELAY_PIN     = D8;
int PULLDOWN_PIN  = D7;

int BUFFER_SIZE  = 256;
int READ_TIMEOUT = 250;

int RING_LEN    = 1000;

int MORSE_SCALER = 150;

// just change the scaler - these are apparently official guidelines

int DIT_LEN = 1 * MORSE_SCALER;
int DAH_LEN = 3 * MORSE_SCALER;
int PROSIGN_INTERVAL = 1 * MORSE_SCALER;
int CHAR_INTERVAL = 3 * MORSE_SCALER;
int WORD_INTERVAL = 7 * MORSE_SCALER;

enum Prosign {
  DIT,
  DAH,
  END
};

typedef enum Prosign Prosign;
typedef Prosign* MorseChar;

char* WIFI_SSID = "Matt LANcock";
char* WIFI_PASS = "quoththeravennevermore";

Prosign A[] = {DIT, DAH, END};
Prosign B[] = {DAH, DIT, DIT, DIT, END};
Prosign C[] = {DAH, DIT, DAH, DIT, END};
Prosign D[] = {DAH, DIT, DIT, END};
Prosign E[] = {DIT, END};
Prosign F[] = {DIT, DIT, DAH, DIT, END};
Prosign G[] = {DAH, DAH, DIT, END};
Prosign H[] = {DIT, DIT, DIT, DIT, END};
Prosign I[] = {DIT, DIT, END};
Prosign J[] = {DIT, DAH, DAH, DAH, END};
Prosign K[] = {DAH, DIT, DAH, END};
Prosign L[] = {DIT, DAH, DIT, DIT, END};
Prosign M[] = {DAH, DAH, END};
Prosign N[] = {DAH, DIT, END};
Prosign O[] = {DAH, DAH, DAH, END};
Prosign P[] = {DIT, DAH, DAH, DIT, END};
Prosign Q[] = {DAH, DAH, DIT, DAH, END};
Prosign R[] = {DIT, DIT, DAH, END};
Prosign S[] = {DIT, DIT, DIT, END};
Prosign T[] = {DAH, END};
Prosign U[] = {DIT, DIT, DAH, END};
Prosign V[] = {DIT, DIT, DIT, DAH, END};
Prosign W[] = {DIT, DAH, DAH, END};
Prosign X[] = {DAH, DIT, DIT, DAH, END};
Prosign Y[] = {DAH, DIT, DAH, DAH, END};
Prosign Z[] = {DAH, DAH, DIT, DIT, END};

MorseChar morseAlphabet[] = {
  A, B, C, D, E, F, G, H, I, J, K,
  L, M, N, O, P, Q, R, S, T, U,
  V, W, X, Y, Z
};

WiFiServer server(42069);

void setupBILED() {
  pinMode(INDICATOR_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
}

void biledOff() {
  digitalWrite(INDICATOR_PIN, HIGH);
  
}

void biledOn(){
  digitalWrite(INDICATOR_PIN, LOW);
  
}

void bellOn() {
  digitalWrite(RELAY_PIN, HIGH);
}

void bellOff() {
  digitalWrite(RELAY_PIN, LOW);
}

void flashBILED(int durationMs) { // duration in ms
  biledOn();
  delay(durationMs);
  biledOff();
}

void flashBell(int durationMs) {
  bellOn();
  delay(durationMs);
  bellOff();
}

void flashBILEDAndBell(int durationMs) {
  bellOn();
  biledOn();
  delay(durationMs);
  bellOff();
  biledOff();  
}

void dividedFlashBILED(int divisor, int totalDurationMs) {
  
  int flashDurationMs = totalDurationMs / (divisor * 2);

  for (int i = 0; i < divisor; i++) {
    flashBILED(flashDurationMs);
    delay(flashDurationMs);
  }

}

void connectToNetwork(char* ssid, char* password, int checkDelayMs) {

  WiFi.begin(ssid, password);

  wl_status_t connectionStatus = WiFi.status();

  while (connectionStatus != WL_CONNECTED) {

    switch(connectionStatus) {
      
      case WL_NO_SHIELD: // compatibility thing - shouldn't occur
        dividedFlashBILED(1, checkDelayMs);
        break;
        
      case WL_IDLE_STATUS: // changing between statuses
        dividedFlashBILED(2, checkDelayMs);
        break;
        
      case WL_NO_SSID_AVAIL: // can't find SSID
        dividedFlashBILED(3, checkDelayMs);
        break;
        
      case WL_SCAN_COMPLETED: // shouldn't occur here
        dividedFlashBILED(4, checkDelayMs);
        break;
        
      case WL_CONNECT_FAILED: // incorrect password
        dividedFlashBILED(5, checkDelayMs);
        break;
        
      case WL_CONNECTION_LOST: // connection lost/ waiting to connect
        dividedFlashBILED(6, checkDelayMs);
        break;
        
      case WL_DISCONNECTED: // not in station mode
        dividedFlashBILED(7, checkDelayMs);
        break;
        
    }

    delay(checkDelayMs);

    connectionStatus = WiFi.status();
    
  }
  
}

void toMorse(char* plaintext, int len, Prosign** morseBuffer) {

  for (int i = 0; i < len; i++) {
    morseBuffer[i] = morseAlphabet[plaintext[i] - 'a'];
  }
    
}

void playProsign(Prosign prosign) {

  switch (prosign) {

    case DIT:
      Serial.println(" - Ringing DIT");
      flashBILEDAndBell(DIT_LEN);
      break;
      
    case DAH:
      Serial.println(" - Ringing DAH");
      flashBILEDAndBell(DAH_LEN);
      break;
    
  }
      
}

void playMorseChar(MorseChar morseChar) {

  Serial.println("Ringing morse char:");

  int i = 0;

  while (morseChar[i] != END) {
    playProsign(morseChar[i]);
    delay(PROSIGN_INTERVAL);
    i++;
  }
    
}

void playMorseMessage(MorseChar* morseMessage, int len) {

  for (int i = 0; i < len; i++) {
    playMorseChar(morseMessage[i]);
    delay(CHAR_INTERVAL);
  }
    
}

void setup() {
  
  Serial.begin(115200); // this is set in the firmware we've installed

  Serial.println("Starting...");
  Serial.flush();
  
  setupBILED();

  Serial.printf("Attempting to connect to %s...", WIFI_SSID);
  Serial.flush();
  
  connectToNetwork(WIFI_SSID, WIFI_PASS, 2000); // blocks until success
  
  Serial.print("This device's IP is ");
  Serial.println(WiFi.localIP());

  Serial.println("Starting server...");
  server.begin();
  Serial.println("Listening...");
  
}

void readString(WiFiClient client) {
}

void handleRequest(WiFiClient client) {
}

char toLower(char c) {
  
  if (isUpperCase(c)) {
    return c - 'A' + 'a';
  }

  return c;
  
}

void ring() {
  Serial.println("Normal ring");
  flashBILEDAndBell(RING_LEN);
}

int blockingReadChar(WiFiClient client) {
  
  char c;
  
  if (client.readBytes(&c, sizeof(char)) > 0) { // read() doesn't block and we need blocking innit
    return c;
  }

  else {
    return -1;
  }

  return c;
  
}

void stopClient(WiFiClient client) {
      
//      delay(500);
      client.stop();
//      delay(500);
      
      Serial.println("Disconnected from client");
}

void loop() {

  WiFiClient client = server.available();

  if (client) {
    
    Serial.print("New connection from ");
    Serial.println(client.remoteIP());

    client.setTimeout(READ_TIMEOUT);

    int bufferSize = 8;
    char buffer[bufferSize];

    int count = 0;
    int readChar;


    while (count < bufferSize) {

      readChar = blockingReadChar(client);
      Serial.printf("Read %d ('%c'), ", readChar, readChar);
      
      if (readChar > 0) {

        if (isAlpha(readChar)) {

          readChar = toLower(readChar);
          buffer[count] = readChar;
          Serial.printf("put '%c' into ring buffer", readChar);
          count++;
          
        }

        Serial.println("");
        
      }

      else {
        break;
        Serial.println("None");
      }        
      
    }

    Serial.println("");

    if (count == 0) {
      Serial.println("Normal ring");
      client.println("ring");
      stopClient(client);
      ring();
    }

    else {

      char toPrint[count+1];
      toPrint[count] = 0;

      for (int i = 0; i < count; i++) {
        toPrint[i] = buffer[i];
      }

      client.println(toPrint);
      stopClient(client);
      
      Serial.printf("About to play \"%s\"\n", toPrint);
      
      MorseChar morseBuffer[count];
      toMorse(buffer, count, morseBuffer);
      playMorseMessage(morseBuffer, count);
      
    }

    Serial.println("Listening...");
    
  }
  
}
