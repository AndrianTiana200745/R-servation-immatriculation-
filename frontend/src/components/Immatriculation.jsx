import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ImmatriculationTable() {
  const [immatriculations, setImmatriculations] = useState([]);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchImmatriculations = async () => {
    setLoading(true);
    try {
      const res = await fetch(`https://localhost:5080/immatriculation/disponible?page=${page}&limit=${limit}&search=${search}`, {
        credentials: 'include',
      });
      const data = await res.json();
      setImmatriculations(data.data);
      setTotalPages(data.pages);
    } catch (error) {
      console.error("Erreur lors du chargement :", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImmatriculations();
  }, [page, search]);

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handleLogout = async () => {
    try {
      const res = await fetch('https://localhost:5080/auth/logout', {
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

  const handleReserve = async (immatriculation_id) => {
    try {
      const res = await fetch('https://localhost:5080/reservation/creer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ immatriculation_id }),
      });

      const data = await res.json();

      if (res.ok) {
        alert('Réservation réussie !');
        fetchImmatriculations();
      } else {
        alert(data.message || 'Erreur lors de la réservation');
      }
    } catch (err) {
      console.error(err);
      alert('Erreur réseau');
    }
  };

  return (
    <div className="container">
      <button onClick={handleLogout} className="btn red lighten-1 waves-effect waves-light" style={{ marginTop: '25px' }}>
        Déconnexion
      </button>
      <h4 className="center-align">Immatriculations Disponibles</h4>

      <div className="input-field">
        <input
          type="text"
          placeholder="Rechercher un numéro"
          value={search}
          onChange={handleSearchChange}
        />
      </div>

      {loading ? (
        <div className="center-align">Chargement...</div>
      ) : (
        <table className="highlight centered">
          <thead>
            <tr>
              <th>Numéro</th>
              <th>Centre</th>
              <th>Série</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {immatriculations.map((item) => (
              <tr key={item.id}>
                <td>{item.numero}</td>
                <td>{item.centre}</td>
                <td>{item.serie}</td>
                <td>
                  <button className="btn waves-effect" onClick={() => handleReserve(item.id)}>
                    Dédier
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="center-align" style={{ marginTop: '20px' }}>
        <button className="btn waves-effect" disabled={page <= 1} onClick={() => setPage(page - 1)}>
          Précédent
        </button>
        <span style={{ margin: '0 15px' }}>Page {page} / {totalPages}</span>
        <button className="btn waves-effect" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>
          Suivant
        </button>
      </div>
    </div>
  );
}
