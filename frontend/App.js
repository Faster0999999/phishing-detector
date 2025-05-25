import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:5000/api/scan", { url });
      setResult(res.data);
    } catch (error) {
      setResult({ phishing: true, reason: 'Error connecting to backend' });
    }
  };

  return (
    <div className="App">
      <h1>Phishing Detection</h1>
      <input
        value={url}
        onChange={e => setUrl(e.target.value)}
        placeholder="Enter URL to scan"
      />
      <button onClick={handleSubmit}>Scan URL</button>
      {result && (
        <div>
          <h3>{result.phishing ? "⚠️ Phishing Detected" : "✅ Safe URL"}</h3>
          <p>{result.reason}</p>
        </div>
      )}
    </div>
  );
}

export default App;





