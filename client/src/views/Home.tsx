import {
  FC,
  useEffect,
  useState,
  useRef,
  ChangeEventHandler,
  Ref,
} from "react";
import {
  PageHeader,
  Comment,
  Input,
  Button,
  Form,
  InputRef,
  Checkbox,
} from "antd";
import { SendOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const EMOJI_REGEX = /\p{Emoji}/gu;

export const Home: FC = () => {
  const [socket, setSocket] = useState<null | WebSocket>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [messageText, setMessageText] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [form] = Form.useForm();
  const textInputRef = useRef<HTMLInputElement | null>(null);
  const [statistics, setStatistics] = useState<string[]>([]);
  const [bgColor, setBgColor] = useState("#202e3e");
  const [isBgModeActive, setIsBgModeActive] = useState(false);
  const [isEmojiRainModeActive, setIsEmojiRainModeActive] = useState(false);
  const [isEmojiAnimationPlaying, setIsEmojiAnimationPlaying] = useState(false);

  const navigate = useNavigate();

  const handleTextInputChange: ChangeEventHandler<HTMLInputElement> = (
    event
  ) => {
    setMessageText(event.target.value);
  };

  const handleMessageSending = () => {
    messageText &&
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
    const emotions = messages
      .map((message) => message.emotion)
      .filter(
        (emotion) =>
          emotion === "neutral" ||
          emotion === "positive" ||
          emotion === "negative"
      );

    setStatistics(emotions);

    if (isBgModeActive) {
      // 16, 133, 47 positive
      // 145, 35, 16 negative
      // 32, 46, 62 neutral

      const positive =
        emotions.filter((emotion) => emotion === "positive").length /
        emotions.length;
      const negative =
        emotions.filter((emotion) => emotion === "negative").length /
        emotions.length;
      const neutral =
        emotions.filter((emotion) => emotion === "neutral").length /
        emotions.length;

      const resultColor = `rgb(${
        16 * positive + 145 * negative + 32 * neutral
      }, ${133 * positive + 35 * negative + 46 * neutral}, ${
        47 * positive + 16 * negative + 62 * neutral
      })`;

      setBgColor(resultColor);
    }

    if (isEmojiRainModeActive && !isEmojiAnimationPlaying && messages.length) {
      (async () => {
        // const translateResponse = await axios.post(
        //   "https://translate.api.cloud.yandex.net/translate/v2/translate/",
        //   {
        //     // folderId: "b1gci6b0pctsrdqq06j0",
        //     // targetLanguageCode: "emj",
        //     // texts: ['Привет'] //messages[messages.length - 1].text.split(" "),
        //   },
        //   {
        //     headers: {
        //       Authorization:
        //         "Bearer t1.9euelZrGzZeLm5jPlpickMeQmY-bk-3rnpWakomRk42cj5fPx5jHmZeQlcjl9PcKHhxm-e9PPAfC3fT3SkwZZvnvTzwHwg.GjLZyFlTlhS0LKoF_cTZx1ckts20SFI_GotIisQwpmRJ-ZrIjWcMyKi-epedsWN-KwslYx_0Ph2BLRngfT0aBw",
        //         "Access-Control-Allow-Origin": "*"
        //     },
        //   }
        // );

        // console.log(translateResponse);

        const matches = [
          ...messages[messages.length - 1].text.matchAll(EMOJI_REGEX),
        ];
        matches.forEach((match, index) => {
          const emoji: string = match[0];

          const element = document.createElement("div");
          element.classList.add("animating-emoji");
          element.innerText = emoji;
          element.style.animationDelay = `${index * 1.5}s`;
          setIsEmojiAnimationPlaying(true);

          document.body.appendChild(element);

          setTimeout(() => {
            element.remove();
            setIsEmojiAnimationPlaying(false);
          }, 1500 * (index + 1) + 500);
        });
      })();
    }
  }, [messages, isBgModeActive, isEmojiRainModeActive]);

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        const message = JSON.parse((event.data as string).replaceAll("'", '"'));

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

  const handleModeChange = () => {
    setIsBgModeActive(!isBgModeActive);

    if (isBgModeActive) {
      const emotions = messages
        .map((message) => message.emotion)
        .filter(
          (emotion) =>
            emotion === "neutral" ||
            emotion === "positive" ||
            emotion === "negative"
        );

      const positive =
        emotions.filter((emotion) => emotion === "positive").length /
        emotions.length;
      const negative =
        emotions.filter((emotion) => emotion === "negative").length /
        emotions.length;
      const neutral =
        emotions.filter((emotion) => emotion === "neutral").length /
        emotions.length;

      const resultColor = `rgb(${
        16 * positive + 145 * negative + 32 * neutral
      }, ${133 * positive + 35 * negative + 46 * neutral}, ${
        47 * positive + 16 * negative + 62 * neutral
      })`;

      setBgColor(resultColor);
    } else {
      setBgColor("#202e3e");
    }
  };

  const handleEmojiRainModeChange = () => {
    setIsEmojiRainModeActive(!isEmojiRainModeActive);
  };

  return (
    <div
      style={{
        padding: "20px 40px",
        color: "#fff",
        background: isBgModeActive ? `${bgColor}` : "#202e3e",
        transition: "0.5s",
        height: "100vh",
      }}
    >
      <PageHeader
        title={localStorage.getItem("username") ?? ""}
        extra={[
          <>
            <Checkbox onClick={handleEmojiRainModeChange}>
              Режим смайлов
            </Checkbox>
            <Checkbox onClick={handleModeChange}>Эмоциональный фон</Checkbox>
            <Button
              onClick={() => {
                localStorage.removeItem("username");
                navigate("/auth");
              }}
              type="primary"
            >
              Выйти
            </Button>
          </>,
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
        {messages.map(({ sender, text, emotion }, index) => {
          const background: string =
            sender === localStorage.getItem("username") ? "#1e4f84" : "#394d63";

          const className =
            emotion === "positive"
              ? "positive-message"
              : emotion === "negative"
              ? "negative-message"
              : "";

          return (
            <Comment
              key={index}
              className={
                sender === localStorage.getItem("username")
                  ? `${className} own`
                  : className
              }
              style={{
                background,
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
          );
        })}
        <div ref={messagesEndRef}></div>
      </div>
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: 12,
          height: "100vh",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {statistics.map((emotion) => (
          <div
            style={{
              width: "100%",
              height: "100%",
              background:
                emotion === "neutral"
                  ? "#2c537d"
                  : emotion === "positive"
                  ? "#25d746"
                  : emotion === "negative"
                  ? "#e23724"
                  : "none",
            }}
          ></div>
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
