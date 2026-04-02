// test-evaluate-api.js
// Node.js script to test /api/evaluate endpoint
const axios = require('axios');

async function testEvaluate() {
  const payload = {
    query: "How do I reset my password?",
    context: ["User account management", "Password reset policy"],
    output: "To reset your password, go to settings and click 'Reset Password'.",
    expected_output: "User should be able to reset password via settings.",
    metric: "all"
  };

  try {
    const res = await axios.post('http://localhost:3001/api/evaluate', payload, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000
    });
    console.log('✅ Success:', res.data);
  } catch (err) {
    if (err.response) {
      console.error('❌ API Error:', err.response.status, err.response.data);
    } else {
      console.error('❌ Request Error:', err.message);
    }
    process.exit(1);
  }
}

testEvaluate();
