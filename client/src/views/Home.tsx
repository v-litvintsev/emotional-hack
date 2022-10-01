import {
  FC,
  useEffect,
  useState,
  useRef,
  ChangeEventHandler,
  Ref,
} from "react";
import { PageHeader, Comment, Input, Button, Form, InputRef } from "antd";
import { SendOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const Home: FC = () => {
  const [socket, setSocket] = useState<null | WebSocket>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [messageText, setMessageText] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [form] = Form.useForm();
  const textInputRef = useRef<HTMLInputElement | null>(null);

  const navigate = useNavigate();

  const handleTextInputChange: ChangeEventHandler<HTMLInputElement> = (
    event
  ) => {
    setMessageText(event.target.value);
  };

  const handleMessageSending = () => {
    socket?.send(
      JSON.stringify({
        type: "message",
        text: messageText,
        sender: localStorage.getItem("username"),
        emotion: "none",
      })
    );
    setMessageText("");
    form.resetFields();
  };

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        const message = JSON.parse(JSON.parse(event.data));

        if (message.type === "message") {
          setMessages((messages) => [...messages, message]);

          if (messagesEndRef) {
            setTimeout(() => {
              messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
            }, 100);
          }

          textInputRef.current?.focus();
        }
      };
    }
  }, [socket]);

  useEffect(() => {
    if (!localStorage.getItem("username")) {
      navigate("/auth");
    }

    if (!socket) {
      setSocket(new WebSocket(`ws://localhost:80/ws`));
    }

    textInputRef.current?.focus();
  }, []);

  useEffect(() => {
    (async () => {
      const response = await axios.get("http://localhost:80/messages");
      setMessages(response.data.data[0]);
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    })();
  }, []);

  return (
    <div
      style={{
        padding: "20px 40px",
        color: "#fff",
        background: "#202e3e",
        height: "100vh",
      }}
    >
      <PageHeader
        title={localStorage.getItem("username") ?? ""}
        style={{ color: "#fff !important" }}
        extra={[
          <Button
            onClick={() => {
              localStorage.removeItem("username");
              navigate("/auth");
            }}
            type="primary"
          >
            Выйти
          </Button>,
        ]}
      />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          height: "calc(100% - 150px)",
          overflow: "auto",
        }}
      >
        {messages.map(({ sender, text }, index) => (
          <Comment
            key={index}
            style={{
              background:
                sender === localStorage.getItem("username")
                  ? "#1e4f84"
                  : "#394d63",
              borderRadius: "10px",
              padding: "0 30px",
              color: "#fff",
              marginTop: 30,
              maxWidth: "80%",
              alignSelf:
                sender === localStorage.getItem("username")
                  ? "flex-end"
                  : "flex-start",
            }}
            content={<p>{text}</p>}
            author={sender}
          />
        ))}
        <div ref={messagesEndRef}></div>
      </div>
      <div
        style={{
          display: "flex",
          position: "fixed",
          bottom: 40,
          width: "calc(100% - 80px)",
        }}
      >
        <Form
          form={form}
          onFinish={handleMessageSending}
          style={{
            display: "flex",
            width: "100%",
          }}
        >
          <Form.Item name="text" style={{ marginBottom: "0" }}>
            <Input
              ref={textInputRef as Ref<InputRef>}
              placeholder="Введите сообщение"
              onChange={handleTextInputChange}
              size="large"
              style={{ width: "calc(100vw - 48px - 80px)" }}
            />
          </Form.Item>
          <Button type="primary" size="large" htmlType="submit">
            <SendOutlined />
          </Button>
        </Form>
      </div>
    </div>
  );
};
