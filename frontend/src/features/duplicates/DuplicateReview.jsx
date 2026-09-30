import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './duplicates.css';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
});

function scoreLabel(score) {
  if (score >= 0.8) return 'Very similar';
  if (score >= 0.6) return 'Likely related';
  return 'Possibly related';
}

export default function DuplicateReview({ applicationId }) {
  const [matches, setMatches] = useState([]);
  const [threshold, setThreshold] = useState(0.45);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadMatches = async () => {
    if (!applicationId) return;
    setLoading(true);
    setError('');
    try {
      const response = await api.get(
        `/applications/${applicationId}/possible-duplicates/`,
        { params: { threshold } }
      );
      setMatches(response.data.matches || []);
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
        'Unable to check for possible duplicates.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMatches();
  }, [applicationId]);

  return (
    <section className="duplicate-review">
      <div className="duplicate-header">
        <div>
          <h3>Duplicate check</h3>
          <p>Find applications that may represent the same opportunity.</p>
        </div>
        <button
          type="button"
          className="duplicate-refresh"
          onClick={loadMatches}
          disabled={loading || !applicationId}
        >
          {loading ? 'Checking…' : 'Check again'}
        </button>
      </div>

      <div className="duplicate-controls">
        <label htmlFor="duplicate-threshold">
          Match threshold: <strong>{threshold.toFixed(2)}</strong>
        </label>
        <input
          id="duplicate-threshold"
          type="range"
          min="0.2"
          max="0.9"
          step="0.05"
          value={threshold}
          onChange={(event) => setThreshold(Number(event.target.value))}
          onMouseUp={loadMatches}
          onKeyUp={loadMatches}
        />
      </div>

      {error && <div className="duplicate-error">{error}</div>}

      {!loading && !error && matches.length === 0 && (
        <div className="duplicate-empty">
          No possible duplicates were found at this threshold.
        </div>
      )}

      <div className="duplicate-list">
        {matches.map((match) => (
          <article key={match.application_id} className="duplicate-card">
            <div className="duplicate-card-main">
              <strong>{match.company}</strong>
              <span>{match.role}</span>
            </div>
            <div className="duplicate-score">
              <span>{scoreLabel(match.score)}</span>
              <strong>{Math.round(match.score * 100)}%</strong>
            </div>
            <div className="duplicate-reasons">
              {match.reasons.map((reason) => (
                <span key={reason}>{reason}</span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
