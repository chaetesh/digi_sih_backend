const express = require("express");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = 3000;

// Step 1: Redirect user to DigiLocker Authorization URL
app.get("/login", (req, res) => {
  const authorizationUrl = `https://api.digitallocker.gov.in/public/oauth2/1/authorize`;

  const params = new URLSearchParams({
    response_type: "code",
    client_id: process.env.CLIENT_ID,
    redirect_uri: process.env.REDIRECT_URI,
    state: "random_string",
  });

  res.redirect(`${authorizationUrl}?${params}`);
});

// Step 2: Handle callback and exchange authorization code for access token
app.get("/callback", async (req, res) => {
  const { code } = req.query;

  if (!code) {
    return res.send("Authorization failed.");
  }

  try {
    const tokenResponse = await axios.post(
      "https://api.digitallocker.gov.in/public/oauth2/1/token",
      null,
      {
        params: {
          client_id: process.env.CLIENT_ID,
          client_secret: process.env.CLIENT_SECRET,
          grant_type: "authorization_code",
          code: code,
          redirect_uri: process.env.REDIRECT_URI,
        },
      }
    );

    const accessToken = tokenResponse.data.access_token;
    res.send(`Access Token: ${accessToken}`);
  } catch (error) {
    res.send("Error exchanging authorization code for token.");
  }
});

// Step 3: Get User Details using Access Token
app.get('/user-details', async (req, res) => {
  const accessToken = "AccessToken"; // pass access token

  try {
    // In real implementation, use axios to call DigiLocker API
    // const response = await axios.get('https://api.digitallocker.gov.in/public/oauth2/1/user', {
    //   headers: {
    //     Authorization: `Bearer ${accessToken}`,
    //   },
    // });

    // Simulated response data
    const userDetails = {
      digilockerid: '123e4567-e89b-12d3-a456-426655440000',
      name: 'Sunil Kumar',
      dob: '31121970',
      gender: 'M',
      eaadhaar: 'Y',
      reference_key: '2a33349e7e606a8ad2e30e3c84521f9377450cf09083e162e0a9b1480ce0f972',
    };

    res.json(userDetails);
  } catch (error) {
    res.send('Error fetching user details.');
  }
});

// Step 4: Get List of Issued Documents
app.get('/issued-documents', async (req, res) => {
  const accessToken = "AcesssToken"; // pass access token

  try {
    // In real implementation, use axios to call DigiLocker API
    // const response = await axios.get('https://api.digitallocker.gov.in/public/oauth2/2/files/issued', {
    //   headers: {
    //     Authorization: `Bearer ${accessToken}`,
    //   },
    // });

    // Simulated response data
    const issuedDocuments = {
      items: [
        {
          name: "Class XII Marksheet",
          type: "file",
          size: "",
          date: "2015-05-12T15:50:38Z",
          parent: "",
          mime: "application/pdf",
          uri: "in.gov.cbse-HSCER-201412345678",
          doctype: "HSCER",
          description: "Class XII Marksheet",
          issuerid: "in.gov.cbse",
          issuer: "CBSE",
        },
        {
          name: "Income Certificate",
          type: "file",
          size: "",
          date: "2015-05-12T15:50:38Z",
          parent: "",
          mime: ["application/pdf", "application/xml"],
          uri: "in.gov.delhi-INCER-98765432",
          doctype: "INCER",
          description: "Income Certificate",
          issuerid: "in.gov.delhi",
          issuer: "Delhi eDistrict",
        },
      ],
    };

    res.json(issuedDocuments);
  } catch (error) {
    res.send('Error fetching issued documents.');
  }
});


// Step 5: Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});