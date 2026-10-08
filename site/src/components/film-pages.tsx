import { useState } from "react";
const asset=(path:string)=>path.startsWith(import.meta.env.BASE_URL) ? path : import.meta.env.BASE_URL+path.replace(/^\//, "");
import films from "@/data/films.json";
export function FilmIndex() {
 const [filter,setFilter]=useState("All films");
 const categories=["All films","Automotive explainer","Documentary animation","Product film","Narrative short"];
 const shown=films.filter(f=>filter==="All films"||f.kind===filter);
 return <main className="home film-page" id="content">
 <section className="intro"><p className="eyebrow">Adesina Adebola / Film</p><h1>Stories.<br/><em>In motion.</em></h1><div className="intro-bottom"><p>3D animation that brings stories, products<br/>and mechanical ideas into view.</p><a className="text-link" href="#films">Explore the films <span aria-hidden="true">↓</span></a></div></section>
 <section className="film-selection" id="films"><div className="section-heading"><h2>Selected films <span>/ 05</span></h2><p>Explanation. Character. Movement.</p></div>
 <div className="filters" role="group" aria-label="Filter films">{categories.map(c=><button key={c} className={filter===c?"active":""} aria-pressed={filter===c} onClick={()=>setFilter(c)}>{c}</button>)}</div><p className="sr-only" role="status">Showing {shown.length} films</p>
 <div className="film-grid">{shown.map((f,i)=><a className={f.slug==="lotus-drivetrain"?"film-card film-feature":"film-card"} href={asset("/film/"+f.slug)} key={f.slug}><div className={"film-cover "+(f.format==="Portrait"?"portrait":"")}><img src={asset(f.poster)} alt={f.title+" — "+f.subtitle} loading={i?"lazy":"eager"}/><span className="film-play">Watch film ↗</span><span className="film-duration">{f.duration}</span></div><div className="film-card-copy"><div><p>{f.kind}</p><h3>{f.title}</h3><span>{f.subtitle}</span></div><span aria-hidden="true">↗</span></div></a>)}</div></section>
 <section className="film-contact"><h2>Have a story to tell?</h2><a className="text-link" href="mailto:deybor4l@gmail.com">Let’s talk ↗</a></section></main>
}
export function FilmDetail({slug}:{slug:string}) {
 const film=films.find(f=>f.slug===slug);
 if(!film) return <main className="film-page" id="content"><h1>Film not found</h1><a href={asset("/film")}>Browse films</a></main>;
 const next=films[(films.indexOf(film)+1)%films.length];
 return <main className="home film-page film-detail" id="content"><section className="film-title"><a className="text-link" href={asset("/film")}>← All films</a><p className="eyebrow">{film.kind} / {film.duration}</p><h1>{film.title}</h1><p className="film-subtitle">{film.subtitle}</p><p className="film-summary">{film.summary}</p></section>
 <section className={"film-player "+(film.format==="Portrait"?"portrait-player":"")} aria-label={film.title+" video"}><video controls playsInline preload="metadata" poster={asset(film.poster)} src={asset(film.video)}>Your browser does not support this video. <a href={asset(film.video)}>Download the film</a>.</video></section>
 <section className="film-notes"><div><h2>The sequence</h2><p>{film.notes}</p><a className="text-link" href={asset(film.video)} download>Download film ↓</a></div><div><h2>Production notes</h2><p>{film.credit}</p>{film.links.length>0&&<p className="film-credits">{film.links.map(([label,url])=><a href={url} key={url} target="_blank" rel="noreferrer">{label} ↗</a>)}</p>}</div></section>
 <a className="film-next" href={asset("/film/"+next.slug)}><span>Next film</span><h2>{next.title} ↗</h2></a></main>
}
