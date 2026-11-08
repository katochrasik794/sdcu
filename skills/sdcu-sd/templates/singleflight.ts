/**
 * Production SingleFlight (Request Coalescing) Implementation
 * Ensures that if 10,000 concurrent requests ask for the same missing key,
 * only 1 database query is executed, and the result is shared across all callers.
 */

export class SingleFlightGroup {
  private inFlight = new Map<string, Promise<any>>();

  /**
   * Execute coalesced call for a given key.
   * If a call with this key is already running, wait for it and share its result.
   */
  public async do<T>(key: string, fn: () => Promise<T>): Promise<T> {
    const existing = this.inFlight.get(key);
    if (existing) {
      return existing as Promise<T>;
    }

    const promise = (async () => {
      try {
        return await fn();
      } finally {
        this.inFlight.delete(key);
      }
    })();

    this.inFlight.set(key, promise);
    return promise;
  }

  /**
   * Return number of currently active in-flight coalesced operations.
   */
  public get activeCalls(): number {
    return this.inFlight.size;
  }
}

