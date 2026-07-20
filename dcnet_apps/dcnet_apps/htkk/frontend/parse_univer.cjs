const fs = require('fs');
const res = JSON.parse(fs.readFileSync('./test_sample.json', 'utf8'));
const sheet = res.message.sheets['sheet-01'];
console.log("Got " + Object.keys(sheet.cellData).length + " rows.");
