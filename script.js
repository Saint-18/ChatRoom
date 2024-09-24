document.addEventListener("DOMContentLoaded", function () {
  const wrapper = document.querySelector("#wrapper");
  // Fetch messages from the FastAPI endpoint
  const chatId = 2;
  fetch(`/api/messages/get/${chatId}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network error");
      }
      return response.json();
    })
    .then((messages) => {
      displayMessages(wrapper, messages);
      createMessageEntryForm(wrapper);
    })
    .catch((error) => {
      console.error("Error fetching messages:", error);
    });

  function displayMessages(wrapper, messages) {
    const messageWindow = document.createElement("div");
    messageWindow.classList.add("flex-1", "p-8");
    wrapper.appendChild(messageWindow);
    // Create frame for messages
    const frame = document.createElement("div");
    frame.classList.add(
      "block",
      "max-w-5xl",
      "h-80",
      "overflow-y-auto",
      "p-6",
      "bg-gray-200",
      "border",
      "border-slate-200",
      "rounded-lg",
      "shadow"
    );
    messageWindow.appendChild(frame);

    for (m of messages) {
      // Create DOM elements
      const messageBox = document.createElement("div");
      const message = document.createElement("div");
      const nameDiv = document.createElement("div");
      const fullName = document.createElement("span");
      const timeStamp = document.createElement("span");
      const messageContent = document.createElement("p");
      const deleteButton = document.createElement("button");

      // Format timestamp
      const datetime = new Date(m.timestamp);
      const hours = datetime.getUTCHours();
      const minutes = datetime.getUTCMinutes();
      const time = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;

      // Append classes to elements
      nameDiv.classList.add("flex", "items-center", "space-x-2");
      if (m.username === "jdoe123") {
        messageBox.classList.add("flex", "items-start", "gap-2.5", "justify-end", "mt-4");
        message.classList.add(
          "flex",
          "flex-col",
          "w-full",
          "max-w-xs",
          "leading-1.5",
          "p-4",
          "border-slate-200",
          "bg-slate-100",
          "rounded-s-xl",
          "rounded-ee-xl"
        );
        fullName.classList.add("text-sm", "font-semibold", "text-slate-900");
        timeStamp.classList.add("text-sm", "font-normal", "text-slate-500");
        messageContent.classList.add("text-sm", "font-normal", "py-2.5", "text-slate-900");
      } else {
        messageBox.classList.add("flex", "items-start", "gap-2.5", "mt-4");
        message.classList.add(
          "flex",
          "flex-col",
          "w-full",
          "max-w-xs",
          "leading-1.5",
          "p-4",
          "border-slate-200",
          "bg-emerald-700",
          "rounded-e-xl",
          "rounded-es-xl"
        );
        fullName.classList.add("text-sm", "font-semibold", "text-slate-200");
        timeStamp.classList.add("text-sm", "font-normal", "text-slate-200");
        messageContent.classList.add("text-sm", "font-normal", "py-2.5", "text-slate-100");
      }

      // Add content from JSON into HTML
      fullName.textContent = m.username;
      timeStamp.textContent = m.created_at;
      //adding delete button after time stamp

    deleteButton.textContent="Delete";
    deleteButton.classList.add("text-red-500", "text-xs");
    //js function to handle delete requests
    deleteButton.onclick=function(){
      deleteMessage(m.id);   //here m.id refers to message id
    }
      messageContent.textContent = m.message_body;

      frame.appendChild(messageBox);
      messageBox.appendChild(message);
      message.appendChild(nameDiv);
      nameDiv.appendChild(fullName);
      nameDiv.appendChild(timeStamp);
      message.appendChild(messageContent);
    }
  }

  function createMessageEntryForm(wrapper) {
    const formWindow = document.createElement("form");
    formWindow.classList.add("max-w-5xl");
    wrapper.appendChild(formWindow);

    const formFrame = document.createElement("div");
    const input = document.createElement("input");
    const button = document.createElement("button");

    formFrame.classList.add("flex", "mb-5", "px-8");

    input.classList.add(
      "bg-gray-50",
      "border",
      "border-gray-300",
      "text-gray-900",
      "text-sm",
      "rounded-lg",
      "focus:outline-none",
      "focus:ring-emerald-500",
      "focus:border-emerald-500",
      "block",
      "w-full",
      "p-2.5",
      "mr-2"
    );
    input.type = "text";
    input.placeholder = "Enter your message...";
    input.required = true;

    button.classList.add(
      "text-white",
      "bg-emerald-600",
      "hover:bg-emerald-700",
      "focus:ring-4",
      "focus:outline-none",
      "focus:ring-emerald-300",
      "font-medium",
      "rounded-lg",
      "text-sm",
      "px-5",
      "py-2.5",
      "text-center"
    );
    button.type = "submit";
    button.textContent = "Send";

    formWindow.appendChild(formFrame);
    formFrame.appendChild(input);
    formFrame.appendChild(button);
  }

  async function deleteMessage(messageId){
    try {
      const response = await fetch(`/api/messages/delete/${messageId}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
      });

      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data.detail); // Handle success message

  } catch (error) {
      console.error('Error:', error);
  }
  }
});
