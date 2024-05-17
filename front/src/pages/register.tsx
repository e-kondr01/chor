import { Input, Button, Form, Spin, Flex } from "antd";
import { useForm } from "antd/es/form/Form";
import styles from "./auth.module.css";
import { Link } from "react-router-dom";
import { RoutePaths } from "../lib/routes";
import { authAPI } from "../api";
import { formErrorsHandler } from "../lib/form-errors-handler";
import { useState } from "react";
import Modal from "antd/es/modal/Modal";

const Register = () => {
  const [form] = useForm();
  const [formError, setFormError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [successModal, setSuccessModal] = useState(false);

  const onSubmit = async () => {
    const fields = form.getFieldsValue(true);
    try {
      setIsLoading(true);
      await authAPI.register(fields);
      setSuccessModal(true);
    } catch (error) {
      formErrorsHandler(form, error, setFormError);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Modal
        open={successModal}
        onCancel={() => {
          form.resetFields();
          setSuccessModal(false);
        }}
        footer={null}
      >
        <p>Вы успешно зарегистрировались!</p>
        <img src="https://cataas.com/cat" className={styles.successCat} />
        <Link to={RoutePaths.LOGIN}>
          <Button type="primary" block>
            Войти!
          </Button>
        </Link>
      </Modal>
      <Form
        requiredMark={false}
        form={form}
        onFinish={onSubmit}
        className={styles.login}
      >
        <Form.Item
          label="Логин"
          name="email"
          rules={[{ required: true, message: "Введите логин" }]}
          labelCol={{ span: 24 }}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Пароль"
          name="password"
          rules={[
            { required: true, message: "Введите пароль" },
            {
              pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d\W]).{8,}$/,
              message:
                "Пароль должен содержать строчные и прописные буквы, цифры и специальные символы",
            },
          ]}
          labelCol={{ span: 24 }}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item
          label="Повторите пароль"
          name="re_password"
          rules={[
            { required: true, message: "Введите пароль" },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error("Пароли не совпадают"));
              },
            }),
          ]}
          labelCol={{ span: 24 }}
        >
          <Input.Password />
        </Form.Item>
        {!!formError && <p className={styles.error}>{formError}</p>}
        <Form.Item>
        <Button type="primary" htmlType="submit" block disabled={isLoading}>
            {isLoading ? <Flex gap={16} align="center" justify="center"><Spin />Зарегистрироваться</Flex> : 'Зарегистрироваться'}
          </Button>
        </Form.Item>
      </Form>
      <p className="white fs-small">
        Уже есть аккаунт?{" "}
        <Link to={RoutePaths.LOGIN} className="white bold">
          Войти
        </Link>
      </p>
    </>
  );
};

export default Register;
