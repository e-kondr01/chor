import { Layout } from "antd";
import { Outlet } from "react-router-dom";
import styles from "./auth-layout.module.css";

const AuthLayout = () => {
  return (
    <Layout className={styles.layout}>
      <div className={styles.formContainer}>
        <Outlet />
      </div>
    </Layout>
  );
}

export default AuthLayout;