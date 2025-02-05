import cv2
from fer import FER
import serial
import time

# 감정 인식 모델 초기화
emotion_detector = FER(mtcnn=True)

# Arduino Nano와 시리얼 통신 설정
arduino = serial.Serial('/dev/cu.usbserial-14140', 9600)
time.sleep(2)  # Arduino 초기화 대기 시간

# 감정에 대한 코드 매핑
emotion_codes = {
    'neutral': 1,
    'sad': 2,
    'happy': 3,
    'angry': 4
}

previous_emotion = None

# 카메라 켜기
cap = cv2.VideoCapture(0)

# 타이머 설정
start_time = time.time()
run_detection = True  # 감정 인식 활성화 상태

print("🚀 감정 인식 시작 (ESC 키: 종료, 스페이스바: 재시작)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 감정 인식 활성화된 경우
    if run_detection:
        current_time = time.time()
        
        # 감정 인식 수행 (10초 동안만 작동)
        if current_time - start_time < 10:
            result = emotion_detector.top_emotion(frame)
            
            if result:
                emotion, score = result

                # 감정이 변경될 때만 시리얼 전송
                if emotion != previous_emotion and emotion in emotion_codes:
                    code = emotion_codes[emotion]
                    arduino.write(f'{code}\n'.encode())  # Arduino로 코드 전송
                    print(f'📤 Sent to Arduino: {emotion} ({code})')
                    previous_emotion = emotion  # 이전 감정 업데이트

                # 화면에 표시
                if score is not None:
                    cv2.putText(frame, f'{emotion} ({score*100:.2f}%)', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, f'{emotion}', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # 10초 후 감정 인식 일시정지
            print("⏸️ 감정 인식 일시정지 (스페이스바로 재시작 가능)")
            run_detection = False

    # 감정 인식 결과 표시
    cv2.imshow('Emotion Detection', frame)

    # 키 입력 처리
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC 키로 종료
        print("❌ ESC 키 감지 - 프로그램 종료")
        break
    elif key == 32:  # 스페이스바로 감정 인식 재시작
        print("▶️ 감정 인식 재시작")
        run_detection = True
        start_time = time.time()  # 타이머 초기화

# 종료 시 자원 정리
cap.release()
cv2.destroyAllWindows()
arduino.close()
