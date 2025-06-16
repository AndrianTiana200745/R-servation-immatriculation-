import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import Immatriculation from './components/Immatriculation';



export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/home" element={<Home />} />
      <Route path="/immatriculation" element={<Immatriculation />} />
      <Route path="*" element={<div className="text-center mt-10 text-xl text-red-600">Page introuvable</div>} />
    </Routes>
  );
}
