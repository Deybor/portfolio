import { useState, type KeyboardEvent } from "react";
import { Link } from "@tanstack/react-router";
import { jewelleryPieces, type JewelleryPiece, type JewelleryView } from "@/lib/jewellery-pieces";

const labels: Record<JewelleryView["kind"], string> = {
  renders: "Renders",
  cad: "Model views",
  wireframe: "Wireframe",
  dimensions: "Dimensions",
  sketches: "Sketches",
};
const order = ["renders", "cad", "wireframe", "dimensions", "sketches"] as const;

export function JewelleryPiecePage({ piece }: { piece: JewelleryPiece }) {
  const [kind, setKind] = useState<JewelleryView["kind"]>("renders");
  const [index, setIndex] = useState(0);
  const kinds = order.filter((value) => piece.views.some((item) => item.kind === value));
  const views = piece.views.filter((item) => item.kind === kind);
  const view = views[index] ?? views[0];
  const previewGallery = JSON.stringify(views.map((item) => ({ href: item.full, title: `${piece.title} / ${item.label}` })));
  const next = jewelleryPieces[jewelleryPieces.findIndex((item) => item.slug === piece.slug) + 1];
  function select(value: JewelleryView["kind"]) {
    setKind(value);
    setIndex(0);
  }
  function handleTabKey(event: KeyboardEvent<HTMLButtonElement>) {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const nextKind =
      event.key === "Home"
        ? kinds[0]
        : event.key === "End"
          ? kinds[kinds.length - 1]
          : kinds[
              (kinds.indexOf(kind) + (event.key === "ArrowLeft" ? -1 : 1) + kinds.length) %
                kinds.length
            ];
    select(nextKind);
    event.currentTarget.parentElement
      ?.querySelector<HTMLButtonElement>(`#piece-${nextKind}-tab`)
      ?.focus();
  }
  return (
    <main className="collection jewellery-piece-page" id="content">
      <div className="collection-wrap">
        <nav className="object-project-nav" aria-label="Jewellery collection">
          <Link className="collection-link" to="/jewellery" hash="jewellery-pieces">
            ← All jewellery
          </Link>
          {next ? (
            <Link className="collection-link" to="/jewellery/$slug" params={{ slug: next.slug }}>
              Next: {next.title} →
            </Link>
          ) : (
            <Link className="collection-link" to="/jewellery/amara">
              Next: Amara’s companion →
            </Link>
          )}
        </nav>
        <header className="object-project-heading">
          <p className="collection-kicker">My jewellery / {piece.category}</p>
          <h1>{piece.title}</h1>
          <p>{piece.description}</p>
        </header>
        <div className="object-project-layout jewellery-piece-layout">
          <section className="object-viewer" aria-label={`${piece.title} image viewer`}>
            <div className="object-view-tabs" role="tablist" aria-label="Design stage">
              {kinds.map((value) => (
                <button
                  key={value}
                  type="button"
                  role="tab"
                  id={`piece-${value}-tab`}
                  aria-selected={kind === value}
                  aria-controls="piece-view-panel"
                  tabIndex={kind === value ? 0 : -1}
                  onClick={() => select(value)}
                  onKeyDown={handleTabKey}
                >
                  {labels[value]}
                  <span>{piece.views.filter((item) => item.kind === value).length}</span>
                </button>
              ))}
            </div>
            <div id="piece-view-panel" role="tabpanel" aria-labelledby={`piece-${kind}-tab`}>
              {kind === "dimensions" && piece.specification && (
                <p className="collection-kicker jewellery-specification-title">
                  Technical specification / {views.length} sheets
                </p>
              )}
              <figure className="object-main-view">
                <a
                  href={view.full}
                  data-preview-gallery={previewGallery}
                  aria-haspopup="dialog"
                  aria-label={`Open ${piece.title} ${view.label} full size`}
                >
                  <img
                    className={
                      kind === "dimensions" || kind === "sketches"
                        ? "jewellery-drawing-view"
                        : undefined
                    }
                    key={view.image}
                    src={view.image}
                    alt={`${piece.title} / ${view.label}`}
                    width={view.width}
                    height={view.height}
                    fetchPriority="high"
                  />
                </a>
                <figcaption>
                  <span>
                    {view.label} / {String(index + 1).padStart(2, "0")}
                  </span>
                  <a href={view.full} data-preview-gallery={previewGallery} aria-haspopup="dialog">
                    View full size ⤢
                  </a>
                </figcaption>
              </figure>
              {views.length > 1 && (
                <div
                  className="object-thumbnails"
                  role="group"
                  aria-label={`${labels[kind]} views`}
                >
                  {views.map((item, n) => (
                    <button
                      key={item.image}
                      type="button"
                      aria-label={`Show ${item.label}`}
                      aria-pressed={index === n}
                      onClick={() => setIndex(n)}
                    >
                      <img src={item.image} alt="" width={120} height={120} loading="lazy" />
                      <span>{String(n + 1).padStart(2, "0")}</span>
                    </button>
                  ))}
                </div>
              )}
              {kind === "dimensions" && (
                <div className="jewellery-piece-downloads">
                  {piece.specification && (
                    <a className="collection-link" href={piece.specification}>
                      View full specification <span aria-hidden="true">↗︎</span>
                    </a>
                  )}
                  {piece.downloads.map((item) => (
                    <div key={item.href}>
                      <p className="collection-kicker">{item.label}</p>
                      <a className="collection-link" href={item.href} download>
                        Download <span aria-hidden="true">↓</span>
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
          <aside
            className="object-specification jewellery-piece-about"
            aria-labelledby="piece-about-title"
          >
            <p className="collection-kicker">The idea</p>
            <h2 id="piece-about-title">About the piece</h2>
            <p>{piece.story}</p>
            <p className="jewellery-piece-note">{piece.note}</p>
          </aside>
        </div>
        <div className="collection-end">
          <Link className="collection-link" to="/jewellery" hash="jewellery-pieces">
            ← Back to jewellery
          </Link>
          <Link className="collection-link" to="/jewellery/amara">
            Explore Amara’s companion ↗︎
          </Link>
        </div>
      </div>
    </main>
  );
}
