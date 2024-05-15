import { Input, Button, Form } from "antd";
import { useForm } from "antd/es/form/Form";
import styles from './login.module.css'
import { Link } from "react-router-dom";
import { RoutePaths } from "../lib/routes";

const Login = () => {
    const [form] = useForm();

    const onSubmit = () => {
        const fields = form.getFieldsValue(true);
        // TODO: api call
        try {
            console.log(fields);
        } catch (error) {
            console.error(error);
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