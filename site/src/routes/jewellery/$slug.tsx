import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { JewelleryPiecePage } from "@/components/jewellery/piece-page";
import { jewelleryPieces } from "@/lib/jewellery-pieces";

export const Route = createFileRoute("/jewellery/$slug")({
  loader: ({ params }) => {
    const piece = jewelleryPieces.find((item) => item.slug === params.slug);
    if (!piece) throw notFound();
    return piece;
  },
  head: ({ loaderData }) => ({
    meta: [{ title: `${loaderData?.title ?? "Jewellery"} — Adesina Adebola` }],
  }),
  component: PieceRoute,
  notFoundComponent: () => (
    <main className="collection" id="content">
      <div className="collection-wrap collection-intro">
        <div>
          <h1>Piece not found</h1>
          <Link className="collection-link" to="/jewellery">
            Browse jewellery →
          </Link>
        </div>
      </div>
    </main>
  ),
});
function PieceRoute() {
  const piece = Route.useLoaderData();
  return <JewelleryPiecePage key={piece.slug} piece={piece} />;
}
