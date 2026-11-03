#define LeftF 3
#define LeftB 4
#define RightB 12
#define RightF 11
#define SpeedL 5
#define SpeedR 6

#define SoilF 13
#define SoilB 2
#define SoilSpeed 9

#define echoPin 7
#define trigPin 10

#define soilPin A0
#define PumpRelay 8

long duration;
int distance;
int soilValue;

bool waitingForFruit = false;
bool pumpRunning = false;

unsigned long pumpStartTime = 0;
unsigned long pumpDuration = 0;

unsigned long soilDownTime = 3000;
unsigned long soilUpTime = 3000;

int soilMotorSpeed = 120;

int drySoilLimit = 500;

void setup() {
  Serial.begin(9600);

  pinMode(LeftF, OUTPUT);
  pinMode(LeftB, OUTPUT);
  pinMode(RightF, OUTPUT);
  pinMode(RightB, OUTPUT);
  pinMode(SpeedL, OUTPUT);
  pinMode(SpeedR, OUTPUT);

  pinMode(SoilF, OUTPUT);
  pinMode(SoilB, OUTPUT);
  pinMode(SoilSpeed, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(PumpRelay, OUTPUT);
  digitalWrite(PumpRelay, HIGH);

  stopSoilMotor();
  Stop();

  delay(2000);
}

void loop() {
  readFromRaspberry();

  if (!waitingForFruit && !pumpRunning) {
    distance = Distance();

    if (distance > 5) {
      Forward();
    } else {
      Stop();
    }
  } else {
    Stop();
  }

  checkPump();
}

void readFromRaspberry() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    msg.toLowerCase();

    Serial.print("Received: ");
    Serial.println(msg);

    if (msg == "plant") {
      if (!waitingForFruit && !pumpRunning) {
        Stop();
        waitingForFruit = true;

        Serial.println("Plant detected");
        Serial.println("Waiting for fruit type...");
      }
    }

    else if (msg == "apple") {
      handleFruit("apple", 3000);
    }

    else if (msg == "guava") {
      handleFruit("guava", 5000);
    }

    else if (msg == "pomegranate") {
      handleFruit("pomegranate", 7000);
    }

    else if (msg == "go") {
      waitingForFruit = false;
      pumpRunning = false;
      digitalWrite(PumpRelay, HIGH);
    }
  }
}

void handleFruit(String fruitName, unsigned long waterTime) {
  if (!waitingForFruit || pumpRunning) {
    return;
  }

  Stop();

  Serial.print("Fruit type: ");
  Serial.println(fruitName);

  Serial.println("Checking soil...");
  checkSoil();

  Serial.print("Soil Value: ");
  Serial.println(soilValue);

  unsigned long finalWaterTime = waterTime;

  if (soilValue > drySoilLimit) {
    Serial.println("Soil is dry, adding 2 seconds...");
    finalWaterTime += 2000;
  } else {
    Serial.println("Soil is wet, watering normal time...");
  }

  Serial.print("Final watering time: ");
  Serial.print(finalWaterTime);
  Serial.println(" ms");

  startPump(finalWaterTime);
}

void checkSoil() {
  Stop();

  Serial.println("Soil sensor down");
  soilDown();
  delay(soilDownTime);

  stopSoilMotor();
  delay(1000);

  soilValue = analogRead(soilPin);

  Serial.print("Soil Value: ");
  Serial.println(soilValue);

  Serial.println("Soil sensor up");
  soilUp();
  delay(soilUpTime);

  stopSoilMotor();
  delay(500);
}

void startPump(unsigned long durationTime) {
  pumpDuration = durationTime;
  pumpStartTime = millis();
  pumpRunning = true;

  digitalWrite(PumpRelay, LOW);

  Serial.print("Pump ON for ");
  Serial.print(durationTime);
  Serial.println(" ms");
}

void checkPump() {
  if (pumpRunning) {
    if (millis() - pumpStartTime >= pumpDuration) {
      digitalWrite(PumpRelay, HIGH);
      pumpRunning = false;

      Serial.println("Pump OFF");

      finishPlant();
    }
  }
}

void finishPlant() {
  waitingForFruit = false;
  pumpRunning = false;

  delay(1000);

  Serial.println("Finished plant, moving to next plant...");
}

void soilDown() {
  analogWrite(SoilSpeed, soilMotorSpeed);
  digitalWrite(SoilF, LOW);
  digitalWrite(SoilB, HIGH);
}

void soilUp() {
  analogWrite(SoilSpeed, soilMotorSpeed);
  digitalWrite(SoilF, HIGH);
  digitalWrite(SoilB, LOW);
}

void stopSoilMotor() {
  analogWrite(SoilSpeed, 0);
  digitalWrite(SoilF, LOW);
  digitalWrite(SoilB, LOW);
}

int Distance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0) {
    return 999;
  }

  distance = duration * 0.034 / 2;
  return distance;
}

void Forward() {
  analogWrite(SpeedR, 85);
  analogWrite(SpeedL, 85);

  digitalWrite(LeftF, HIGH);
  digitalWrite(LeftB, LOW);

  digitalWrite(RightF, HIGH);
  digitalWrite(RightB, LOW);
}

void Stop() {
  analogWrite(SpeedR, 0);
  analogWrite(SpeedL, 0);

  digitalWrite(LeftF, LOW);
  digitalWrite(LeftB, LOW);

  digitalWrite(RightF, LOW);
  digitalWrite(RightB, LOW);
}
