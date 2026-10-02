import { Link } from "@tanstack/react-router";
import { printedObjects } from "@/lib/printed-objects";
import { jewelleryPieces } from "@/lib/jewellery-pieces";
export function CollectionNav({ active }: { active: "jewellery" | "objects" }) {
  return (
    <nav className="collection-nav" aria-label="Design collections">
      <Link to="/jewellery" aria-current={active === "jewellery" ? "page" : undefined}>
        Jewellery <span>{String(jewelleryPieces.length + 1).padStart(2, "0")}</span>
      </Link>
      <Link to="/objects" aria-current={active === "objects" ? "page" : undefined}>
        Printed objects <span>{String(printedObjects.length).padStart(2, "0")}</span>
      </Link>
    </nav>
  );
}
export function ObjectsPreview() {
  return (
    <section className="collection-sibling" aria-labelledby="other-objects-title">
      <div>
        <p className="collection-kicker">Beyond jewellery</p>
        <h2 id="other-objects-title">Printed objects</h2>
        <p>Trophies, medals and sculptural forms.</p>
        <Link className="collection-link" to="/objects">
          Browse the {printedObjects.length} objects <span aria-hidden="true">↗︎</span>
        </Link>
      </div>
      <Link
        className="collection-sibling-images"
        to="/objects"
        aria-label="Explore the printed objects collection"
      >
        {printedObjects.slice(0, 3).map((object) => (
          <img
            key={object.slug}
            src={object.card}
            alt={object.title}
            loading="lazy"
            width={800}
            height={800}
          />
        ))}
      </Link>
    </section>
  );
}
