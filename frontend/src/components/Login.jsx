import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import M from 'materialize-css';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    M.AutoInit(); // Initialisation des composants Materialize
  }, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('https://localhost:5080/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) setError(data.error || 'Échec de la connexion');
      else navigate('/immatriculation');
    } catch (err) {
      console.error(err);
      setError('Erreur réseau');
    }
  };

  return (
    <div className="container" style={{ maxWidth: '500px', marginTop: '50px' }}>
      <div className="card z-depth-2">
        <div className="card-content">
          <span className="card-title center">Connexion</span>

          {error && (
            <div className="card-panel red lighten-4 red-text text-darken-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="input-field">
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                required
              />
              <label htmlFor="email">Email</label>
            </div>

            <div className="input-field">
              <input
                id="password"
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                required
              />
              <label htmlFor="password">Mot de passe</label>
            </div>

            <button type="submit" className="btn waves-effect waves-light full-width">
              Se connecter
            </button>
          </form>
        </div>

        <div className="card-action center">
          <p>
            Pas encore de compte ?{' '}
            <Link to="/register" className="blue-text text-darken-2">
              Inscrivez-vous ici
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
