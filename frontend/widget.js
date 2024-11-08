// Функция для отображения/скрытия виджета чата
function toggleChat() {
    const chatWidget = document.querySelector('.chat-widget');
    chatWidget.style.display = chatWidget.style.display === 'none' ? 'flex' : 'none';
}

// Функция отправки сообщения
async function sendMessage() {
    const messageInput = document.getElementById("user-message");
    const chatBody = document.getElementById("chat-body");
    const userMessage = messageInput.value.trim();

    if (!userMessage) return;

    // Отображаем сообщение пользователя
    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("user-message");
    userMessageElement.textContent = userMessage;
    chatBody.appendChild(userMessageElement);

    chatBody.scrollTop = chatBody.scrollHeight;
    messageInput.value = '';

    // Отправка сообщения на сервер Flask
    try {
        console.log("Отправка сообщения на сервер:", userMessage);

        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=UTF-8'
            },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        const assistantResponse = data.response;

        console.log("Ответ от сервера:", assistantResponse);

        const assistantMessageElement = document.createElement("div");
        assistantMessageElement.classList.add("assistant-message");
        assistantMessageElement.textContent = assistantResponse;
        chatBody.appendChild(assistantMessageElement);

        chatBody.scrollTop = chatBody.scrollHeight;
    } catch (error) {
        console.error("Ошибка при отправке сообщения:", error);

        const errorMessageElement = document.createElement("div");
        errorMessageElement.classList.add("assistant-message");
        errorMessageElement.textContent = "Извините, возникла ошибка. Пожалуйста, попробуйте снова.";
        chatBody.appendChild(errorMessageElement);
    }
}
