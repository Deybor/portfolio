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
            <p className="collection-kicker">
              Adesina Adebola / Jewellery design · CAD · Technical development
            </p>
            <h1>Jewellery Design</h1>
          </div>
          <p>
            I develop jewellery from collection fit
            <br className="desktop-break" /> to dimensioned CAD and technical specifications.
          </p>
        </header>
        <JewelleryShowcase />
        <div className="technical-entry-fabrication jewellery-fabrication">
          <p>
            Alongside jewellery, I design and physically 3D print trophies, medals and sculptural
            objects. Production is ongoing; the current gallery shows renders and model views.
          </p>
          <Link className="collection-link" to="/objects">
            Fabrication work <span aria-hidden="true">↗︎</span>
          </Link>
        </div>
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
