// Example: Production Resilient Backend following SDCU principles

import express from 'express';
import cors from 'cors';
import { SingleFlightGroup } from '../../skills/sdcu-sd/templates/singleflight';
import { CircuitBreaker } from '../../skills/sdcu-sd/templates/circuit-breaker';
import { JitteredCache } from '../../skills/sdcu-sd/templates/jittered-cache';

const app = express();

// 01: Secret keys kept strictly server-side
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;

// 06: Restricted explicit CORS whitelist
const ALLOWED_ORIGINS = ['https://myapp.com', 'https://admin.myapp.com'];
app.use(cors({ origin: ALLOWED_ORIGINS, credentials: true }));

// Resilience engines
const singleFlight = new SingleFlightGroup();
const circuitBreaker = new CircuitBreaker();
const cache = new JitteredCache<any>(3600, 600); // 1hr base + up to 10m random jitter

// 03: Parameterized SQL queries (No injection)
app.get('/api/users', async (req, res) => {
  const email = req.query.email as string;
  // const users = await db.query('SELECT * FROM users WHERE email = $1', [email]);
  res.json({ email });
});

// Cache-to-DB resilience: SingleFlight coalescing prevents stampedes
app.get('/api/product/:id', async (req, res) => {
  const id = req.params.id;

  const data = await singleFlight.do(`product:${id}`, async () => {
    return cache.getOrFetch(`product:${id}`, async () => {
      return circuitBreaker.execute(async () => {
        // Query primary database safely
        return { id, name: 'Product ' + id };
      }, () => ({ id, name: 'Fallback Product (Cached/Degraded)' }));
    });
  });

  res.json(data);
});
