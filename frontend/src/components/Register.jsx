import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import M from 'materialize-css';

export default function Register() {
  const [form, setForm] = useState({
    nom: '',
    prenom: '',
    email: '',
    password: '',
    role: 'utilisateur',
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const elems = document.querySelectorAll('select');
    M.FormSelect.init(elems);
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('https://localhost:5080/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Échec de l'inscription");
      } else {
        navigate('/login');
      }
    } catch (err) {
      console.error(err);
      setError('Erreur réseau');
    }
  };

  return (
    <div className="container">
      <div className="row">
        <form onSubmit={handleSubmit} className="col s12 m8 offset-m2 l6 offset-l3 z-depth-2 card-panel">
          <h4 className="center-align">Inscription</h4>

          {error && <p className="red-text center">{error}</p>}

          <div className="input-field">
            <input id="nom" name="nom" type="text" value={form.nom} onChange={handleChange} required />
            <label htmlFor="nom">Nom</label>
          </div>

          <div className="input-field">
            <input id="prenom" name="prenom" type="text" value={form.prenom} onChange={handleChange} required />
            <label htmlFor="prenom">Prénom</label>
          </div>

          <div className="input-field">
            <input id="email" name="email" type="email" value={form.email} onChange={handleChange} required />
            <label htmlFor="email">Email</label>
          </div>

          <div className="input-field">
            <input id="password" name="password" type="password" value={form.password} onChange={handleChange} required />
            <label htmlFor="password">Mot de passe</label>
          </div>

          <div className="input-field">
            <select name="role" value={form.role} onChange={handleChange}>
              <option value="utilisateur">Utilisateur</option>
              <option value="admin">Admin</option>
            </select>
            <label>Rôle</label>
          </div>

          <button type="submit" className="btn waves-effect waves-light blue w-100">
            S'inscrire
          </button>

          <p className="center-align grey-text text-darken-1" style={{ marginTop: '20px' }}>
            Déjà un compte ?{' '}
            <Link to="/login" className="blue-text text-darken-2">Connectez-vous ici</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
