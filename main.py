import cv2
from ultralytics import YOLO
import paho.mqtt.client as mqtt
import time
import requests
import os
from dotenv import load_dotenv

# 1. 先載入環境變數
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# 檢查變數是否存在，若不存在直接結束程式，避免後續報錯
if not TG_TOKEN or not TG_CHAT_ID:
    print("錯誤：找不到環境變數，請檢查 .env 檔案是否包含 TG_TOKEN 與 TG_CHAT_ID")
    exit() # 找不到就不要跑了

# --- 設定區 ---
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "ntou/cs/solomon/detect"

# 初始化 MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
try:
    client.connect(MQTT_BROKER, 1883, 60)
except Exception as e:
    print(f"MQTT 連線失敗: {e}")

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

def send_telegram_alert(frame, message):
    photo_path = "alert.jpg"
    cv2.imwrite(photo_path, frame)
    
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": TG_CHAT_ID, "caption": message}
        try:
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(">>> Telegram 警報照片已送出！")
            else:
                print(f"Telegram 回傳錯誤: {response.text}")
        except Exception as e:
            print(f"發送失敗: {e}")
    
    if os.path.exists(photo_path):
        os.remove(photo_path)

last_alert_time = 0

print("系統啟動中，監控中...")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # 執行 AI 辨識
    results = model(frame, stream=True, verbose=False) # verbose=False 讓終端機乾淨一點
    person_detected = False
    
    # 這裡修正一個潛在問題：確保 annotated_frame 永遠有值
    annotated_frame = frame.copy() 

    for r in results:
        annotated_frame = r.plot()
        for box in r.boxes:
            label = model.names[int(box.cls[0])]
            if label == 'person':
                person_detected = True

    # 偵測邏輯
    if person_detected and (time.time() - last_alert_time > 10):
        current_time = time.strftime('%H:%M:%S')
        msg = f"【AI 警報】於 {current_time} 偵測到可疑人員！"
        
        client.publish(MQTT_TOPIC, msg)
        send_telegram_alert(annotated_frame, msg)
        
        last_alert_time = time.time()

    cv2.imshow("AIoT Edge Monitor", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()
client.disconnect()