import { FC, useEffect, useState, useRef, ChangeEventHandler } from "react";
import { PageHeader, Comment, Input, Button, Form } from "antd";
import { SendOutlined } from "@ant-design/icons";
import { io } from "socket.io-client";
import { useNavigate } from "react-router-dom";

export const Home: FC = () => {
  const [socket, setSocket] = useState<any>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [messageText, setMessageText] = useState("");
  const textRef = useRef<any>(null);
  const [form] = Form.useForm();

  const navigate = useNavigate();

  const handleTextInputChange: ChangeEventHandler<HTMLInputElement> = (
    event
  ) => {
    setMessageText(event.target.value);
  };

  const handleMessageSending = () => {
    setMessageText("");
    form.resetFields();
  };

  useEffect(() => {
    if (!localStorage.getItem("username")) {
      navigate("/auth");
    }

    setSocket(
      io(`ws://localhost:8000/ws/${localStorage.getItem("username") ?? ""}`)
    );

    setMessages([
      { id: "0", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
      { id: "1", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
      { id: "2", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
      { id: "3", text: "falsdfkjasldkfjasf", sender: "lkjlkj" },
      { id: "4", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
      { id: "5", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
      { id: "6", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
      {
        id: "7",
        text: "falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf falsdfkjasldkfjasf",
        sender: "qweruadflzvx",
      },
      { id: "8", text: "falsdfkjasldkfjasf", sender: "qweruadflzvx" },
    ]);
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
        {messages.map(({ sender, text, id }) => (
          <Comment
            key={id}
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
              placeholder="Введите сообщение"
              onChange={handleTextInputChange}
              size="large"
              style={{ width: "calc(100vw - 48px - 80px)" }}
              ref={textRef}
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
