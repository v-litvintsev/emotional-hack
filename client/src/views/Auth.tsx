import { Button, Form, Input } from "antd";
import { FC } from "react";
import { useNavigate } from "react-router-dom";

export const Auth: FC = () => {
  const navigate = useNavigate();

  const handleSubmit = (values: any) => {
    if (values.username) {
      navigate("/");
      localStorage.setItem("username", values.username);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
      }}
    >
      <Form onFinish={handleSubmit}>
        <Form.Item
          label="Имя пользователя"
          name="username"
          rules={[{ required: true, message: "Поле обязательно" }]}
        >
          <Input />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Подтвердить
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};
