#include <ESP8266WiFi.h>
// #include <WiFi.h> // Descomente esta linha se estiver usando ESP32

const char *ssid = "ESP_SERVER";
const int serverPort = 8080;

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
        for (int i = 0; i < fileSizeRequested; i++)
        {
          client.print("A"); // Conteúdo do arquivo (caractere 'A' repetido)
          Serial.print("A");
        }
      }
    }
    client.stop();
    Serial.println("\nCliente desconectado");
    delay(2000);
  }
}
