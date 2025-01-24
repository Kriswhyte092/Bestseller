import express from 'express';
import dotenv from 'dotenv';
import { connectDB } from './config/db.js';

dotenv.config();

const app = express();

// Middleware to parse incoming JSON requests
app.use(express.json());






app.listen(4000, () => {
  connectDB();
  console.log('Server is running on http://localhost:4000');
});

