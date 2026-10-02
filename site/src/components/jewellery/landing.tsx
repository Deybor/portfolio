import { Link } from "@tanstack/react-router";
import { CollectionNav, ObjectsPreview } from "@/components/portfolio-collection";
import { DeckProgress, Reveal } from "@/components/jewellery/stage";
import { JewelleryShowcase } from "@/components/jewellery/showcase";
import { JewelleryPieces } from "@/components/jewellery/pieces";

export function JewelleryLanding() {
  return (
    <main className="collection collection-jewellery" id="content">
      <DeckProgress />
      <div className="collection-wrap">
        <header className="collection-intro">
          <div>
            <p className="collection-kicker">Adesina Adebola / Jewellery · 3D modelling · Visualization</p>
            <h1>Jewellery Design</h1>
          </div>
          <p>
            I explore how a piece looks, how it belongs
            <br className="desktop-break" /> and how it can be made.
          </p>
        </header>
        <JewelleryShowcase />
        <CollectionNav active="jewellery" />
        <JewelleryPieces />
        <Reveal className="amara-invitation" id="amara-study">
          <div className="invitation-copy">
            <p className="collection-kicker">An independent exploration / ÌTURA</p>
            <h2>
              Amara’s
              <br />
              <em>companion</em>
            </h2>
            <p>A companion for an existing necklace.</p>
            <Link className="collection-link" to="/jewellery/amara">
              Open study <span aria-hidden="true">↗︎</span>
            </Link>
          </div>
          <Link
            className="invitation-image"
            to="/jewellery/amara"
            aria-label="Open Amara’s companion study"
          >
            <img
              src="/jewellery/refs/amara-1599.jpg"
              alt="The original ÌTURA Amara heart necklace worn on the neck"
              loading="lazy"
              width={1200}
              height={1200}
            />
            <span>The Amara necklace / ÌTURA</span>
          </Link>
        </Reveal>
        <ObjectsPreview />
      </div>
    </main>
  );
}
