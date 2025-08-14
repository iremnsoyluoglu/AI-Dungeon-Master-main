const express = require("express");
const cors = require("cors");
const path = require("path");

// Import the main server app from server/index.js
const apiApp = require("./server/index.js");

const app = express();

// CORS middleware
app.use(cors());
app.use(express.json());

// Serve static files from the dist directory (if built)
app.use(express.static(path.join(__dirname, "dist")));

// Mount the API app at /api
app.use("/api", apiApp);

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    server: "AI Dungeon Master API",
    version: "1.0.0",
  });
});

// Serve the React app for any non-API routes
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "dist", "index.html"));
});

const PORT = process.env.PORT || 5005;

app
  .listen(PORT, () => {
    console.log(`🚀 AI Dungeon Master Server running on port ${PORT}`);
    console.log(`📱 Frontend should be accessible at http://localhost:3001`);
    console.log(`🔧 API endpoints available at http://localhost:${PORT}/api`);
  })
  .on("error", (err) => {
    if (err.code === "EADDRINUSE") {
      console.log(`❌ Port ${PORT} is already in use. Trying port ${PORT + 1}`);
      app.listen(PORT + 1, () => {
        console.log(`🚀 AI Dungeon Master Server running on port ${PORT + 1}`);
        console.log(`📱 Frontend should be accessible at http://localhost:3001`);
        console.log(`🔧 API endpoints available at http://localhost:${PORT + 1}/api`);
      }).on("error", (err2) => {
        if (err2.code === "EADDRINUSE") {
          console.log(`❌ Port ${PORT + 1} is also in use. Trying port ${PORT + 2}`);
          app.listen(PORT + 2, () => {
            console.log(`🚀 AI Dungeon Master Server running on port ${PORT + 2}`);
            console.log(`📱 Frontend should be accessible at http://localhost:3001`);
            console.log(`🔧 API endpoints available at http://localhost:${PORT + 2}/api`);
          });
        } else {
          console.error("Server error:", err2);
        }
      });
    } else {
      console.error("Server error:", err);
    }
  });
