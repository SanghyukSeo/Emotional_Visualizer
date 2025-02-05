#include <Servo.h>

// 서보 객체 생성
Servo servo1, servo2, servo3, servo4;

// 초기 위치 설정
const int initialPosition = 85;   // 서보의 중립 위치로 설정
const int rotatedPosition = 0;    // 회전 위치

void setup() {
  Serial.begin(9600);

  // 전원 안정화 대기 (1초)
  delay(1000);  // 전원 안정화 지연

  // 서보 핀 연결
  servo1.attach(3);
  servo2.attach(4);
  servo3.attach(5);
  servo4.attach(6);

  // 초기 위치로 설정 (전원 안정화 후)
  resetServos();
}

void loop() {
  if (Serial.available() > 0) {
    int command = Serial.parseInt();

    switch (command) {
      case 1:
        Serial.println("Servo 1 Activated");
        moveServo(servo1);
        break;
      case 2:
        Serial.println("Servo 2 Activated");
        moveServo(servo2);
        break;
      case 3:
        Serial.println("Servo 3 Activated");
        moveServo(servo3);
        break;
      case 4:
        Serial.println("Servo 4 Activated");
        moveServo(servo4);
        break;
      default:
        break;
    }
  }
}

// 서보 제어 함수
void moveServo(Servo &servo) {
  servo.write(rotatedPosition);    // 회전
  delay(500);                      // 짧은 유지
  servo.write(initialPosition);    // 원래 위치로 복귀
  delay(300);                      // 복귀 후 짧은 유지
}

// 초기 위치로 리셋
void resetServos() {
  servo1.write(initialPosition);
  servo2.write(initialPosition);
  servo3.write(initialPosition);
  servo4.write(initialPosition);
}

