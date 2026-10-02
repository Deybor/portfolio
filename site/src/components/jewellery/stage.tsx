import { useEffect, useRef, useState, type ReactNode } from "react";

export function useActiveChapter(ids: string[]) {
  const [active, setActive] = useState(ids[0] ?? "");
  const key = ids.join("|");

  useEffect(() => {
    const list = key.split("|").filter(Boolean);
    const nodes = list
      .map((id) => document.getElementById(id))
      .filter((node): node is HTMLElement => Boolean(node));
    if (!nodes.length) return;

    const seen = new Map<string, number>();
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          seen.set(entry.target.id, entry.isIntersecting ? entry.intersectionRatio : 0);
        }
        const next = [...seen.entries()].sort((a, b) => b[1] - a[1])[0];
        if (next && next[1] > 0) setActive(next[0]);
      },
      { rootMargin: "-40% 0px -45% 0px", threshold: [0, 0.25, 0.6] },
    );

    nodes.forEach((node) => observer.observe(node));
    return () => observer.disconnect();
  }, [key]);

  return active;
}

export function ChapterRail({
  items,
  active,
}: {
  items: { id: string; label: string }[];
  active: string;
}) {
  return (
    <nav className="chapter-rail" aria-label="Chapters">
      {items.map((item, index) => (
        <a
          key={item.id}
          href={`#${item.id}`}
          aria-current={active === item.id ? "true" : undefined}
          aria-label={`${String(index + 1).padStart(2, "0")} ${item.label}`}
        >
          <span />
        </a>
      ))}
    </nav>
  );
}

export function DeckProgress() {
  useEffect(() => {
    const id = window.location.hash.replace("#", "");
    if (!id) return;
    const node = document.getElementById(id);
    if (!node) return;
    requestAnimationFrame(() => node.scrollIntoView({ block: "start" }));
  }, []);

  return <div className="deck-progress" aria-hidden="true" />;
}

function useEntrance(threshold: number) {
  const ref = useRef<HTMLElement>(null);
  const [on, setOn] = useState(false);
  const [ready, setReady] = useState(false);
  const completed = useRef(false);

  useEffect(() => {
    const node = ref.current;
    if (!node || !window.IntersectionObserver) return;
    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    let observer: IntersectionObserver | undefined;
    const reveal = () => {
      completed.current = true;
      setOn(true);
      observer?.disconnect();
    };
    const update = () => {
      if (preference.matches) {
        setReady(false);
        reveal();
        return;
      }
      if (completed.current) return;
      setReady(true);
      observer = new IntersectionObserver(
        ([entry]) => {
          if (entry?.isIntersecting) reveal();
        },
        { threshold, rootMargin: "0px 0px -5% 0px" },
      );
      observer.observe(node);
    };
    update();
    preference.addEventListener("change", update);
    return () => {
      observer?.disconnect();
      preference.removeEventListener("change", update);
    };
  }, [threshold]);

  return { ref, on, ready };
}

export function MotionArticle({
  className = "",
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  const { ref, on, ready } = useEntrance(0.08);
  return (
    <article
      ref={ref}
      className={`amara-motion-item${ready ? " motion-ready" : ""}${on ? " is-in" : ""} ${className}`}
    >
      {children}
    </article>
  );
}

export function Reveal({
  id,
  labelledBy,
  threshold = 0.2,
  className = "",
  children,
}: {
  id?: string;
  labelledBy?: string;
  threshold?: number;
  className?: string;
  children: ReactNode;
}) {
  const { ref, on, ready } = useEntrance(threshold);

  return (
    <section
      id={id}
      aria-labelledby={labelledBy}
      ref={ref}
      className={`reveal${ready ? " motion-ready" : ""}${on ? " is-in" : ""} ${className}`.trim()}
    >
      {children}
    </section>
  );
}
