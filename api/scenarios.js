const express = require('express');
const router = express.Router();

// Load scenarios endpoint
router.get('/', (req, res) => {
  try {
    const scenarios = require('../data/enhanced_scenarios.json');
    res.json({
      success: true,
      scenarios: scenarios
    });
  } catch (error) {
    console.error('Error loading scenarios:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to load scenarios' 
    });
  }
});

// Toggle favorite endpoint
router.post('/:scenarioId/toggle-favorite', (req, res) => {
  try {
    const { scenarioId } = req.params;
    // Mock favorite toggle - in real app this would update database
    res.json({ 
      success: true, 
      message: 'Favorite status updated' 
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: 'Failed to toggle favorite' 
    });
  }
});

module.exports = router;
