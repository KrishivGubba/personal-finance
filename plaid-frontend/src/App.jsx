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
    fetch('http://localhost:5000/api/sendaccesstoken', {
      method: "POST",
      body: JSON.stringify({
        publicToken: public_token
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    .then(response => {       
      if (!response.ok) {
        throw new Error('Failed to exchange token');
      }
      return response.json();  
    })
    .then(data => {           
      console.log("Successfully connected bank account");
    })
    .catch(error => {
      console.log("Some error occurred: ", error);
    });
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