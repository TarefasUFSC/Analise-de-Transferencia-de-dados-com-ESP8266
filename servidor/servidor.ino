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
  WiFi.softAP(ssid,NULL,4);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.begin();
}

void handle_buffer(WiFiClient client, String outputBuffer, int *progress, int fileSizeRequested, int i)
{
  if (outputBuffer.length() >= 1024) // Enviar o buffer quando atingir um tamanho específico
  {
    client.print(outputBuffer);
    outputBuffer = "";
    if (100 * i / fileSizeRequested >= *progress + 5)
    {
      Serial.print("Progresso: ");
      Serial.println((int)(100 * i / fileSizeRequested));
      *progress = 100 * i / fileSizeRequested;
    }
  }
}

void send_data(WiFiClient client, int fileSizeRequested)
{
  // Bufferizando a saída para enviar vários caracteres de uma vez
  int progress = 0;

  Serial.println("Progresso: 0");
  if (fileSizeRequested > 0)
  {
    String outputBuffer = "";
    for (int i = 0; i < fileSizeRequested; i++)
    {
      outputBuffer += 'A'; // Conteúdo do arquivo (caractere 'A' repetido)
      handle_buffer(client, outputBuffer, &progress, fileSizeRequested, i);
    }
    // Enviar o restante do buffer, se houver
    if (outputBuffer.length() > 0)
    {
      client.print(outputBuffer);
    }
  }
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

      // Verificando se a requisição é válida
      int index = request.indexOf("GET /file?size=");
      if (index != -1)
      {
        int fileSizeRequested = request.substring(index + 15).toInt();
        Serial.print("Request: ");
        Serial.println(request);
        Serial.print("File size request: ");
        Serial.println(fileSizeRequested);

        // envia os dados
        send_data(client, fileSizeRequested);
      }
      else
      {
        Serial.println("Requisição inválida");
      }
    }
    client.stop();
    Serial.println("Cliente desconectado");
    delay(2000);
  }
}
