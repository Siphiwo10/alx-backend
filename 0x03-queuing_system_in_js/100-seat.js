const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Create Redis client and promisify methods
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Set initial available seats
const initialSeats = 50;
client.set('available_seats', initialSeats);
let reservationEnabled = true;

// Create Kue queue
const queue = kue.createQueue();

// Redis functions to reserve seats and get available seats
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
};

// Kue job processing
queue.process('reserve_seat', async (job, done) => {
  try {
    let availableSeats = await getCurrentAvailableSeats();

    if (availableSeats <= 0) {
      job.failed(new Error('Not enough seats available'));
      console.log(`Seat reservation job ${job.id} failed: Not enough seats available`);
      done(new Error('Not enough seats available'));
      return;
    }

    availableSeats -= 1;
    await reserveSeat(availableSeats);

    if (availableSeats === 0) {
      reservationEnabled = false; // Disable reservations when seats are exhausted
    }

    console.log(`Seat reservation job ${job.id} completed`);
    done();
  } catch (error) {
    console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
    done(error);
  }
});

// Routes
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    await getCurrentAvailableSeats();
    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

