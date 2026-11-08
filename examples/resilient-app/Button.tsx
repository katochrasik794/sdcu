// Example: Crafted, Unslopped Frontend Component following SDCU 9-pass design

export function CraftedHero() {
  return (
    // Pass 1 & 2: Calm tinted neutral background, intentional spacing
    <div className="bg-zinc-950 text-zinc-100 p-12">
      {/* Pass 3: Quiet chrome with crisp 1px border instead of neon glow */}
      <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 p-8 shadow-sm">
        {/* Pass 3 & 4: Clean typography pill instead of emoji badge */}
        <span className="inline-flex items-center text-xs font-medium text-emerald-400 bg-emerald-950/40 border border-emerald-800/50 px-2.5 py-0.5 rounded-full">
          Release 2.0
        </span>
        {/* Pass 6: Punchy, human microcopy */}
        <h1 className="mt-4 text-2xl font-semibold tracking-tight text-zinc-100">
          Automate database failover and request coalescing
        </h1>
        {/* Pass 7 & 9: Deliberate single primary action */}
        <button className="mt-6 inline-flex items-center justify-center rounded-lg bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-900 transition-colors hover:bg-zinc-200">
          Deploy Cluster
        </button>
      </div>
    </div>
  );
}
