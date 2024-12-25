const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const csv = require('csv-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static('public'));

// CSV file setup
const EXPENSE_FILE = 'expenses.csv';
const csvWriter = createCsvWriter({
  path: EXPENSE_FILE,
  header: [
    { id: 'date', title: 'Date' },
    { id: 'amount', title: 'Amount' },
    { id: 'category', title: 'Category' }
  ]
});

// Initialize CSV file if it doesn't exist
if (!fs.existsSync(EXPENSE_FILE)) {
  csvWriter.writeRecords([]);
}

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/add-expense', async (req, res) => {
  try {
    const { date, amount, category } = req.body;
    await csvWriter.writeRecords([{ date, amount, category }]);
    res.json({ status: 'success', message: 'Expense added successfully!' });
  } catch (error) {
    res.status(500).json({ status: 'error', message: error.message });
  }
});

app.get('/get-expenses', (req, res) => {
  const { month, category } = req.query;
  const expenses = [];

  fs.createReadStream(EXPENSE_FILE)
    .pipe(csv())
    .on('data', (row) => {
      if ((!month || row.Date.startsWith(month)) &&
          (!category || row.Category === category)) {
        expenses.push(row);
      }
    })
    .on('end', () => {
      res.json(expenses);
    });
});

app.get('/generate-report', (req, res) => {
  const { month } = req.query;
  const expenses = [];

  fs.createReadStream(EXPENSE_FILE)
    .pipe(csv())
    .on('data', (row) => {
      if (!month || row.Date.startsWith(month)) {
        expenses.push(row);
      }
    })
    .on('end', () => {
      if (expenses.length === 0) {
        return res.json({ status: 'error', message: 'No data available for this month.' });
      }

      // Calculate category totals for client-side charting
      const categoryTotals = expenses.reduce((acc, curr) => {
        acc[curr.Category] = (acc[curr.Category] || 0) + parseFloat(curr.Amount);
        return acc;
      }, {});

      res.json({
        status: 'success',
        data: categoryTotals
      });
    });
});

app.listen(port, () => {
  console.log(`Expense tracker app running at http://localhost:${port}`);
});