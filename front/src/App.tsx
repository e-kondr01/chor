import './App.css'
import { Navigate, Route, Routes } from 'react-router-dom'
import { RoutePaths } from './lib/routes'
import AuthLayout from './layout/auth-layout'
import Login from './pages/login'
import Register from './pages/register'

function App() {

  return (
    <Routes>
      <Route path={RoutePaths.MAIN} element={<Navigate to={RoutePaths.LOGIN}/>} />
      <Route element={<AuthLayout />}>
        <Route path={RoutePaths.LOGIN} element={<Login />} />
        <Route path={RoutePaths.REGISTER} element={<Register />} />
      </Route>
    </Routes>
  )
}

export default App
