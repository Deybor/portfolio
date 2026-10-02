import { useEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Pause, Play } from "lucide-react";

const slides = [
  {
    title: "Amara Nest, as a pair",
    kind: "My design / beauty render",
    image: "/jewellery/amara-nest/beauty/03.webp",
    alt: "My Amara Nest heart studs rendered as a pair on a mirrored surface",
    backdrop: false,
    placeholder: false,
  },
  {
    title: "Confluence",
    kind: "My design / Blender render",
    image: "/jewellery/confluence/render-01-environment.webp",
    alt: "My Confluence three-stone ring with sweeping gold shoulders",
    backdrop: true,
    placeholder: false,
  },
  {
    title: "Iced-out ring",
    kind: "My design / Blender render",
    image: "/jewellery/iced-out-ring/render-01-gallery.webp",
    alt: "My iced-out ring with rows of stones around a gold band",
    backdrop: true,
    placeholder: false,
  },
  {
    title: "Heartline",
    kind: "My design / Blender render",
    image: "/jewellery/heartline-pendant/render-01-studio.webp",
    alt: "My Heartline open-heart pendant in a studio render",
    backdrop: true,
    placeholder: false,
  },
  {
    title: "Ribbon Leaf",
    kind: "My design / Blender render",
    image: "/jewellery/ribbon-leaf/render-01-studio.webp",
    alt: "My Ribbon Leaf drop earrings with stone clusters and open ribbon-shaped leaves",
    backdrop: true,
    placeholder: false,
  },
];

export function JewelleryShowcase() {
  const [slide, setSlide] = useState(0);
  const [paused, setPaused] = useState(false);
  const [hovered, setHovered] = useState(false);
  const [reduced, setReduced] = useState(true);
  const [visible, setVisible] = useState(false);
  const [documentHidden, setDocumentHidden] = useState(false);
  const root = useRef<HTMLElement>(null);
  const touch = useRef<{ x: number; y: number } | null>(null);
  const playing = !paused && !hovered && !reduced && visible && !documentHidden;

  useEffect(() => {
    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    const updateMotion = () => setReduced(preference.matches);
    const updateVisibility = () => setDocumentHidden(document.hidden);
    updateMotion();
    updateVisibility();
    preference.addEventListener("change", updateMotion);
    document.addEventListener("visibilitychange", updateVisibility);
    const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting), {
      threshold: 0.25,
    });
    if (root.current) observer.observe(root.current);
    return () => {
      observer.disconnect();
      preference.removeEventListener("change", updateMotion);
      document.removeEventListener("visibilitychange", updateVisibility);
    };
  }, []);

  useEffect(() => {
    if (!playing) return;
    const timer = window.setTimeout(
      () => setSlide((current) => (current + 1) % slides.length),
      3500,
    );
    return () => window.clearTimeout(timer);
  }, [playing, slide]);

  function select(index: number) {
    setPaused(true);
    setSlide((index + slides.length) % slides.length);
  }

  return (
    <section
      ref={root}
      className="jewellery-showcase"
      aria-label="Jewellery showcase"
      aria-roledescription="carousel"
      onMouseEnter={() => {
        if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) setHovered(true);
      }}
      onMouseLeave={() => setHovered(false)}
      onFocusCapture={(event) => {
        if (!(event.target as HTMLElement).closest("[data-playback]")) setPaused(true);
      }}
      onKeyDown={(event) => {
        if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
          event.preventDefault();
          select(slide + (event.key === "ArrowRight" ? 1 : -1));
        }
      }}
    >
      <div
        className="showcase-stage"
        onTouchStart={(event) => {
          const point = event.touches[0];
          touch.current = { x: point.clientX, y: point.clientY };
        }}
        onTouchEnd={(event) => {
          const start = touch.current;
          touch.current = null;
          if (!start) return;
          const point = event.changedTouches[0];
          const dx = point.clientX - start.x;
          if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(point.clientY - start.y))
            select(slide + (dx < 0 ? 1 : -1));
        }}
      >
        {slides.map((item, index) => (
          <div
            key={item.image}
            className={`showcase-slide${item.backdrop ? " showcase-slide-with-backdrop" : ""}${slide === index ? " is-active" : ""}`}
            role="group"
            aria-roledescription="slide"
            aria-label={`${index + 1} of ${slides.length}: ${item.title}`}
            aria-hidden={slide !== index}
          >
            {item.backdrop && (
              <img
                className="showcase-backdrop"
                src={item.image}
                alt=""
                aria-hidden="true"
                draggable={false}
              />
            )}
            <img
              className="showcase-image"
              src={item.image}
              alt={item.alt}
              width={1672}
              height={941}
              fetchPriority={index === 0 ? "high" : "auto"}
            />
          </div>
        ))}
        {slides[slide].placeholder && (
          <p className="showcase-placeholder">AI concept placeholder</p>
        )}
      </div>
      <div className="showcase-caption">
        <div key={slides[slide].image} className="showcase-copy" aria-live={paused ? "polite" : "off"} aria-atomic="true">
          <p className="collection-kicker">{slides[slide].kind}</p>
          <h2>{slides[slide].title}</h2>
        </div>
        <div className="showcase-controls">
          <button
            type="button"
            aria-label="Previous showcase image"
            onClick={() => select(slide - 1)}
          >
            <ArrowLeft size={18} />
          </button>
          <span className="showcase-count" aria-hidden="true">
            0{slide + 1} / 0{slides.length}
          </span>
          <button type="button" aria-label="Next showcase image" onClick={() => select(slide + 1)}>
            <ArrowRight size={18} />
          </button>
          {!reduced && (
            <button
              type="button"
              data-playback
              aria-label={paused ? "Play jewellery slideshow" : "Pause jewellery slideshow"}
              onClick={() => setPaused((current) => !current)}
            >
              {paused ? <Play size={16} /> : <Pause size={16} />}
            </button>
          )}
        </div>
      </div>
    </section>
  );
}
