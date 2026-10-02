import { Link } from "@tanstack/react-router";
import { jewelleryPieces } from "@/lib/jewellery-pieces";
import { Reveal } from "@/components/jewellery/stage";

export function JewelleryPieces() {
  return (
    <section
      className="jewellery-pieces"
      id="jewellery-pieces"
      aria-labelledby="jewellery-pieces-title"
    >
      <div className="jewellery-pieces-heading">
        <p className="collection-kicker">My jewellery / Design studies</p>
        <h2 id="jewellery-pieces-title">Rings, earrings & a pendant</h2>
      </div>
      <div className="jewellery-piece-grid">
        {jewelleryPieces.map((piece) => (
          <Reveal key={piece.slug} className="jewellery-piece-card" threshold={0.08}>
            <Link
              to="/jewellery/$slug"
              params={{ slug: piece.slug }}
              aria-label={`Explore ${piece.title}`}
            >
              <div className="jewellery-piece-image">
                <img
                  src={piece.card}
                  alt={`${piece.title} / diagonal split of my beauty render and black wireframe on warm ivory`}
                  width={900}
                  height={900}
                  loading="lazy"
                />
                <div className="jewellery-piece-wireframe" aria-hidden="true">
                  <img
                    src={piece.cardWireframe}
                    alt=""
                    width={900}
                    height={900}
                    loading="lazy"
                  />
                </div>
                <span aria-hidden="true">↗︎</span>
              </div>
              <div className="jewellery-piece-copy">
                <p className="collection-kicker">{piece.category}</p>
                <h3>{piece.title}</h3>
                <p>{piece.description}</p>
                <span className="collection-link">
                  Explore piece <span aria-hidden="true">↗︎</span>
                </span>
              </div>
            </Link>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
