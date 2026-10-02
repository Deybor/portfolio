const heart =
  "M 0.0 -24.0 L 0.0 -24.4 L 0.2 -25.6 L 0.6 -27.5 L 1.4 -29.9 L 2.6 -32.7 L 4.3 -35.6 L 6.6 -38.6 L 9.3 -41.2 L 12.6 -43.5 L 16.3 -45.1 L 20.2 -45.9 L 24.4 -46.0 L 28.5 -45.2 L 32.5 -43.5 L 36.3 -41.1 L 39.6 -38.0 L 42.3 -34.2 L 44.3 -30.1 L 45.6 -25.6 L 46.0 -20.9 L 45.6 -16.1 L 44.3 -11.3 L 42.3 -6.6 L 39.6 -2.1 L 36.3 2.3 L 32.5 6.6 L 28.5 10.8 L 24.4 14.8 L 20.2 18.7 L 16.3 22.5 L 12.6 26.1 L 9.3 29.7 L 6.6 33.0 L 4.3 36.1 L 2.6 38.9 L 1.4 41.4 L 0.6 43.3 L 0.2 44.8 L 0.0 45.7 L 0.0 46.0 L -0.0 45.7 L -0.2 44.8 L -0.6 43.3 L -1.4 41.4 L -2.6 38.9 L -4.3 36.1 L -6.6 33.0 L -9.3 29.7 L -12.6 26.1 L -16.3 22.5 L -20.2 18.7 L -24.4 14.8 L -28.5 10.8 L -32.5 6.6 L -36.3 2.3 L -39.6 -2.1 L -42.3 -6.6 L -44.3 -11.3 L -45.6 -16.1 L -46.0 -20.9 L -45.6 -25.6 L -44.3 -30.1 L -42.3 -34.2 L -39.6 -38.0 L -36.3 -41.1 L -32.5 -43.5 L -28.5 -45.2 L -24.4 -46.0 L -20.2 -45.9 L -16.3 -45.1 L -12.6 -43.5 L -9.3 -41.2 L -6.6 -38.6 L -4.3 -35.6 L -2.6 -32.7 L -1.4 -29.9 L -0.6 -27.5 L -0.2 -25.6 L -0.0 -24.4 Z";

function DimH({ x1, x2, y, label }: { x1: number; x2: number; y: number; label: string }) {
  return (
    <g fill="none" stroke="currentColor" strokeWidth="0.8">
      <line x1={x1} y1={y} x2={x2} y2={y} />
      <line x1={x1} y1={y - 5} x2={x1} y2={y + 5} />
      <line x1={x2} y1={y - 5} x2={x2} y2={y + 5} />
      <text
        x={(x1 + x2) / 2}
        y={y - 8}
        textAnchor="middle"
        fontSize="11"
        fill="currentColor"
        stroke="none"
      >
        {label}
      </text>
    </g>
  );
}

export function NestViews() {
  return (
    <div className="sheet-views">
      <figure className="view">
        <svg viewBox="0 0 250 290" role="img" aria-label="Front view. Proposed Nest stud, 10 by 11 millimetres.">
          <g transform="translate(118 148)">
            <g transform="translate(-14 6) scale(1.52 1.58)">
              <path d={heart} fill="var(--color-metal)" />
            </g>
            <path d={heart} fill="var(--color-stone)" stroke="currentColor" strokeWidth="1.2" />
            <path d="M0 -6 L0 22" fill="none" stroke="currentColor" strokeWidth="0.7" opacity="0.4" />
            <path d="M-20 -4 L0 24 L20 -4" fill="none" stroke="currentColor" strokeWidth="0.7" opacity="0.4" />
            <path d="M-28 6 C-8 0 8 0 28 6" fill="none" stroke="currentColor" strokeWidth="0.6" opacity="0.35" />
          </g>
          <DimH x1={36} x2={196} y={28} label="10.0" />
          <g fill="none" stroke="currentColor" strokeWidth="0.8">
            <line x1="214" y1="78" x2="214" y2="236" />
            <line x1="209" y1="78" x2="219" y2="78" />
            <line x1="209" y1="236" x2="219" y2="236" />
            <text x="226" y="162" fontSize="11" fill="currentColor" stroke="none">
              11.0
            </text>
          </g>
          <text x="46" y="262" fontSize="11" fill="currentColor">
            satin fold
          </text>
          <text x="150" y="262" fontSize="11" fill="currentColor">
            polished lip
          </text>
        </svg>
        <figcaption>Front · proposed</figcaption>
      </figure>
      <figure className="view">
        <svg viewBox="0 0 250 220" role="img" aria-label="Side view. Post length 10 millimetres, on the reverse.">
          <rect x="28" y="108" width="78" height="7" fill="var(--color-metal)" stroke="currentColor" strokeWidth="0.8" />
          <path
            d="M106 52 H138 C146 52 150 64 150 86 C150 112 142 128 136 146 H114 C108 128 106 112 106 86 C106 64 108 52 114 52 Z"
            fill="var(--color-stone)"
            stroke="currentColor"
            strokeWidth="1.1"
          />
          <path d="M110 124 H146 V150 H110 Z" fill="var(--color-metal)" stroke="currentColor" strokeWidth="0.8" />
          <DimH x1={28} x2={106} y={176} label="10.0 post" />
          <text x="128" y="176" textAnchor="middle" fontSize="11" fill="currentColor">
            4.2
          </text>
          <g fill="none" stroke="currentColor" strokeWidth="0.8">
            <line x1="168" y1="52" x2="168" y2="150" />
            <line x1="163" y1="52" x2="173" y2="52" />
            <line x1="163" y1="150" x2="173" y2="150" />
          </g>
          <text x="178" y="106" fontSize="11" fill="currentColor">
            11.0
          </text>
          <text x="125" y="204" textAnchor="middle" fontSize="11" fill="currentColor">
            post behind the fold
          </text>
        </svg>
        <figcaption>Side · schematic</figcaption>
      </figure>
      <figure className="view">
        <svg viewBox="0 0 250 250" role="img" aria-label="Back view. Post does not pass through the stone.">
          <g transform="translate(125 118)">
            <g transform="translate(-14 6) scale(1.52 1.58)">
              <path d={heart} fill="var(--color-ivory)" />
            </g>
            <path d={heart} fill="var(--color-stone)" stroke="currentColor" strokeWidth="1.15" />
            <circle cx="-28" cy="22" r="7" fill="var(--color-metal)" stroke="currentColor" strokeWidth="0.9" />
            <circle cx="-28" cy="22" r="2.2" fill="currentColor" />
          </g>
          <line x1="70" y1="150" x2="40" y2="190" stroke="currentColor" strokeWidth="0.7" />
          <text x="18" y="208" fontSize="11" fill="currentColor">
            post Ø 0.8
          </text>
          <text x="125" y="236" textAnchor="middle" fontSize="11" fill="currentColor">
            not through the stone
          </text>
        </svg>
        <figcaption>Back · post</figcaption>
      </figure>
    </div>
  );
}

export function PendantViews() {
  return (
    <div className="sheet-views two">
      <figure className="view">
        <svg viewBox="0 0 280 300" role="img" aria-label="Front view of the estimated Amara pendant.">
          <defs>
            <clipPath id="amara-stone">
              <path d={heart} />
            </clipPath>
          </defs>
          <g transform="translate(140 150)">
            <line x1="0" y1="-24" x2="0" y2="-78" stroke="currentColor" strokeWidth="1.5" />
            <circle cx="0" cy="-84" r="2.4" fill="currentColor" />
            <path d={heart} fill="var(--color-stone)" stroke="currentColor" strokeWidth="1.2" />
            <g clipPath="url(#amara-stone)">
              <rect x="-48" y="20" width="96" height="30" fill="var(--color-metal)" />
            </g>
            <path d={heart} fill="none" stroke="currentColor" strokeWidth="1.2" />
            <circle cx="-30" cy="-34" r="6.2" fill="var(--color-metal)" stroke="currentColor" strokeWidth="0.7" />
            <circle cx="30" cy="-34" r="6.2" fill="var(--color-metal)" stroke="currentColor" strokeWidth="0.7" />
          </g>
          <DimH x1={94} x2={186} y={40} label="8.0 stone" />
          <text x="140" y="268" textAnchor="middle" fontSize="11" fill="currentColor">
            cup 2.2 high · beads Ø 0.9
          </text>
          <text x="140" y="286" textAnchor="middle" fontSize="11" fill="currentColor">
            chain 395 + 50, not drawn full length
          </text>
        </svg>
        <figcaption>Front · estimated</figcaption>
      </figure>
      <figure className="view">
        <svg viewBox="0 0 240 280" role="img" aria-label="Side view of the estimated pendant, stone depth 4.5 millimetres.">
          <line x1="118" y1="28" x2="118" y2="78" stroke="currentColor" strokeWidth="1.5" />
          <path
            d="M100 86 C118 74 146 96 146 124 C146 156 128 176 118 186 C108 176 90 156 90 124 C90 96 98 86 100 86 Z"
            fill="var(--color-stone)"
            stroke="currentColor"
            strokeWidth="1.15"
          />
          <path d="M92 156 H144 V184 H92 Z" fill="var(--color-metal)" stroke="currentColor" strokeWidth="0.8" />
          <DimH x1={90} x2={146} y={214} label="4.5 depth" />
          <text x="118" y="248" textAnchor="middle" fontSize="11" fill="currentColor">
            wall 0.7 · partial cup
          </text>
          <text x="118" y="268" textAnchor="middle" fontSize="11" fill="currentColor">
            estimated, not factory
          </text>
        </svg>
        <figcaption>Side · estimated</figcaption>
      </figure>
    </div>
  );
}
