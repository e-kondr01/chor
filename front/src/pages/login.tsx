import { Input, Button, Form } from "antd";
import { useForm } from "antd/es/form/Form";
import styles from './login.module.css'
import { Link } from "react-router-dom";
import { RoutePaths } from "../lib/routes";
import { authAPI } from "../api";
import { formErrorsHandler } from "../lib/form-errors-handler";
import { useState } from "react";

const Login = () => {
    const [form] = useForm();
    const [formError, setFormError] = useState<string>('')

    const onSubmit = async () => {
        const fields = form.getFieldsValue(true);
        try {
            await authAPI.login(fields)
        } catch (error) {
            formErrorsHandler(form, error?.response?.data, setFormError)
        }
    }


  return (
    <>
      <Form requiredMark={false} form={form} onFinish={onSubmit} className={styles.login}>
        <Form.Item
          label="Логин"
          name="username"
          rules={[{ required: true, message: 'Введите логин' }]}
          labelCol={{span: 24}}
        >
          <Input type="email" />
        </Form.Item>
        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: 'Введите пароль' }]}
          labelCol={{span: 24}}
        >
          <Input.Password />
        </Form.Item>
        {!!formError && <p className={styles.error}>{formError}</p>}
        <Form.Item>
          <Button type="primary" htmlType="submit" block size="large">
            Войти
          </Button>
        </Form.Item>
      </Form>
      <p className="fs-small white">Ещё нет аккаунта? <Link to={RoutePaths.REGISTER} className="white bold">Зарегистрироваться</Link></p>
    </>
  );
}

export default Login;