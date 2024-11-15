import './App.css';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import Landing from './Screens/Landing';
import Home from './Screens/Home';
import Layout from './components/ui/Layout';
import Auth from './Screens/Auth';
import Compose from './Screens/Compose';
import FocusedHome from './Screens/FocusedHome';

function App() {
  return (
    <BrowserRouter>
        <Routes>
          <Route path='/' element={<Layout />}>
            <Route index element={<Landing />} />
            <Route path='auth' element={<Auth />} />
            <Route path='home' element={<Home />} />
            <Route path='home/:blogId' element={<FocusedHome />} />
            <Route path='compose' element={<Compose />} />
            <Route path='*' element={<>Error</>} />
          </Route>
        </Routes>
    </BrowserRouter>
  )
}

export default App
