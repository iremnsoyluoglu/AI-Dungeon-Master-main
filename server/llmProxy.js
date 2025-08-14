const express = require("express");
const fetch = require("node-fetch");
require("dotenv").config();

const router = express.Router();

router.post("/", async (req, res) => {
  const { prompt, temperature = 0.7, max_tokens = 2000 } = req.body;
  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo-instruct",
        prompt,
        temperature,
        max_tokens,
      }),
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
