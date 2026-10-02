import { Fragment, useEffect, useRef } from "react";
import groups from "@/data/amara-spec.json";

export function SpecificationTable() {
  const viewportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const viewport = viewportRef.current;
    if (!viewport || !window.IntersectionObserver) return;

    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (preference.matches) return;

    const rows = Array.from(viewport.querySelectorAll<HTMLElement>(".amara-spec-data-row"));
    const pendingRows = new Set<HTMLElement>();
    let frameObserver: IntersectionObserver;
    let valueObserver: IntersectionObserver;
    let enteredAt: number | null = null;
    let paintFrame = 0;
    let finished = false;

    const finish = () => {
      finished = true;
      cancelAnimationFrame(paintFrame);
      frameObserver?.disconnect();
      valueObserver?.disconnect();
      viewport.classList.remove("is-motion-ready");
      viewport.classList.add("has-entered");
      rows.forEach((row) => row.classList.add("is-value-visible"));
      pendingRows.clear();
    };

    const revealPendingRows = () => {
      if (enteredAt === null || finished) return;
      const lead = Math.max(0, 240 - (performance.now() - enteredAt));
      Array.from(pendingRows)
        .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top)
        .forEach((row, index) => {
          row.style.setProperty("--spec-value-delay", `${lead + Math.min(index, 5) * 65}ms`);
          row.classList.add("is-value-visible");
          valueObserver.unobserve(row);
        });
      pendingRows.clear();
    };

    frameObserver = new IntersectionObserver(
      (entries) => {
        if (enteredAt !== null || !entries.some((entry) => entry.isIntersecting) || finished)
          return;
        cancelAnimationFrame(paintFrame);
        paintFrame = requestAnimationFrame(() => {
          enteredAt = performance.now();
          viewport.classList.add("has-entered");
          frameObserver.disconnect();
          revealPendingRows();
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.01 },
    );

    valueObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) pendingRows.add(entry.target as HTMLElement);
        });
        revealPendingRows();
      },
      { rootMargin: "0px 0px 32px 0px", threshold: 0.1 },
    );

    const onPreferenceChange = () => {
      if (preference.matches) finish();
    };

    viewport.classList.add("is-motion-ready");
    frameObserver.observe(viewport);
    rows.forEach((row) => valueObserver.observe(row));
    preference.addEventListener("change", onPreferenceChange);

    return () => {
      cancelAnimationFrame(paintFrame);
      frameObserver.disconnect();
      valueObserver.disconnect();
      preference.removeEventListener("change", onPreferenceChange);
      viewport.classList.remove("is-motion-ready", "has-entered");
      rows.forEach((row) => {
        row.classList.remove("is-value-visible");
        row.style.removeProperty("--spec-value-delay");
      });
    };
  }, []);

  return (
    <div className="amara-spec-motion" ref={viewportRef}>
      <div className="amara-spec-table-frame">
        <table className="amara-spec-table">
          <caption>Amara Nest · specification</caption>
          <tbody>
            {groups.map((group) => (
              <Fragment key={group.heading}>
                <tr className="amara-spec-group">
                  <th colSpan={2}>{group.heading}</th>
                </tr>
                {group.rows.map(([name, value]) => (
                  <tr className="amara-spec-data-row" key={name}>
                    <th scope="row">{name}</th>
                    <td>
                      <span className="amara-spec-value">{value}</span>
                    </td>
                  </tr>
                ))}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
