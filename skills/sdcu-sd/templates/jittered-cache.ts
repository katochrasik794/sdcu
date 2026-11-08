/**
 * Jittered Cache Expiration & Stale-While-Revalidate Engine
 * Eliminates cache stampedes by dispersing TTL expiration times randomly.
 */

export interface CacheEntry<T> {
  value: T;
  savedAt: number;
  softTtlMs: number;
  hardTtlMs: number;
}

export class JitteredCache<T> {
  private store = new Map<string, CacheEntry<T>>();

  constructor(
    private readonly baseTtlSeconds: number = 3600,
    private readonly maxJitterSeconds: number = 600
  ) {}

  /**
   * Computes a jittered expiration time:
   * TTL = Base TTL + UniformRandom(0, MaxJitter)
   */
  public getJitteredTtlSeconds(): number {
    const jitter = Math.floor(Math.random() * this.maxJitterSeconds);
    return this.baseTtlSeconds + jitter;
  }

  public set(key: string, value: T, customBaseTtl?: number): void {
    const base = customBaseTtl ?? this.baseTtlSeconds;
    const jitter = Math.floor(Math.random() * this.maxJitterSeconds);
    const ttlSeconds = base + jitter;

    this.store.set(key, {
      value,
      savedAt: Date.now(),
      softTtlMs: ttlSeconds * 1000,
      hardTtlMs: ttlSeconds * 2 * 1000, // 2x for stale serving
    });
  }

  /**
   * Stale-While-Revalidate fetch:
   * - If fresh: returns immediate cached value.
   * - If between soft and hard TTL: returns stale value immediately, triggers async refresh.
   * - If hard expired or missing: calls loader.
   */
  public async getOrFetch(
    key: string,
    loader: () => Promise<T>,
    onAsyncRefreshError?: (err: unknown) => void
  ): Promise<T> {
    const entry = this.store.get(key);
    const now = Date.now();

    if (entry) {
      const age = now - entry.savedAt;

      if (age < entry.softTtlMs) {
        // Cache is fresh
        return entry.value;
      }

      if (age < entry.hardTtlMs) {
        // Stale-While-Revalidate window: Return stale value immediately, refresh in background
        loader()
          .then((fresh) => this.set(key, fresh))
          .catch((err) => {
            if (onAsyncRefreshError) onAsyncRefreshError(err);
          });
        return entry.value;
      }
    }

    // Cache miss or hard expired: fetch fresh data synchronously
    const freshValue = await loader();
    this.set(key, freshValue);
    return freshValue;
  }

  public has(key: string): boolean {
    return this.store.has(key);
  }

  public delete(key: string): boolean {
    return this.store.delete(key);
  }

  public clear(): void {
    this.store.clear();
  }
}
