// Функция для открытия и закрытия виджета чата
function toggleChat() {
    const chatWidget = document.querySelector('.chat-widget');
    chatWidget.style.display = chatWidget.style.display === 'none' ? 'flex' : 'none';
}

// Функция для отправки сообщения
async function sendMessage() {
    const messageInput = document.getElementById("user-message");
    const chatBody = document.getElementById("chat-body");
    const userMessage = messageInput.value.trim();

    // Проверка на пустое сообщение
    if (!userMessage) return;

    // Отображаем сообщение пользователя в чате
    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("user-message");
    userMessageElement.textContent = userMessage;
    chatBody.appendChild(userMessageElement);

    // Прокрутка вниз после добавления нового сообщения
    chatBody.scrollTop = chatBody.scrollHeight;

    // Очищаем поле ввода
    messageInput.value = '';

    // Отправка сообщения на локальный сервер Flask
    try {
        const response = await fetch('http://127.0.0.1:5000/chat', { // Локальный URL для тестирования
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        // Обработка ответа от сервера
        const data = await response.json();
        const assistantResponse = data.response;

        // Отображаем ответ ассистента в чате
        const assistantMessageElement = document.createElement("div");
        assistantMessageElement.classList.add("assistant-message");
        assistantMessageElement.textContent = assistantResponse;
        chatBody.appendChild(assistantMessageElement);

        // Прокрутка вниз после добавления ответа ассистента
        chatBody.scrollTop = chatBody.scrollHeight;
    } catch (error) {
        console.error("Ошибка при отправке сообщения:", error);
        // Отображаем сообщение об ошибке в чате
        const errorMessageElement = document.createElement("div");
        errorMessageElement.classList.add("assistant-message");
        errorMessageElement.textContent = "Извините, возникла ошибка. Пожалуйста, попробуйте снова.";
        chatBody.appendChild(errorMessageElement);
    }
}

// Обработчик нажатия на Enter для отправки сообщения
document.getElementById("user-message").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
