import { Link } from "@tanstack/react-router";
import { ChapterRail, DeckProgress, Reveal, useActiveChapter } from "@/components/jewellery/stage";

const chapters = [
  { id: "bench-open", label: "Open" },
  { id: "nest", label: "Nest" },
];

export function WorkbenchPage() {
  const active = useActiveChapter(chapters.map((chapter) => chapter.id));

  return (
    <main className="jewel deck" id="content">
      <DeckProgress />
      <ChapterRail items={chapters} active={active} />

      <Reveal className="plate plate-hero" id="bench-open">
        <div className="plate-copy">
          <p className="index-label line">3D modelling and technical drawings</p>
          <h1 className="line">The Workbench</h1>
          <p className="lede line">
            My Amara model views, measured drawings and technical specification.
          </p>
        </div>
        <figure className="plate-frame">
          <img
            className="shot shot-final-cad"
            src="/jewellery/amara-nest/03-profile.png"
            alt="Profile model view of the Amara Nest stud"
          />
        </figure>
      </Reveal>

      <div className="tech">
        <div className="jewel-wrap bench-list">
          <article id="nest">
            <p className="index-label">01 — Amara Nest / design development</p>
            <h2>Nest stud</h2>
            <p className="prose">
              A folded shell frames the heart-cut CZ, with a rear attachment boss and post.
              Mirrored pair; physical fit and earring-back selection TBC.
            </p>
            <figure className="sheet">
              <img
                className="nest-sheet-drawing"
                src="/jewellery/amara-nest/sketches49/amara-sketches.svg"
                alt="Model-derived sketch sheet of Amara Nest: front, side and back"
              />
              <figcaption className="sheet-cap">
                <span>Plate 01</span>
                <strong>Nest · 9.04 W × 9.34 H mm</strong>
                <span>Model dimensions · physical sample pending</span>
              </figcaption>
            </figure>
            <table className="spec">
              <caption>Design model · review dimensions in millimetres</caption>
              <tbody>
                <tr>
                  <th scope="row">Head</th>
                  <td>9.04 W × 9.34 H × 5.58 D, including rear boss</td>
                </tr>
                <tr>
                  <th scope="row">Stone</th>
                  <td>Clear heart-cut cubic zirconia (CZ); model size 6.00 × 6.00 × 3.55 mm</td>
                </tr>
                <tr>
                  <th scope="row">Post</th>
                  <td>
                    Model envelope 0.92 × 10.60 mm; matching back TBC
                  </td>
                </tr>
                <tr>
                  <th scope="row">Proposed metal / finish</th>
                  <td>
                    925 sterling silver with 18K gold vermeil; proposed
                  </td>
                </tr>
                <tr>
                  <th scope="row">Status</th>
                  <td>Digital design study; physical sample approval pending</td>
                </tr>
              </tbody>
            </table>
            <a
              className="spec-download"
              href="/jewellery/amara-nest/specification.html"
              target="_blank"
              rel="noopener noreferrer"
            >
              Open the full specification <span aria-hidden="true">↗</span>
            </a>
          </article>
        </div>
      </div>

      <div className="jewel-wrap">
        <nav className="next-room" aria-label="Continue">
          <Link to="/jewellery/amara">← Amara study</Link>
          <a href="/#work">Back to work</a>
        </nav>
      </div>
    </main>
  );
}
