import { Reveal, MotionArticle } from "@/components/jewellery/stage";
import { SelectedReveal } from "@/components/jewellery/selected-reveal";
import type { ReactNode } from "react";
import { ArrowDown } from "lucide-react";

const directions = [
  {
    title: "Scaled miniature",
    image: "/jewellery/amara-nest/directions/scaled-miniature.webp",
    style: "is-miniature",
    label: "Concept illustration",
    alt: "Miniature Heart stud concept, shown as a pair and in a wearing illustration",
    copy: "I tried a smaller version of the necklace. It matched, but I wanted the stud to have a shape of its own.",
  },
  {
    title: "Nest",
    image: "/jewellery/amara-nest/directions/nest.webp",
    style: "is-nest",
    label: "Chosen direction / concept illustration",
    alt: "Nest stud concept, shown as a pair and in a wearing illustration",
    copy: "I kept the heart and wrapped one side in gold. A satin fold and polished edge were the finishes I had in mind.",
  },
  {
    title: "A drop",
    image: "/jewellery/amara-nest/directions/unfurl-drop.webp",
    style: "is-drop",
    label: "Concept illustration",
    alt: "Unfurl drop concept with a gold fold and heart stone, shown as a pair and in a wearing illustration",
    copy: "The drop was another option. I put it aside because I wanted a matching stud, and ÌTURA already has heart drops.",
  },
];

export function AmaraStory({ children }: { children?: ReactNode }) {
  return (
    <>
      <section
        className="amara-hero amara-container amara-question"
        id="overview"
        aria-labelledby="amara-title"
      >
        <div className="amara-hero-copy">
          <p className="amara-kicker">Independent companion design / ÌTURA</p>
          <h1 id="amara-title">
            What if Amara
            <br />
            <em>had a stud?</em>
          </h1>
          <p className="amara-hero-lede">
            I took the necklace’s heart and soft gold wrap, and explored them as a matching stud.
          </p>
          <p className="amara-hero-reason">
            A stud felt like a natural companion. I wanted a shape of its own, with room for another
            earring beside it.
          </p>
          <dl className="amara-hero-facts">
            <div>
              <dt>My work</dt>
              <dd>Design, technical drawings &amp; specifications</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>Independent digital study</dd>
            </div>
          </dl>
          <div className="amara-hero-actions">
            <a
              className="amara-action amara-action-primary"
              href="/jewellery/amara-nest/specification.html"
            >
              Inspect dimensions &amp; specification
            </a>
            <a className="amara-action amara-decision-cue" href="#directions">
              Design decisions
              <ArrowDown className="amara-decision-arrow" aria-hidden="true" />
            </a>
          </div>
          <details className="amara-research-detail amara-opening-research">
            <summary>What informed the idea</summary>
            <p>
              I started with Amara in ÌTURA’s bestseller edit. Studs with a clear focal stone and a
              fuller shape, and ways of stacking earrings, informed the direction.
            </p>
            <div className="amara-market-sources">
              <a
                href="https://iturajewelry.com/collections/bestsellers"
                target="_blank"
                rel="noopener noreferrer"
              >
                ÌTURA’s bestseller edit
              </a>
              <a
                href="https://mejuri.com/collections/best-selling-earrings"
                target="_blank"
                rel="noopener noreferrer"
              >
                Mejuri’s studs &amp; huggies
              </a>
              <a
                href="https://us.missoma.com/blogs/the-chain/how-to-stack-style-your-earrings"
                target="_blank"
                rel="noopener noreferrer"
              >
                Missoma’s stacking approach
              </a>
            </div>
          </details>
        </div>
        <div className="amara-opening-visual">
          <figure className="amara-hero-visual amara-result-visual">
            <img
              src="/jewellery/amara-nest/beauty/03.webp"
              alt="My Amara Nest companion studs, modelled and rendered as a pair on a mirrored surface"
              width={1920}
              height={1920}
              fetchPriority="high"
            />
            <figcaption>Amara Nest / my Blender render</figcaption>
          </figure>
          <figure className="amara-reference-inset">
            <img
              src="/jewellery/refs/amara-1599.jpg"
              alt="The original ÌTURA Amara heart necklace worn on the neck"
              width={1400}
              height={1600}
            />
            <figcaption>Starting point / ÌTURA</figcaption>
          </figure>
        </div>
        <div className="amara-opening-path">
          <a href="#directions" className="amara-text-link amara-decision-cue">
            Design decisions
            <ArrowDown className="amara-decision-arrow" aria-hidden="true" />
          </a>
        </div>
      </section>

      {children}

      <Reveal
        className="amara-container amara-options amara-options-refined"
        id="directions"
        threshold={0.06}
      >
        <div className="amara-section-heading">
          <p className="amara-kicker">03 / Exploring the companion</p>
          <h2>
            Three ideas
            <br />
            <em>for the earring</em>
          </h2>
          <p>I tried a smaller heart stud, a folded gold stud and a drop.</p>
        </div>
        <div className="amara-direction-gallery">
          {directions.map((item, index) => (
            <MotionArticle className={`amara-direction-card ${item.style}`} key={item.title}>
              <a
                href={item.image}
                aria-haspopup="dialog"
                aria-label={`Open ${item.title} image`}
                className="amara-direction-image"
              >
                <img src={item.image} alt={item.alt} loading="lazy" width={1536} height={1024} />
                <span>{item.label}</span>
              </a>
              <div className="amara-direction-copy">
                <p className="amara-kicker">
                  0{index + 1}
                  {index === 1 ? " / My choice" : ""}
                </p>
                <h3>{item.title}</h3>
                <p>{item.copy}</p>
              </div>
            </MotionArticle>
          ))}
        </div>
      </Reveal>
      <SelectedReveal />
    </>
  );
}

export function AmaraBeautyGallery() {
  return (
    <Reveal id="rendered" className="amara-container amara-beauty-gallery">
      <div className="amara-section-heading">
        <p className="amara-kicker">The finished design / rendered</p>
        <h2>More rendered views</h2>
        <p>I explored the design in light, as a pair and from the reverse.</p>
      </div>
      <div className="amara-render-grid">
        {[
          {
            id: "03",
            alt: "A pair of Amara Nest studs on a reflective gold surface",
            caption: "As a pair",
          },
          {
            id: "04",
            alt: "Amara Nest front and reverse on pale stone",
            caption: "Front & reverse",
          },
          {
            id: "02",
            alt: "A close paired view of Amara Nest studs",
            caption: "The fold in light",
          },
        ].map((item) => (
          <a
            key={item.id}
            href={`/jewellery/amara-nest/beauty/${item.id}.webp`}
            aria-haspopup="dialog"
          >
            <figure>
              <img
                src={`/jewellery/amara-nest/beauty/${item.id}.webp`}
                alt={item.alt}
                width={1920}
                height={1920}
                loading="lazy"
              />
              <figcaption>{item.caption}</figcaption>
            </figure>
          </a>
        ))}
      </div>
    </Reveal>
  );
}
