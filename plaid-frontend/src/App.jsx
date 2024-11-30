import { useState } from 'react'
import './App.css'
import { usePlaidLink } from 'react-plaid-link'

function App() {
  // Store the link token when we get it
  const [linkToken, setLinkToken] = useState(null);

  function fetchLinkToken() {
    fetch('http://localhost:5000/api/getlinktoken')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log("Got link token:", data);
        setLinkToken(data.link_token);
      })
      .catch(error => {
        console.error('Error getting link token:', error);
      });
  }

  const onSuccess = (public_token, metadata) => {
    console.log("Got public token:", public_token);
  };

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess,
  });

  return (
    <>
      <button 
        onClick={() => {
          if (linkToken) open()
          else fetchLinkToken()
        }}
        // onClick={fetchLinkToken}
      >
        Connect your bank account
      </button>
    </>
  )
}

export default App