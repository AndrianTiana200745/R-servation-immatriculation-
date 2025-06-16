import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function Home() {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleLogout = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5080/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });
      const data = await res.json();
      if (res.ok) {
        navigate('/login');
      } else {
        setError(data.message || 'Déconnexion échouée');
      }
    } catch (err) {
      console.error(err);
      setError('Erreur réseau lors de la déconnexion');
    }
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col s12 m8 offset-m2 l6 offset-l3 card-panel center-align z-depth-2" style={{ marginTop: '80px' }}>
          <h4>Bienvenue sur la page d'accueil</h4>
          <p className="grey-text text-darken-1">Voici le tableau de bord principal de votre application.</p>

          {error && <p className="red-text" style={{ marginTop: '15px' }}>{error}</p>}

          <button onClick={handleLogout} className="btn red lighten-1 waves-effect waves-light" style={{ marginTop: '25px' }}>
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  );
}
