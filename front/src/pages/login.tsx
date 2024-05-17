import { Button, Flex, Form, Input, Spin } from "antd";
import { useForm } from "antd/es/form/Form";
import Modal from "antd/es/modal/Modal";
import { useState } from "react";
import { Link } from "react-router-dom";
import { authAPI } from "../api";
import { formErrorsHandler } from "../lib/form-errors-handler";
import { RoutePaths } from "../lib/routes";
import styles from "./auth.module.css";

const Login = () => {
  const [form] = useForm();
  const [formError, setFormError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [successModal, setSuccessModal] = useState(false);

  const onSubmit = async () => {
    const fields = form.getFieldsValue(true);
    try {
      setIsLoading(true);
      await authAPI.login(fields);
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
        footer={null}
        onCancel={() => {
          form.resetFields();
          setSuccessModal(false);
        }}
      >
        <p>Успех!</p>
        <img src="https://cataas.com/cat" className={styles.successCat} />
      </Modal>
      <Form
        requiredMark={false}
        form={form}
        onFinish={onSubmit}
        className={styles.login}
      >
        <Form.Item
          label="Логин"
          name="username"
          rules={[{ required: true, message: "Введите логин" }, { pattern: /^[^\d\W_]*[.,' -]*[^\d\W_]$/, message: 'В логине допускаются только латинские буквы' }]}
          labelCol={{ span: 24 }}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: "Введите пароль" }]}
          labelCol={{ span: 24 }}
        >
          <Input.Password />
        </Form.Item>
        {!!formError && <p className={styles.error}>{formError}</p>}
        <Form.Item>
          <Button type="primary" htmlType="submit" block disabled={isLoading}>
            {isLoading ? <Flex gap={16} align="center" justify="center"><Spin />Войти</Flex> : 'Войти'}
          </Button>
        </Form.Item>
      </Form>
      <p className="fs-small white">
        Ещё нет аккаунта?{" "}
        <Link to={RoutePaths.REGISTER} className="white bold">
          Зарегистрироваться
        </Link>
      </p>
    </>
  );
};

export default Login;
