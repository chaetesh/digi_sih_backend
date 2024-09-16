const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// Set up multer for file uploads
const upload = multer({ dest: 'uploads/' });

// Route to process the OCR request
app.post('/process-file', upload.single('file'), (req, res) => {
  const filePath = req.file.path;
  const outputFolder = 'uploads/';

  // Command to run Python script
  const pythonCommand = `python ocr_script.py ${filePath} ${outputFolder}`;

  // Run the Python script and return OCR results
  exec(pythonCommand, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('Internal Server Error');
    }

    if (stderr) {
      console.error(`Stderr: ${stderr}`);
    }

    // Parse Python script output
    let result;
    try {
      result = JSON.parse(stdout);
    } catch (parseError) {
      return res.status(500).send('Error parsing Python script output');
    }

    // Delete the uploaded file after processing
    fs.unlink(filePath, (err) => {
      if (err) console.error(err);
    });

    // Return the result
    res.json(result);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
