import { useEffect, useRef, useState } from "react";

const smoothPhase = (progress: number, start: number, end: number) => {
  const phase = Math.min(1, Math.max(0, (progress - start) / (end - start)));
  return phase * phase * (3 - 2 * phase);
};

const chromeBottom = () => {
  const header = document.querySelector<HTMLElement>(".site-header");
  const navigation = document.querySelector<HTMLElement>(".amara-local-nav");
  const position = navigation ? window.getComputedStyle(navigation).position : "";
  const navigationBottom =
    position === "sticky" || position === "fixed"
      ? (navigation?.getBoundingClientRect().bottom ?? 0)
      : 0;
  return Math.ceil(Math.max(0, header?.getBoundingClientRect().bottom ?? 0, navigationBottom));
};

export function SelectedReveal() {
  const root = useRef<HTMLElement>(null);
  const stage = useRef<HTMLDivElement>(null);
  const image = useRef<HTMLElement>(null);
  const revealed = useRef(false);
  const [motion, setMotion] = useState(false);
  const [sticky, setSticky] = useState(false);
  const [paused, setPaused] = useState(false);
  const animate = motion && !paused;

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: no-preference)");
    const update = () => {
      const top = chromeBottom();
      root.current?.style.setProperty("--nest-top", `${top}px`);
      const available = window.innerHeight - top;
      setMotion(media.matches);
      // Small viewports still get the entrance, without a constrained pinned stage.
      setSticky(window.innerWidth > 900 && available >= 480);
    };
    update();
    media.addEventListener("change", update);
    window.addEventListener("resize", update);
    return () => {
      media.removeEventListener("change", update);
      window.removeEventListener("resize", update);
    };
  }, []);

  useEffect(() => {
    const node = root.current;
    const stageNode = stage.current;
    const imageNode = image.current;
    if (!node || !stageNode || !imageNode || !animate) return;

    let frame = 0;
    const paint = () => {
      frame = 0;
      const top = chromeBottom();
      node.style.setProperty("--nest-top", `${top}px`);
      const copyNode = node.querySelector<HTMLElement>(".amara-chosen-copy");
      if (sticky) {
        const stageStyle = window.getComputedStyle(stageNode);
        const controls = node.querySelector<HTMLElement>(".amara-chosen-continuation");
        const contentSpace =
          stageNode.clientHeight -
          parseFloat(stageStyle.paddingTop) -
          parseFloat(stageStyle.paddingBottom) -
          parseFloat(stageStyle.rowGap) -
          (controls?.offsetHeight ?? 0);
        if (Math.max(imageNode.offsetHeight, copyNode?.offsetHeight ?? 0) > contentSpace + 4) {
          setSticky(false);
          return;
        }
      }
      const bounds = node.getBoundingClientRect();
      const entry = smoothPhase(
        (window.innerHeight - bounds.top) / Math.max(1, window.innerHeight - top),
        0.04,
        0.74,
      );
      const distance = Math.max(1, bounds.height - stageNode.offsetHeight);
      const progress = sticky ? Math.min(1, Math.max(0, (top - bounds.top) / distance)) : entry;
      const settled = sticky ? (revealed.current ? 1 : smoothPhase(progress, 0.02, 0.5)) : entry;
      const copyTop = stageNode.getBoundingClientRect().top + (copyNode?.offsetTop ?? 0);
      const copyEntry = sticky
        ? smoothPhase(progress, 0.46, 0.64)
        : smoothPhase((window.innerHeight - copyTop) / (window.innerHeight * 0.4), 0.05, 0.72);
      if (copyEntry >= 1) revealed.current = true;
      const copy = revealed.current ? 1 : copyEntry;
      // Repeat the object's movement on revisiting; keep its explanation readable.
      const centre = (stageNode.clientWidth - imageNode.offsetWidth) / 2 - imageNode.offsetLeft;

      node.style.setProperty("--nest-shift", `${sticky ? centre * (1 - settled) : 0}px`);
      node.style.setProperty("--nest-lift", `${(1 - entry) * 72}px`);
      node.style.setProperty(
        "--nest-scale",
        `${sticky ? 0.88 + entry * 0.36 - settled * 0.24 : 0.9 + entry * 0.1}`,
      );
      node.style.setProperty("--nest-image-opacity", `${entry}`);
      node.style.setProperty("--nest-warm", `${0.3 + entry * 0.7}`);
      node.style.setProperty("--nest-copy", `${copy}`);
      node.style.setProperty("--nest-copy-lift", `${(1 - copy) * 36}px`);
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(paint);
    };

    paint();
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
    };
  }, [animate, sticky]);

  return (
    <section
      ref={root}
      id="selected"
      aria-labelledby="selected-title"
      className={`amara-chosen${animate ? " has-motion" : ""}${animate && sticky ? " has-sticky-scene" : ""}`}
    >
      <div ref={stage} className="amara-chosen-stage amara-container">
        <figure ref={image} className="amara-chosen-image">
          <img
            src="/jewellery/amara-nest/beauty/06.webp"
            width={1920}
            height={1920}
            alt="My Amara Nest stud rendered in gold against an amber textured background"
            loading="lazy"
          />
          <figcaption>Amara Nest / Blender render</figcaption>
        </figure>
        <div className="amara-chosen-copy">
          <p className="amara-kicker">02 / The Nest stud</p>
          <h2 id="selected-title">The heart, held in a fold.</h2>
          <p>
            I kept Amara’s heart and wrapped one side in gold. The fold gives the stud a shape of
            its own, while leaving the stone open to the light.
          </p>
        </div>
        <div className="amara-chosen-continuation">
          <div className="amara-chosen-links">
            <a href="#inspect">View the model</a>
            {motion && (
              <button
                type="button"
                aria-pressed={paused}
                onClick={() => setPaused((value) => !value)}
              >
                {paused ? "Resume motion" : "Pause motion"}
              </button>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
