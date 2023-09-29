#include <ESP8266WiFi.h>
// #include <WiFi.h> // Descomente esta linha se estiver usando ESP32

const char *ssid = "ESP_SERVER";
const int serverPort = 8080;
const int maxChunkSize = 1024; // Tamanho máximo de cada parte em bytes

WiFiServer server(serverPort);

void setup()
{
  Serial.begin(9600);

  // Configurando o ESP como ponto de acesso
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.begin();
}

void loop()
{
  WiFiClient client = server.available();
  if (client)
  {
    Serial.println("Cliente conectado");
    if (client.connected())
    {
      String request = client.readStringUntil('\r');
      client.flush();

      int requestedSize = 0;
      Serial.print("Request: ");
      Serial.println(request);
      int index = request.indexOf("GET /file?size=");
      int fileSizeRequested = request.substring(index + 15).toInt();
      Serial.print("File size request: ");
      Serial.println(fileSizeRequested);

      if (fileSizeRequested > 0)
      {
        // client.println("HTTP/1.1 200 OK");
        // client.println("Content-Type: text/plain");
        // client.println("Connection: close");
        // client.print("Content-Length: ");
        // client.println(requestedSize);
        // client.println();

        for (int i = 0; i < fileSizeRequested * 1024; i++)
        {
          client.print("A"); // Conteúdo do arquivo (caractere 'A' repetido)

          delay(10); // Pequena pausa para evitar sobrecarga
        }
      }
    }
    client.stop();
    Serial.println("Cliente desconectado");
  }
}
