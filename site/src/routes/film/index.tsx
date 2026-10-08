import { createFileRoute } from "@tanstack/react-router";
import { FilmIndex } from "@/components/film-pages";
export const Route = createFileRoute("/film/")({ head:()=>({meta:[{title:"Film — Deybor 3D"},{name:"description",content:"Automotive explanation, documentary reconstruction and animated stories by Adesina Adebola."}]}), component:FilmIndex });
