import { Link } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { filters, projects, type FilterId, type Project } from "@/data/projects";

const featured = [
  {
    id: "sound",
    kicker: "Featured / Sound in context",
    image: "/portfolio/speaker-wide.webp",
    alt: "Orange speaker on a wooden surface in warm afternoon light",
  },
  {
    id: "black",
    kicker: "Featured / Industrial form",
    image: "/portfolio/dev-tools-workshop.webp",
    alt: "PC enclosures arranged on a workshop bench for dev.tools",
  },
  {
    id: "gpu",
    kicker: "Featured / Engineered in light",
    image: "/portfolio/gpu-detail.webp",
    alt: "Graphics card fans and metallic surfaces in cool light",
  },
];

export function HomePage() {
  const [filter, setFilter] = useState<FilterId>("All");
  const [active, setActive] = useState<Project | null>(null);
  const [slide, setSlide] = useState(0);
  const [paused, setPaused] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);
  const openerRef = useRef<HTMLElement | null>(null);
  const touchRef = useRef<{ x: number; y: number } | null>(null);
  const suppressClick = useRef(false);

  const shown = projects.filter((p) => filter === "All" || p.category === filter);
  const counts = {
    All: projects.length,
    Product: projects.filter((p) => p.category === "Product").length,
    Beauty: projects.filter((p) => p.category === "Beauty").length,
    Motion: projects.filter((p) => p.category === "Motion").length,
  };

  function openProject(id: string, trigger?: HTMLElement | null) {
    const project = projects.find((item) => item.id === id);
    if (!project) return;
    if (trigger) openerRef.current = trigger;
    setActive(project);
  }

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (active && !dialog.open) dialog.showModal();
    if (active) dialog.scrollTop = 0;
    if (!active && dialog.open) dialog.close();
  }, [active]);

  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (paused || reduced || active) return;
    const timer = window.setTimeout(() => setSlide((n) => (n + 1) % featured.length), 6000);
    return () => window.clearTimeout(timer);
  }, [slide, paused, active]);

  useEffect(() => {
    document.body.classList.toggle("modal-open", Boolean(active));
    return () => document.body.classList.remove("modal-open");
  }, [active]);

  const next = active ? projects[(projects.indexOf(active) + 1) % projects.length] : null;

  return (
    <main className="home" id="content">
      <section className="intro">
        <p className="eyebrow">Adesina Adebola / Lagos</p>
        <h1>
          Objects.
          <br />
          <em>In a new light.</em>
        </h1>
        <div className="intro-bottom">
          <p>
            Product imagery, animation,
            <br />
            and jewellery developed through to a detailed 3D model.
          </p>
          <a className="text-link" href="#work">
            Explore selected work <span aria-hidden="true">↓</span>
          </a>
        </div>
        <span className="intro-number" aria-hidden="true">
          (01—{String(projects.length).padStart(2, "0")})
        </span>
      </section>

      <section
        className="featured-carousel"
        aria-label="Featured work"
        aria-roledescription="carousel"
      >
        <div
          className="featured-window"
          onTouchStart={(event) => {
            const t = event.changedTouches[0];
            touchRef.current = { x: t.clientX, y: t.clientY };
          }}
          onTouchEnd={(event) => {
            if (!touchRef.current) return;
            const t = event.changedTouches[0];
            const dx = t.clientX - touchRef.current.x;
            const dy = t.clientY - touchRef.current.y;
            touchRef.current = null;
            if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)) {
              suppressClick.current = true;
              setSlide((n) => (n + (dx < 0 ? 1 : -1) + featured.length) % featured.length);
              window.setTimeout(() => {
                suppressClick.current = false;
              }, 400);
            }
          }}
          onClickCapture={(event) => {
            if (!suppressClick.current) return;
            event.preventDefault();
            event.stopPropagation();
          }}
        >
          <div className="featured-track" style={{ transform: `translateX(-${slide * 100}%)` }}>
            {featured.map((item, index) => (
              <div
                className="featured-slide"
                key={item.id}
                role="group"
                aria-roledescription="slide"
                aria-label={`${index + 1} of ${featured.length}: ${item.kicker}`}
                aria-hidden={index !== slide}
                inert={index !== slide}
              >
                <button
                  className="hero-shot"
                  type="button"
                  aria-label={`Open ${item.kicker} case study`}
                  onClick={(event) => openProject(item.id, event.currentTarget)}
                >
                  <img
                    src={item.image}
                    alt={item.alt}
                    width={1920}
                    height={1080}
                    draggable={false}
                  />
                  <span className="hero-caption">
                    <span>{item.kicker}</span>
                    <span>View project ↗</span>
                  </span>
                </button>
              </div>
            ))}
          </div>
        </div>
        <div className="featured-controls">
          <button
            className="featured-pause"
            type="button"
            aria-label={paused ? "Play slideshow" : "Pause slideshow"}
            onClick={() => setPaused((value) => !value)}
          >
            {paused ? "Play" : "Pause"}
          </button>
          <div className="featured-dots" role="group" aria-label="Choose featured project">
            {featured.map((item, index) => (
              <button
                key={item.id}
                type="button"
                aria-label={`Show ${item.kicker}`}
                aria-pressed={index === slide}
                onClick={() => setSlide(index)}
              >
                <span />
              </button>
            ))}
          </div>
          <div className="featured-navigation">
            <span className="featured-count">
              0{slide + 1} / 0{featured.length}
            </span>
            <button
              className="featured-prev"
              type="button"
              aria-label="Previous featured project"
              onClick={() => setSlide((n) => (n - 1 + featured.length) % featured.length)}
            >
              ←
            </button>
            <button
              className="featured-next"
              type="button"
              aria-label="Next featured project"
              onClick={() => setSlide((n) => (n + 1) % featured.length)}
            >
              →
            </button>
          </div>
        </div>
      </section>

      <section className="work section" id="work">
        <div className="section-heading">
          <h2>
            Selected work<span> / {projects.length}</span>
          </h2>
          <p>Still images. Moving ideas.</p>
        </div>

        <div className="design-collections">
          <Link className="jewel-entry" to="/jewellery">
            <div className="jewel-entry-copy">
              <p className="eyebrow">Jewellery / 3D modelling</p>
              <h3>Jewellery Design</h3>
              <p>Form, detail and objects developed from concept to a detailed 3D model.</p>
              <p className="jewel-entry-meta">Jewellery · 3D modelling · Visualization · Prototyping</p>
              <span className="text-link">
                Enter <span aria-hidden="true">↗</span>
              </span>
            </div>
            <img
              src="/jewellery/amara-nest/02-three-quarter.png"
              alt="Amara Nest companion stud 3D design"
              width={1200}
              height={1500}
            />
          </Link>

          <Link className="jewel-entry object-entry" to="/objects">
            <div className="jewel-entry-copy">
              <p className="eyebrow">Objects / 3D printing</p>
              <h3>Printed Objects</h3>
              <p>Ten trophy and medal designs. Beauty renders, wireframes and original drawings.</p>
              <p className="jewel-entry-meta">Trophies · Medals · Model views</p>
              <span className="text-link">
                Explore the collection <span aria-hidden="true">↗</span>
              </span>
            </div>
            <div className="home-object-images">
              <img
                src="/objects/zenith-cup/card.webp"
                alt="The Zenith Cup beauty render"
                loading="lazy"
                width={800}
                height={800}
              />
              <img
                src="/objects/world/card.webp"
                alt="World award beauty render"
                loading="lazy"
                width={800}
                height={800}
              />
            </div>
          </Link>
        </div>

        <div className="filters" role="group" aria-label="Filter projects">
          {filters.map((item) => (
            <button
              key={item.id}
              type="button"
              className={filter === item.id ? "active" : undefined}
              aria-pressed={filter === item.id}
              onClick={() => setFilter(item.id)}
            >
              {item.label} <span>{counts[item.id]}</span>
            </button>
          ))}
        </div>
        <p className="sr-only" role="status">
          Showing {shown.length} {filter === "All" ? "" : `${filter.toLowerCase()} `}projects
        </p>
        <div className="grid">
          {shown.map((project) => (
            <button
              key={project.id}
              className="project"
              type="button"
              aria-label={`View ${project.title} case study`}
              onClick={(event) => openProject(project.id, event.currentTarget)}
            >
              <div
                className={
                  project.fit === "contain"
                    ? "project-image project-image-contain"
                    : "project-image"
                }
              >
                <img src={project.cover} alt="" width={1080} height={1080} />
                {project.video ? <span className="play-tag">Play film</span> : null}
              </div>
              <div className="project-info">
                <div>
                  <h3>{project.title}</h3>
                  <span className="category">{project.label}</span>
                </div>
                <span className="arrow" aria-hidden="true">
                  ↗
                </span>
              </div>
            </button>
          ))}
        </div>
      </section>

      <section className="about section" id="about">
        <p className="eyebrow">Behind the images</p>
        <div className="about-layout">
          <h2>
            A considered eye.
            <br />
            <em>A different dimension.</em>
          </h2>
          <div>
            <p className="about-copy">
              I’m Adesina Adebola, a 3D artist and designer based in Lagos. I make product visuals
              and develop objects — including jewellery — from a design language through to a detailed 3D model.
            </p>
            <p>
              The practice spans modeling, sculpting, animation, and post-production, from quiet
              product studies to more expressive imagery, alongside independent jewellery concepts
              and dimensioned 3D modelling studies.
            </p>
            <div className="cv">
              <h3>Experience & tools</h3>
              <dl>
                <div>
                  <dt>Experience</dt>
                  <dd>
                    Dead Game Entertainment
                    <br />
                    StrongFood — Strong Bar
                    <br />
                    Titan Air Mobility
                    <br />
                    dev.tools
                  </dd>
                </div>
                <div>
                  <dt>Tools</dt>
                  <dd>
                    Blender · DaVinci Resolve
                    <br />
                    Adobe Photoshop
                  </dd>
                </div>
                <div>
                  <dt>Practice</dt>
                  <dd>
                    Product visualization · Animation
                    <br />
                    Jewellery design · 3D modelling studies
                  </dd>
                </div>
              </dl>
              <a className="text-link" href="/portfolio/adesina-adebola-cv.pdf" download>
                Download CV <span aria-hidden="true">↓</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="contact" id="contact">
        <p className="eyebrow">Have a project in mind?</p>
        <h2>
          Your next product.
          <br />
          <em>A new perspective.</em>
        </h2>
        <div className="contact-bottom">
          <a className="email" href="mailto:deybor4l@gmail.com">
            deybor4l@gmail.com <span aria-hidden="true">↗</span>
          </a>
          <p>
            Lagos, Nigeria
            <br />
            Visualization, animation, object design
          </p>
        </div>
      </section>

      <dialog
        id="case-study"
        ref={dialogRef}
        aria-labelledby="case-title"
        onClose={() => {
          dialogRef.current?.querySelectorAll("video").forEach((video) => video.pause());
          setActive(null);
          openerRef.current?.focus();
        }}
        onClick={(event) => {
          const dialog = dialogRef.current;
          if (!dialog || event.target !== dialog) return;
          const rect = dialog.getBoundingClientRect();
          const { clientX: x, clientY: y } = event;
          if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) dialog.close();
        }}
      >
        <div className="dialog-bar">
          <span>Deybor 3D / Project notes</span>
          <button className="close" type="button" onClick={() => dialogRef.current?.close()}>
            Close ×
          </button>
        </div>
        {active ? (
          <article>
            <div className="case-head">
              <p className="eyebrow">{active.label}</p>
              <h2 id="case-title">{active.title}</h2>
              <p>{active.intro}</p>
            </div>
            {active.video ? (
              <figure className="case-media">
                <video
                  controls
                  playsInline
                  preload="metadata"
                  poster={active.cover}
                  aria-label={`${active.title} film`}
                >
                  <source src={active.video} type="video/mp4" />
                </video>
                <figcaption>Play the film. Sound controls are in the player.</figcaption>
              </figure>
            ) : null}
            {active.images.map(([src, caption]) => (
              <figure className="case-media" key={src}>
                <img src={src} alt={caption} />
                <figcaption>{caption}</figcaption>
              </figure>
            ))}
            <div className="case-details">
              <div>
                <h3>Visual approach</h3>
                <p>{active.focus}</p>
              </div>
              <div>
                <h3>Details & craft</h3>
                <p>{active.details}</p>
              </div>
            </div>
            <div className="case-footer">
              <a
                className="text-link"
                href={`mailto:deybor4l@gmail.com?subject=${encodeURIComponent(`Project enquiry — ${active.title}`)}`}
              >
                Discuss a similar project ↗
              </a>
              {next ? (
                <button className="case-next" type="button" onClick={() => openProject(next.id)}>
                  Next: {next.title} →
                </button>
              ) : null}
            </div>
          </article>
        ) : null}
      </dialog>
    </main>
  );
}
