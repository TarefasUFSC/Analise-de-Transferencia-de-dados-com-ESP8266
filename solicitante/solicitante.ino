#include <ESP8266WiFi.h>
// #include <WiFi.h> // Descomente esta linha se estiver usando ESP32

const char *ssid = "ESP_SERVER";
const int serverPort = 8080;
const char *serverIP = "192.168.4.1"; // IP padrão do ESP quando atua como AP

WiFiClient client;

void setup()
{
    Serial.begin(9600);
    WiFi.begin(ssid); // Conectando-se ao AP "ESP_SERVER"

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Conectando ao WiFi...");
    }
    Serial.println("Conectado ao WiFi");
}

void loop()
{
    Serial.println("Digite o tamanho do arquivo que você deseja (em KB):");
    while (!Serial.available())
    {
        delay(10);
    }
    int requestedFileSizeKB = Serial.parseInt();
    if(requestedFileSizeKB == 0) return;
    Serial.println("Solicitando arquivo de " + String(requestedFileSizeKB) + " KB...");

    if (client.connect(serverIP, serverPort))
    {
        Serial.println("Conectado ao servidor");

        unsigned long startTime = millis();

        client.println("GET /file?size=" + String(requestedFileSizeKB) + " HTTP/1.1");

        int bytesRead = 0;
        Serial.println();
        
      long timeout = millis() + 50000;  // Define um timeout de 5 segundos
      bool received = false;
      while (millis() < timeout && requestedFileSizeKB*1024>bytesRead) {
        while (client.available())
        {
            received = true;
            char c = client.read();
            bytesRead++;
            Serial.print(".");
        }
      }
        
        Serial.println();

        unsigned long endTime = millis();
        unsigned long duration = endTime - startTime;

        Serial.println("Arquivo recebido!");
        Serial.print("Tamanho do arquivo: ");
        Serial.print(bytesRead);
        Serial.println(" bytes");
        Serial.print("Tempo de transferência: ");
        Serial.print(duration);
        Serial.println(" ms");

        client.stop();
    }
    else
    {
        Serial.println("Falha na conexão ao servidor");
    }
    delay(5000);
}
