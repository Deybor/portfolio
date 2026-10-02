import { useState, type KeyboardEvent } from "react";
import { Link } from "@tanstack/react-router";
import { printedObjects, type PrintedObject } from "@/lib/printed-objects";

export function ObjectProject({ project }: { project: PrintedObject }) {
  return <ObjectStudy key={project.slug} project={project} />;
}

const viewLabels: Record<string, string> = {
  final: "Renders", clay: "Clay", wireframe: "Wireframe", references: "References", dimensions: "Dimensions",
};
const captions: Record<string, string> = {
  final: "Beauty render", clay: "Clay study", wireframe: "Model wireframe", references: "Original design drawing", dimensions: "Dimensioned model drawing",
};

function ObjectStudy({ project }: { project: PrintedObject }) {
  const [kind, setKind] = useState("final");
  const [index, setIndex] = useState(0);
  const hasWireframes = project.views.some((view) => view.kind === "wireframe");
  const kinds = ["final", "clay", "wireframe", "dimensions", "references"].filter((value) => project.views.some((view) => view.kind === value));
  const views = project.views.filter((view) => view.kind === kind);
  const view = views[index] ?? views[0];
  const previewGallery = JSON.stringify(views.map((item) => ({ href: item.full, title: `${project.title} / ${item.label ?? captions[kind]} / ${item.index}` })));
  const projectIndex = printedObjects.findIndex((item) => item.slug === project.slug);
  const next = printedObjects[(projectIndex + 1) % printedObjects.length];
  function selectKind(value: string) {
    setKind(value);
    setIndex(0);
  }
  function handleTabKey(event: KeyboardEvent<HTMLButtonElement>) {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const value =
      event.key === "Home"
        ? "final"
        : event.key === "End"
          ? kinds[kinds.length - 1]
          : kinds[(kinds.indexOf(kind) + (event.key === "ArrowLeft" ? -1 : 1) + kinds.length) % kinds.length];
    selectKind(value);
    event.currentTarget.parentElement?.querySelector<HTMLButtonElement>(`#${value}-tab`)?.focus();
  }
  return (
    <main className="collection object-project" id="content">
      <div className="collection-wrap">
        <nav className="object-project-nav" aria-label="Object collection">
          <Link className="collection-link" to="/objects">
            ← All printed objects
          </Link>
          <Link className="collection-link" to="/objects/$slug" params={{ slug: next.slug }}>
            Next: {next.title} <span aria-hidden="true">→</span>
          </Link>
        </nav>
        <header className="object-project-heading">
          <p className="collection-kicker">
            {String(projectIndex + 1).padStart(2, "0")} /{" "}
            {project.slug === "medal" ? "Medal" : "Award design"}
          </p>
          <h1>{project.title}</h1>
          <p>
            3D model · {project.views.filter((item) => item.kind === "final").length} render{" "}
            {project.views.filter((item) => item.kind === "final").length === 1 ? "view" : "views"}
            {project.views.some((item) => item.kind === "clay") ? " · Clay + wireframe studies" : ""}
          </p>
        </header>
        <div className="object-project-layout">
          <section className="object-viewer" aria-label={`${project.title} image viewer`}>
            {hasWireframes ? (
              <div className="object-view-tabs" role="tablist" aria-label="Design stage">
                {kinds.map((value) => (
                  <button
                    key={value}
                    type="button"
                    role="tab"
                    id={`${value}-tab`}
                    aria-selected={kind === value}
                    aria-controls="object-view-panel"
                    tabIndex={kind === value ? 0 : -1}
                    onClick={() => selectKind(value)}
                    onKeyDown={handleTabKey}
                  >
                    {viewLabels[value]}
                    <span>{project.views.filter((item) => item.kind === value).length}</span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="object-view-label" id="final-views-heading">
                Final render views
              </p>
            )}
            <div
              id="object-view-panel"
              role={hasWireframes ? "tabpanel" : "region"}
              aria-labelledby={hasWireframes ? `${kind}-tab` : "final-views-heading"}
            >
              <figure className="object-main-view">
                <a
                  href={view.full}
                  data-preview-gallery={previewGallery}
                  aria-haspopup="dialog"
                  aria-label={`Open ${project.title} ${viewLabels[kind]} view ${view.index} full size`}
                >
                  <img
                    key={view.image}
                    src={view.image}
                    alt={`${project.title} ${view.label ?? captions[kind]}, view ${view.index}`}
                    width={view.width}
                    height={view.height}
                    fetchPriority="high"
                  />
                </a>
                <figcaption>
                  <span>
                    {view.label ?? captions[kind]} /{" "}
                    {String(view.index).padStart(2, "0")}
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
                  aria-label={`${viewLabels[kind]} views`}
                >
                  {views.map((item, n) => (
                    <button
                      key={item.image}
                      type="button"
                      aria-label={`Show ${item.label ?? viewLabels[kind]} view ${item.index}`}
                      aria-pressed={index === n}
                      onClick={() => setIndex(n)}
                    >
                      <img src={item.image} alt="" loading="lazy" width={120} height={120} />
                      <span>{String(item.index).padStart(2, "0")}{item.label === "Blender workspace" ? " · Blender" : ""}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </section>
          <aside className="object-specification" aria-labelledby="object-spec-title">
            <p className="collection-kicker">Object specification</p>
            <h2 id="object-spec-title">The essentials</h2>
            <dl>
              {project.dimensions && ["height", "width", "depth"].map((axis) => (
                <div key={axis}><dt>Overall {axis}</dt><dd>{project.dimensions![axis as keyof typeof project.dimensions].toFixed(1)} <span className="object-unit">mm</span></dd></div>
              ))}
              {[...(project.dimensions ? [] : ["Dimensions"]), "Materials", "Printing process", "Finish"].map((label) => (
                <div key={label}>
                  <dt>{label}</dt>
                  <dd>—</dd>
                </div>
              ))}
            </dl>
            {project.dimensions && <>
              <button className="collection-link object-drawing-link" onClick={() => { selectKind("dimensions"); document.getElementById("dimensions-tab")?.focus(); }}>View dimensioned drawing <span aria-hidden="true">↗︎</span></button>
              <a className="collection-link" href={`/objects/${project.slug}/dimensions.svg`} download>Download</a>
            </>}
            <div className="object-project-resources">
              <p className="collection-kicker">Explore the collection</p>
              <Link className="collection-link" to="/objects" hash="drawings">
                Original award design drawings <span aria-hidden="true">↗︎</span>
              </Link>
              <a
                className="collection-link"
                href="/objects/award-designs.pdf"
                target="_blank"
                rel="noopener noreferrer"
              >
                Open the design book <span aria-hidden="true">↗︎</span>
              </a>
            </div>
          </aside>
        </div>
        <div className="collection-end">
          <Link className="collection-link" to="/objects">
            ← Back to all objects
          </Link>
          <Link className="collection-link" to="/objects/$slug" params={{ slug: next.slug }}>
            Explore {next.title} <span aria-hidden="true">→</span>
          </Link>
        </div>
      </div>
    </main>
  );
}
