import { createFileRoute } from "@tanstack/react-router";
import { FilmDetail } from "@/components/film-pages";
import films from "@/data/films.json";
export const Route = createFileRoute("/film/$slug")({head:({params})=>({meta:[{title:(films.find(f=>f.slug===params.slug)?.title||"Film")+" — Deybor 3D"}]}),component:Page});
function Page(){const {slug}=Route.useParams();return <FilmDetail slug={slug}/>;}
