document.addEventListener("DOMContentLoaded", function () {
  const wrapper = document.querySelector("#wrapper");
  const list = document.querySelector("#chat-list");
  // Fetch messages from the FastAPI endpoint
  const currentURL = window.location.href;
  const splitURL = currentURL.split("/");
  // Update chatId based on URL
  const chatId = splitURL[splitURL.length - 1];
  // if (currentURL contains chat/something) call getMessages
  if (Number.isInteger(Number(chatId))) {
    getMessages(chatId);
  }
  listenForLogin();
  if (list) {
    const cookieUser = document.cookie
      .split("; ")
      .find((row) => row.startsWith("username="))
      ?.split("=")[1];
    buildSidebar(cookieUser, chatId);
  }
  function getMessages(chatId) {
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
  }

  function buildSidebar(user, chatId) {
    const request = {
      username: user,
    };

    // Convert the object to JSON
    const userJSON = JSON.stringify(request);
    fetch("/api/get/chatlist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: userJSON,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data) {
          for (d of data) {
            const listElement = document.createElement("li");
            const link = document.createElement("a");
            // if chatId is present, update the link to highlight chat in sidebar
            link.classList.add(
              "block",
              "py-2",
              "px-4",
              "hover:bg-emerald-700",
              "hover:text-gray-200",
              "rounded"
            );
            if (d.chat_id == chatId) {
              link.classList.add("bg-emerald-700", "text-gray-200");
            }
            link.setAttribute("id", d.chat_id);
            link.setAttribute("href", "/chat/" + d.chat_id);
            link.textContent = d.chat_title;
            list.appendChild(listElement);
            listElement.appendChild(link);
          }
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error loading chats.");
      });
  }

  function listenForLogin() {
    const form = document.getElementById("loginForm");

    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();

        // Get the values of the input fields
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Send the data to the Python backend
        // TODO: Create backend route to handle login
        // TODO: Add database processing to return authorized chat list

        const loginData = {
          username: username,
          password: password,
        };

        // Convert the object to JSON
        const loginJSON = JSON.stringify(loginData);
        fetch("/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: loginJSON,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data) {
              setCookie("username", username, 7);
              window.location.href = "/chat";
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Login failed. Please try again.");
          });
      });
    }
  }

  function setCookie(name, value, days) {
    let expires = "";

    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }

    // Set the cookie
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }

  function displayMessages(wrapper, messages) {
    const cookieUser = document.cookie
      .split("; ")
      .find((row) => row.startsWith("username="))
      ?.split("=")[1];
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
      // TODO: Insert message_id into HTML as ID tag for each message
      const messageBox = document.createElement("div");
      const message = document.createElement("div");
      const nameDiv = document.createElement("div");
      const fullName = document.createElement("span");
      const timeStamp = document.createElement("span");
      const messageContent = document.createElement("p");

      // Format timestamp
      const datetime = new Date(m.timestamp);
      const hours = datetime.getUTCHours();
      const minutes = datetime.getUTCMinutes();
      const time = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;

      // Append classes to elements
      nameDiv.classList.add("flex", "items-center", "space-x-2");
      if (m.username === cookieUser) {
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
      messageContent.textContent = m.message_body;

      frame.appendChild(messageBox);
      messageBox.appendChild(message);
      message.appendChild(nameDiv);
      nameDiv.appendChild(fullName);
      nameDiv.appendChild(timeStamp);
      message.appendChild(messageContent);
    }
    setTimeout(() => {
      frame.scrollTop = frame.scrollHeight;
    }, 0);
  }

  function createMessageEntryForm(wrapper) {
    const formWindow = document.createElement("form");
    formWindow.setAttribute("id", "newMessage");
    formWindow.classList.add("max-w-5xl");
    wrapper.appendChild(formWindow);

    const formFrame = document.createElement("div");
    const input = document.createElement("input");
    input.setAttribute("id", "messageText");
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

    listenForSumbit();
  }

  /* Handles chat message submission
  TODO: Tie into backend API to add message to database
        and reload the page with updated chats.
        use location.reload(true); to force reload
  NEED: Username from session cookie after login, 
        chat_id from HTML tag (return with user chats list upon login)

  */
  function listenForSumbit() {
    const form = document.getElementById("newMessage");

    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();

        const cookieUser = document.cookie
          .split("; ")
          .find((row) => row.startsWith("username="))
          ?.split("=")[1];

        // Capture the message content
        const messageText = document.getElementById("messageText").value;

        // Create a message object, need to also pass in username and chat_id
        // for db update
        const messageData = {
          username: cookieUser,
          chat_id: chatId,
          messageText: messageText,
        };

        // Convert the object to JSON
        const messageJSON = JSON.stringify(messageData);

        fetch("/api/messages/create", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: messageJSON,
        })
          .then((response) => response.json())
          .then((data) => {
            if ((data.status = 200)) {
              form.reset();
              location.reload(true);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
    } else {
      console.log("Unable to locate message input field");
    }
  }
});
