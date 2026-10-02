import { Link, useElementScrollRestoration } from "@tanstack/react-router";
import { useEffect } from "react";
import { AmaraStory, AmaraBeautyGallery } from "@/components/jewellery/amara-story";
import { useActiveChapter, Reveal } from "@/components/jewellery/stage";
import { SpecificationTable } from "@/components/jewellery/specification-table";
import { ModelComparison } from "@/components/jewellery/model-comparison";
import { AmaraScrollProgress } from "@/components/jewellery/amara-scroll-progress";

const asset = "/jewellery/amara-nest/";
const spec = `${asset}specification.html`;

export function AmaraPage() {
  const hasSavedScroll = Boolean(
    useElementScrollRestoration({
      getElement: () => (typeof window === "undefined" ? undefined : window),
    }),
  );
  useEffect(() => {
    // The scroll scene takes its measured height after hydration. Resolve an initial
    // chapter link after that layout settles, including links to the model/spec sheet.
    if (hasSavedScroll || !window.location.hash) return;
    const initialHash = window.location.hash;
    let frame = 0;
    let cancelled = false;
    const settle = (remaining: number) => {
      frame = requestAnimationFrame(() => {
        if (cancelled || window.location.hash !== initialHash) return;
        if (remaining > 0) return settle(remaining - 1);
        const target = document.getElementById(window.location.hash.slice(1));
        target?.scrollIntoView({ block: "start", behavior: "instant" });
      });
    };
    settle(2);
    return () => {
      cancelled = true;
      cancelAnimationFrame(frame);
    };
  }, [hasSavedScroll]);

  const active = useActiveChapter([
    "overview",
    "directions",
    "selected",
    "inspect",
    "specification",
    "rendered",
  ]);

  return (
    <main className="amara-case" id="content">
      <nav className="amara-local-nav" aria-label="On this page">
        <span className="amara-local-title">Amara Nest</span>
        <div className="amara-local-links">
          <a href="#overview" aria-current={active === "overview" ? "location" : undefined}>
            The question
          </a>
          <a
            href="#directions"
            aria-current={["directions", "selected"].includes(active) ? "location" : undefined}
          >
            The decisions
          </a>
          <a href="#inspect" aria-current={active === "inspect" ? "location" : undefined}>
            Model
          </a>
          <a
            href="#specification"
            aria-current={["specification", "rendered"].includes(active) ? "location" : undefined}
          >
            Spec sheet
          </a>
        </div>
        <AmaraScrollProgress />
      </nav>

      <AmaraStory />

      <Reveal className="amara-inspect" id="inspect" labelledBy="inspect-title" threshold={0.06}>
        <div className="amara-container">
          <div className="amara-section-heading amara-section-heading-light">
            <p className="amara-kicker">03 / The model</p>
            <h2 id="inspect-title">Building the stud</h2>
            <p>
              I modelled the shell, seat and prongs in Blender. Here’s the same view with the
              materials and mesh.
            </p>
          </div>
          <ModelComparison />
        </div>
      </Reveal>

      <Reveal className="amara-spec" id="specification" labelledBy="spec-title" threshold={0.02}>
        <div className="amara-container">
          <div className="amara-section-heading amara-section-heading-dark">
            <p className="amara-kicker">04 / Specification</p>
            <h2 id="spec-title">The spec sheet</h2>
            <p>The model at a glance, with dimensions, materials and estimated weight.</p>
          </div>
          <div className="amara-spec-sheet-layout">
            <figure className="amara-spec-model">
              <img
                src={`${asset}model49/model-overview.svg`}
                alt="Amara Nest front and side sketches with overall width, height and depth dimensions, plus an isometric view"
                loading="lazy"
                width={1000}
                height={1400}
              />
              <figcaption>Model sketches</figcaption>
              <a
                className="amara-action amara-action-dark"
                href={spec}
                target="_blank"
                rel="noopener noreferrer"
              >
                Open the full spec sheet
              </a>
            </figure>
            <SpecificationTable />
          </div>
          <p className="amara-spec-note">
            Model dimensions before finishing. Proposed metal and finish. Estimated weight excludes
            backs; the unit cost is a planning target. Sample approval pending.
          </p>
        </div>
      </Reveal>

      <AmaraBeautyGallery />

      <nav className="amara-end-nav amara-container" aria-label="Continue browsing">
        <Link to="/jewellery">Jewellery overview</Link>
        <Link to="/jewellery/workbench">More drawings and making</Link>
      </nav>
    </main>
  );
}
