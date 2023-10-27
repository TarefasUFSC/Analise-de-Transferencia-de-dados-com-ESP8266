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

    Serial.print("CONNECTING");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);

        Serial.print(".");
    }
    Serial.println("\nCONNECTED");
}

void loop()
{
    // limpa o buffer do serial monitor
    while (Serial.available())
    {
        Serial.read();
    }
    Serial.println("FILE SIZE (Bytes):");
    while (!Serial.available())
    {
        delay(10);
    }
    int requestedFileSizeB = Serial.parseInt();
    if (requestedFileSizeB == 0)
        return;
    Serial.println("Solicitando arquivo de " + String(requestedFileSizeB) + " Bytes...");

    if (client.connect(serverIP, serverPort))
    {
        unsigned long startTime = millis();

        client.println("GET /file?size=" + String(requestedFileSizeB) + " HTTP/1.1");

        int bytesRead = 0;

        long timeout = millis() + 600000; // Define um timeout de 600 segundos
        bool received = false;

        // clear buffer
        client.flush();

        while (millis() < timeout && bytesRead < requestedFileSizeB)
        {
            while (client.available())
            {
                received = true;
                char c = client.read();
                bytesRead++;
            }
        }

        unsigned long endTime = millis();
        unsigned long duration = endTime - startTime;

        Serial.print("SUCCESS;");
        Serial.print("Size:");
        Serial.print(bytesRead);
        Serial.print(" bytes;");
        Serial.print("Duration:");
        Serial.print(duration);
        Serial.println(" ms");
        client.stop();
    }
    else
    {
        Serial.println("ERROR: Falha de Conexão com o Servidor");
    }
}
