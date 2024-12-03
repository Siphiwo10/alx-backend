import { createClient } from 'redis';

// Create a Redis client
const client = createClient();

// Event: When the client connects successfully
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Event: When the client encounters an error
client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});
