// Example: Vulnerable Application showing common AI Anti-Patterns

import express from 'express';
import cors from 'cors';

const app = express();

// Anti-Pattern 01: API Key exposed in client prefix
export const PUBLIC_STRIPE_KEY = process.env.NEXT_PUBLIC_STRIPE_SECRET_KEY;

// Anti-Pattern 06: Open wildcard CORS
app.use(cors({ origin: '*' }));

// Anti-Pattern 03: SQL Injection via string interpolation
app.get('/api/users', async (req, res) => {
  const email = req.query.email;
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  // const users = await db.query(query);
  res.json({ query });
});

// Anti-Pattern 12: N+1 query loop
app.get('/api/posts-with-authors', async (req, res) => {
  const posts: any[] = [];
  // posts.forEach(async (p) => { await db.users.findById(p.authorId); });
  res.json(posts);
});

// Anti-Pattern 13: Hardcoded static cache without jitter (Stampede risk)
app.post('/api/cache-data', async (req, res) => {
  const redis: any = {};
  // redis.set("hot_key", "data", 3600); // exactly 1 hour, detonates all at once!
  res.json({ ok: true });
});
