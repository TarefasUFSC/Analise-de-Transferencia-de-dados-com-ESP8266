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

    Serial.print("Conectando ao WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);

        Serial.print(".");
    }
    Serial.println("\nConectado ao WiFi");
}

void loop()
{
    Serial.println("Digite o tamanho do arquivo que você deseja (em Bytes):");
    while (!Serial.available())
    {
        delay(10);
    }
    int requestedFileSizeB = Serial.parseInt();
    if (requestedFileSizeB == 0)
        return;
    // Serial.println("Solicitando arquivo de " + String(requestedFileSizeB) + " Bytes...");

    if (client.connect(serverIP, serverPort))
    {
        // Serial.println("Conectado ao servidor");

        unsigned long startTime = millis();

        client.println("GET /file?size=" + String(requestedFileSizeB) + " HTTP/1.1");

        int bytesRead = 0;
        Serial.println();

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
                // Serial.print(c);
            }
        }

        Serial.println();

        unsigned long endTime = millis();
        unsigned long duration = endTime - startTime;

        // Serial.println("Arquivo recebido!");
        // Serial.print("Tamanho do arquivo: ");
        // Serial.print(bytesRead);
        // Serial.println(" bytes");
        Serial.print("Tempo de transferência: ");
        Serial.print(duration);
        Serial.println(" ms");

        client.stop();
    }
    else
    {
        Serial.println("Falha na conexão ao servidor");
    }
}
