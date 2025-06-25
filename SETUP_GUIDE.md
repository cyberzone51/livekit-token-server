# Пошаговая инструкция по настройке стабильной работы Android-приложения

Эта инструкция поможет вам настроить стабильную работу вашего Android-приложения с LiveKit, независимо от того, включен компьютер или нет. Мы создадим сервер для генерации токенов и разместим его в облаке.

## 🟡 ШАГ 1: Сгенерируйте API ключи в LiveKit Cloud

1. Перейдите на [LiveKit Cloud](https://cloud.livekit.io)
2. Создайте аккаунт или войдите в существующий
3. Создайте новый проект (если у вас его еще нет)
4. В разделе **API Keys** нажмите кнопку **Create**
5. Запишите полученные ключи:
   - **API Key**
   - **API Secret** ← храните в секрете!

## 🟡 ШАГ 2: Подготовьте Python API сервер

Мы уже создали для вас сервер на FastAPI, который находится в папке `livekit_token_server`. Вам нужно:

1. Создайте файл `.env` на основе `.env.example`:
   ```
   cp .env.example .env
   ```

2. Отредактируйте файл `.env` и добавьте ваши ключи LiveKit:
   ```
   LIVEKIT_API_KEY=ваш_api_key
   LIVEKIT_API_SECRET=ваш_api_secret
   ```

3. Для локального тестирования установите зависимости и запустите сервер:
   ```
   pip install -r requirements.txt
   python main.py
   ```

4. Сервер будет доступен по адресу http://localhost:8000

## 🟡 ШАГ 3: Разместите сервер в облаке

Мы рекомендуем использовать [Railway.app](https://railway.app) для размещения сервера:

1. Создайте аккаунт на [Railway.app](https://railway.app)

2. Установите Railway CLI (опционально):
   ```
   npm i -g @railway/cli
   ```

3. Войдите в Railway:
   ```
   railway login
   ```

4. Создайте новый проект:
   ```
   railway init
   ```

5. Добавьте переменные окружения:
   ```
   railway variables set LIVEKIT_API_KEY=ваш_api_key LIVEKIT_API_SECRET=ваш_api_secret
   ```

6. Разверните приложение:
   ```
   railway up
   ```

Альтернативно, вы можете развернуть приложение через веб-интерфейс Railway:

1. Перейдите на [Railway.app](https://railway.app) и войдите
2. Нажмите **New Project** > **Deploy from GitHub**
3. Выберите ваш репозиторий с кодом сервера
4. Добавьте переменные окружения:
   - `LIVEKIT_API_KEY`: Ваш LiveKit API ключ
   - `LIVEKIT_API_SECRET`: Ваш LiveKit API секрет
5. Разверните приложение

После развертывания Railway предоставит вам URL вашего сервера (например, https://livekit-token-server-production.up.railway.app).

## 🟡 ШАГ 4: Обновите Android-приложение

Мы уже обновили файл `TokenExt.kt` в вашем Android-приложении. Теперь нужно собрать проект в Android Studio:

1. Откройте проект в Android Studio:
   - Запустите Android Studio
   - Выберите "Open an existing Android Studio project"
   - Найдите и выберите папку `Sergio_AI`
   - Дождитесь, пока Android Studio загрузит проект и синхронизирует Gradle

2. Откройте файл `Sergio_AI/app/src/main/java/io/livekit/android/example/voiceassistant/TokenExt.kt`

3. Замените URL сервера токенов на ваш:
   ```kotlin
   // URL of your deployed token server
   const val TOKEN_SERVER_URL = "https://your-token-server-url.railway.app"
   ```
   Замените `https://your-token-server-url.railway.app` на URL вашего сервера, полученный на предыдущем шаге.

4. Замените URL LiveKit сервера на URL вашего проекта:
   ```kotlin
   // LiveKit Cloud URL - замените на URL вашего проекта в LiveKit Cloud
   val liveKitUrl = "wss://your-livekit-server-url.livekit.cloud"
   ```
   Замените `wss://your-livekit-server-url.livekit.cloud` на WebSocket URL вашего проекта в LiveKit Cloud. Его можно найти в настройках проекта в LiveKit Cloud.

5. Соберите проект:
   - Нажмите на меню "Build" в верхней части Android Studio
   - Выберите "Make Project" (или нажмите Ctrl+F9)
   - Дождитесь завершения сборки

6. Запустите приложение:
   - Подключите Android-устройство к компьютеру или настройте эмулятор
   - Нажмите на зеленую кнопку "Run" (или нажмите Shift+F10)
   - Выберите целевое устройство для установки и запуска приложения
   - Дождитесь установки и запуска приложения на устройстве

## 🟢 Готово!

Теперь ваше приложение будет работать стабильно, независимо от того, включен компьютер или нет. Токены будут генерироваться на вашем сервере в облаке, а не локально.

### Как это работает:

1. Ваше Android-приложение отправляет запрос на ваш сервер токенов в облаке
2. Сервер генерирует токен с помощью LiveKit API ключей
3. Приложение получает токен и использует его для подключения к LiveKit
4. Все работает стабильно, так как сервер токенов всегда доступен в облаке

### Дополнительные рекомендации:

1. Добавьте аутентификацию на ваш сервер токенов для повышения безопасности
2. Настройте мониторинг сервера для отслеживания его работы
3. Рассмотрите возможность использования CDN для улучшения производительности

Если у вас возникнут вопросы или проблемы, обратитесь к документации [LiveKit](https://docs.livekit.io) или [Railway](https://docs.railway.app).
