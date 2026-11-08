/**
 * Production Circuit Breaker Implementation
 * Prevents cascading service failures and database stampedes.
 */

export enum CircuitState {
  CLOSED = 'CLOSED',       // Normal operation: requests pass through
  OPEN = 'OPEN',           // Tripped: fail immediately without hitting target
  HALF_OPEN = 'HALF_OPEN', // Testing: permit canary requests to verify recovery
}

export interface CircuitBreakerOptions {
  failureThreshold: number; // e.g. 5 consecutive failures
  cooldownPeriodMs: number; // e.g. 10000ms before trying Half-Open
  halfOpenMaxSuccesses: number; // e.g. 2 successful probes to close
}

export class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private consecutiveFailures = 0;
  private successfulProbes = 0;
  private lastFailureTime = 0;

  constructor(private readonly options: CircuitBreakerOptions = {
    failureThreshold: 5,
    cooldownPeriodMs: 10000,
    halfOpenMaxSuccesses: 2,
  }) {}

  public getState(): CircuitState {
    if (this.state === CircuitState.OPEN) {
      const now = Date.now();
      if (now - this.lastFailureTime > this.options.cooldownPeriodMs) {
        this.state = CircuitState.HALF_OPEN;
        this.successfulProbes = 0;
      }
    }
    return this.state;
  }

  public async execute<T>(action: () => Promise<T>, fallback?: () => Promise<T> | T): Promise<T> {
    const currentState = this.getState();

    if (currentState === CircuitState.OPEN) {
      if (fallback) {
        return fallback();
      }
      throw new Error(`CircuitBreaker is OPEN - request rejected to protect downstream resource`);
    }

    try {
      const result = await action();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      if (fallback) {
        return fallback();
      }
      throw error;
    }
  }

  private onSuccess(): void {
    if (this.state === CircuitState.HALF_OPEN) {
      this.successfulProbes++;
      if (this.successfulProbes >= this.options.halfOpenMaxSuccesses) {
        this.state = CircuitState.CLOSED;
        this.consecutiveFailures = 0;
      }
    } else {
      this.consecutiveFailures = 0;
    }
  }

  private onFailure(): void {
    this.consecutiveFailures++;
    this.lastFailureTime = Date.now();
    if (this.state === CircuitState.HALF_OPEN || this.consecutiveFailures >= this.options.failureThreshold) {
      this.state = CircuitState.OPEN;
    }
  }
}
