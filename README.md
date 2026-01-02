AIoT Edge Monitor: YOLOv8 影像偵測與自動化警報系統
這是一個基於 AI 影像辨識的物聯網監控專案。系統能透過網路攝影機即時偵測目標（如：人），並在偵測到特定物件時，透過 MQTT 協定觸發雲端警報，同步傳送即時影像至使用者 Telegram 手機端。

🚀 核心功能
AI 即時偵測：使用 Ultralytics YOLOv8 模型進行邊緣運算辨識。

雲端通訊：整合 MQTT 協定，實現低延遲的偵測狀態同步。

即時通知：對接 Telegram Bot API，實現異常狀況自動拍照回傳。

環境變數管理：採用 .env 進行 API Token 與 Chat ID 的安全控管。

🛠️ 開發與 Debug 歷程 (Problem Solving)
在開發本專案的過程中，我遇到了多個實務上的挑戰，並透過資工思維一一克服：

1. 環境遷移與路徑寫死問題 (Virtual Environment Issues)
問題：將專案從 C:\Users\User\aiot_env 搬移至 C:\sideproject 後，虛擬環境因絕對路徑寫死導致失效。

解決方案：不採取搬移資料夾的方式，而是利用 pip freeze > requirements.txt 紀錄套件清單，並在新的路徑重新建立虛擬環境，確保開發環境的純淨與可移植性。

2. 第三方 API 通訊故障排除 (Telegram API Debugging)
在串接 Telegram Bot 時，經歷了連續的 API 報錯調校：

401 Unauthorized：發現 Token 複製不全或無效。透過 @BotFather 執行 /revoke 重新取得憑證解決。

404 Not Found：URL 路徑拼寫錯誤。經比對 RESTful API 文件後，修正為正確的 /bot<token>/getMe 格式。

400 Bad Request (Chat not found)：機器人無法主動發訊。透過主動與機器人發起對話（/start）並重新抓取 Chat ID 解決。

3. Git 歷史污染與大型檔案管理 (Git History Management)
問題：不慎將包含 300MB torch 庫的 aiot_env 推送到 GitHub，導致超過 100MB 限制而被 Rejected。

解決方案：執行 Git 歷史重置（Reset History），刪除 .git 紀錄，配置 .gitignore 徹底排除二進位大型檔案與敏感資訊 (.env)，實現輕量化推送。

📂 專案結構
Plaintext

.
├── main.py            # 主程式：包含 YOLO 辨識與 MQTT/Telegram 邏輯
├── leetcode_1.py      # 演算法練習：Two Sum (Hash Map 優化版)
├── .env.example       # 環境變數範本 (不包含私鑰)
├── requirements.txt   # 專案套件依賴清單
└── .gitignore         # Git 忽略設定 (排除環境與金鑰)
⚙️ 安裝與使用
複製專案：

Bash

git clone https://github.com/你的帳號/AIoT-Edge-Monitor.git
cd AIoT-Edge-Monitor
建立虛擬環境與安裝套件：

Bash

python -m venv aiot_env
aiot_env\Scripts\activate
pip install -r requirements.txt
設定環境變數： 將 .env.example 重新命名為 .env，並填入你的 TG_TOKEN 與 TG_CHAT_ID。

執行程式：

Bash

python main.py
