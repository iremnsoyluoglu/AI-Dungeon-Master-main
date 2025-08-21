const express = require('express');
const router = express.Router();
const multer = require('multer');
const AIScenarioGenerator = require('../../server/aiScenarioGenerator');

// Multer configuration for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    // Allow text files
    if (file.mimetype === 'text/plain' || 
        file.mimetype === 'text/markdown' || 
        file.mimetype === 'application/json') {
      cb(null, true);
    } else {
      cb(new Error('Only text files are allowed'), false);
    }
  }
});

// Get AI scenarios
router.get('/', async (req, res) => {
  try {
    const scenarios = await AIScenarioGenerator.getScenarios();
    res.json({
      success: true,
      scenarios: scenarios
    });
  } catch (error) {
    console.error('Error loading AI scenarios:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to load AI scenarios' 
    });
  }
});

// Generate new AI scenario
router.post('/generate', upload.single('file'), async (req, res) => {
  try {
    // FormData'dan gelen verileri işle
    const { prompt, theme, difficulty, genre } = req.body;
    
    // Dosya yükleme kontrolü
    let fileContent = '';
    if (req.file) {
      fileContent = req.file.buffer.toString('utf8');
      console.log('File uploaded:', req.file.originalname, 'Size:', req.file.size);
    }
    
    // Prompt'u birleştir
    const finalPrompt = fileContent ? `${fileContent}\n\n${prompt || ''}` : (prompt || 'Epik bir macera');
    
    console.log('Generating scenario with:', {
      prompt: finalPrompt,
      theme,
      difficulty,
      genre
    });
    
    const scenario = await AIScenarioGenerator.generateScenario(finalPrompt, theme, difficulty, genre);
    const saved = await AIScenarioGenerator.saveScenario(scenario);
    
    if (saved) {
      res.json({
        success: true,
        scenario: scenario
      });
    } else {
      res.status(500).json({ 
        success: false, 
        error: 'Failed to save generated scenario' 
      });
    }
  } catch (error) {
    console.error('Error generating AI scenario:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to generate scenario' 
    });
  }
});

module.exports = router;
