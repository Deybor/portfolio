import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { CollectionNav } from "@/components/portfolio-collection";
import { DeckProgress, Reveal } from "@/components/jewellery/stage";
import { awardSketches, printedObjects } from "@/lib/printed-objects";

export function ObjectsIndex() {
  const [filter, setFilter] = useState("all");
  const shown = printedObjects.filter(
    (object) =>
      filter === "all" || (filter === "medals" ? object.slug === "medal" : object.slug !== "medal"),
  );
  const filters = [
    { id: "all", label: "All objects", count: printedObjects.length },
    { id: "awards", label: "Awards", count: printedObjects.length - 1 },
    { id: "medals", label: "Medals", count: 1 },
  ];
  return (
    <main className="collection collection-objects" id="content">
      <DeckProgress />
      <div className="collection-wrap">
        <header className="collection-intro">
          <div>
            <p className="collection-kicker">Adesina Adebola / 3D design & printing</p>
            <h1>Printed Objects</h1>
          </div>
          <p>
            Trophies, medals and sculptural forms.
            <br className="desktop-break" /> Renders, clay studies, wireframes and original drawings.
          </p>
        </header>
        <CollectionNav active="objects" />
        <div className="object-index-tools">
          <div className="object-filters" role="group" aria-label="Filter printed objects">
            {filters.map((item) => (
              <button
                key={item.id}
                type="button"
                aria-pressed={filter === item.id}
                onClick={() => setFilter(item.id)}
              >
                {item.label} <span>{item.count}</span>
              </button>
            ))}
          </div>
          <a className="collection-link" href="#drawings">
            Original design drawings <span aria-hidden="true">↓</span>
          </a>
        </div>
        <p className="sr-only" role="status">
          Showing {shown.length} {filter === "all" ? "objects" : filter}
        </p>
        <section className="object-grid" aria-label="Printed object projects">
          {shown.map((object) => (
            <Reveal className="catalog-card" key={object.slug}>
              <Link className="object-card-link" to="/objects/$slug" params={{ slug: object.slug }}>
                <div className="object-card-image">
                  <img
                    className="shot"
                    src={object.card}
                    alt={`${object.title} beauty render`}
                    loading={object.slug === "zenith-cup" ? "eager" : "lazy"}
                    width={800}
                    height={800}
                  />
                  <span aria-hidden="true">↗</span>
                </div>
                <div className="object-card-copy">
                  <p className="collection-kicker">
                    {String(printedObjects.indexOf(object) + 1).padStart(2, "0")} /{" "}
                    {object.slug === "medal" ? "Medal" : "Award design"}
                  </p>
                  <h2>{object.title}</h2>
                  <p>
                    {object.views.some((view) => view.kind === "wireframe")
                      ? "Renders · Clay · Wireframe"
                      : `${object.views.length} render ${object.views.length === 1 ? "view" : "views"}`}
                  </p>
                </div>
              </Link>
            </Reveal>
          ))}
        </section>
        <section className="award-drawings" id="drawings" aria-labelledby="award-drawings-title">
          <div className="drawings-heading">
            <div>
              <p className="collection-kicker">From the original design book</p>
              <h2 id="award-drawings-title">Sketches & development</h2>
            </div>
            <a
              className="collection-link"
              href="/objects/award-designs.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              Open the design book <span aria-hidden="true">↗</span>
            </a>
          </div>
          <details className="sketch-disclosure">
            <summary>
              Explore the original sketches and annotated designs <span aria-hidden="true">+</span>
            </summary>
            <div className="award-sketch-grid">
              {awardSketches.map((sketch) => (
                <a
                  key={sketch.page}
                  href={`/objects/award-sketches-${sketch.page}.webp`}
                  aria-haspopup="dialog"
                >
                  <figure>
                    <img
                      src={`/objects/award-sketches-${sketch.page}.webp`}
                      alt={`${sketch.title}, original award design book page ${sketch.page}`}
                      loading="lazy"
                      width={1600}
                      height={900}
                    />
                    <figcaption>
                      {sketch.title}
                      <span>Page {sketch.page} ↗</span>
                    </figcaption>
                  </figure>
                </a>
              ))}
            </div>
          </details>
        </section>
        <div className="collection-end">
          <Link className="collection-link" to="/jewellery">
            Explore jewellery design <span aria-hidden="true">↗</span>
          </Link>
          <a className="collection-link" href="/#work">
            Back to the main portfolio <span aria-hidden="true">↗</span>
          </a>
        </div>
      </div>
    </main>
  );
}
