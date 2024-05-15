import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import { themeConfig } from './lib/themeConfig.ts'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
    <ConfigProvider theme={themeConfig}>
      <App />
    </ConfigProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
