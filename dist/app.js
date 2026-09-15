const projects=[
{id:'sound',title:'Sound in context',category:'Product',label:'Product / Lifestyle setting',cover:'speaker-wide.webp',images:[['speaker-wide.webp','A warm setting for an orange portable speaker.'],['speaker-detail.webp','A closer view of the grille, lighting, and wood surface.']],intro:'A portable speaker, placed in the warmth of an everyday interior.',focus:'The scene pairs a saturated orange speaker with warm timber and soft background lighting. The two viewpoints move from a balanced product composition to a closer material study.',details:'Fine grille detail, wood grain, and a shallow depth of field give a familiar object a tactile presence.'},
{id:'titan',title:'A new perspective on flight',category:'Product',label:'Titan Air Mobility / eVTOL visualization',cover:'titan-air.webp',fit:'contain',images:[['titan-air.webp','eVTOL aircraft visualization for Titan Air Mobility.']],intro:'An eVTOL aircraft visualization created for Titan Air Mobility.',focus:'An elevated three-quarter view brings the cabin, wings, and rotor arrangement into one composition. Directional light traces the aircraft against a dark setting.',details:'3D visualization with a focus on the aircraft form, reflective surfaces, and lighting.'},
{id:'strongfood',title:'Strong Bar — Variant A',category:'Product',label:'StrongFood / Packaging visualization',cover:'strong-box-yellow.webp',fit:'contain',images:[['strong-bar-yellow.webp','Chocolate Hazelnut — Variant A bar.'],['strong-box-yellow.webp','Chocolate Hazelnut — matching display carton.'],['strong-bar-blue.webp','White Blueberry — Variant A bar.'],['strong-box-blue.webp','White Blueberry — matching display carton.'],['strong-bar-green.webp','Dark Choc Peanut Flavour — Variant A bar.'],['strong-box-green.webp','Dark Choc Peanut Flavour — matching display carton.']],intro:'Bar and display-carton visualizations for StrongFood, bringing the Variant A range together across three flavours.',focus:'Yellow, blue, and green distinguish the three variants. Each wrapper is paired with its matching retail carton to show the packaging as a complete range.',details:'3D packaging visualization across individual wrappers and filled display cartons.'},
{id:'serum',title:'A quieter kind of luxury',category:'Beauty',label:'Beauty / Product visualization',cover:'serum.webp',images:[['serum.webp','A minimal daylight composition with a glass platform.'],['serum-spa.webp','The serum in a candlelit spa setting.']],intro:'Two visual worlds for the same serum: quiet daylight and a richly layered spa scene.',focus:'The first image uses a restrained palette and directional shadows. The second introduces towels, stone, candles, and botanicals to place the product in a ritual of care.',details:'Dark glass anchors both compositions, while reflections and soft-focus backgrounds separate the product from its surroundings.'},
{id:'headset',title:'Form in suspension',category:'Product',label:'Technology / Product visualization',cover:'headset.webp',images:[['headset.webp','Multiple headset views arranged against a white background.']],intro:'A study of repeated form, reflective surfaces, and a vivid orange accent.',focus:'Suspended headsets create a rhythmic composition. Different angles reveal the curved faceplate, padded interior, and woven strap.',details:'Glossy black, soft fabric, and metallic components sit together in a high-contrast lighting treatment.'},
{id:'skincare',title:'Daily essentials',category:'Beauty',label:'Beauty / Packaging visualization',cover:'skincare.webp',images:[['skincare.webp','A diagonal arrangement of two skincare products with foliage shadows.']],intro:'A skincare pairing framed by soft shadows, clear droplets, and pale surfaces.',focus:'A diagonal layout introduces movement to a still image, while the contrasting labels keep each product distinct.',details:'Subtle translucency and reflected light support the clean, fresh feel of the composition.'},
{id:'gpu',title:'Engineered in light',category:'Product',label:'Technology / Product visualization',cover:'gpu-detail.webp',images:[['gpu-detail.webp','A close study of graphics card fans and metallic surfaces.'],['gpu.webp','Two graphics cards shown in an upright composition.']],intro:'Graphics card studies exploring technical detail and cool, sculptural lighting.',focus:'Two compositions present the RTX 3080 form at different scales, from the cooling fans and layered fins to the full silhouette.',details:'Blue highlights against silver and black surfaces emphasize the geometry and repetition of the cooling assembly.'},
{id:'candles',title:'After the flame',category:'Beauty',label:'Lifestyle / Lighting study',cover:'candles.webp',images:[['candles.webp','Glass candles on a wooden table, with a smoke trail and blurred background lights.']],intro:'A still life built around the moment just after a candle goes out.',focus:'A fine trail of smoke draws attention to the foreground candle. The second flame and distant lights carry warmth through the scene.',details:'Glass, wax, wood, and smoke offer contrasting surfaces within a single low-light composition.'},
{id:'energy',title:'Energy in motion',category:'Motion',label:'Motion / Product film',cover:'energy-film.jpg',video:'energy-film.mp4',images:[['energy.webp','A close product detail with cyan fluid and condensation.']],intro:'A product animation exploring energy, surface detail, and movement.',focus:'Watch the film for the full sequence, with a still frame below for a closer look at the product treatment.',details:'Product animation and rendering created in Blender.'},
{id:'fluid',title:'Fluid study',category:'Motion',label:'Motion / Fluid animation',cover:'fluid-film.jpg',video:'fluid-film.mp4',images:[],intro:'A short exploration of fluid movement around a product.',focus:'The clip brings flowing forms into a product scene, exploring the relationship between the object and the surrounding motion.',details:'Animation study created in Blender.'},
{id:'black',title:'Industrial form',category:'Motion',label:'dev.tools / Industrial visualization',cover:'dev-tools-workshop.webp',fit:'contain',video:'black-film.mp4',images:[['dev-tools-workshop.webp','PC enclosures in a workshop setting, created for dev.tools.']],intro:'An industrial form study for dev.tools, pairing a rotating enclosure animation with a workshop scene.',focus:'The film explores the perforated structure in motion. The still places three enclosure configurations among tools and computer components.',details:'3D visualization and animation created in Blender.'},
{id:'motion',title:'The reveal',category:'Motion',label:'Motion / Animation',cover:'motion-film.jpg',video:'motion-film.mp4',images:[],intro:'A restrained packaging reveal, moving from darkness into light.',focus:'Close framing and directional highlights gradually reveal a pale, branded package against a black background.',details:'Animation created in Blender.'}
];
const grid=document.querySelector('#projects');
const dialog=document.querySelector('#case-study');
let activeFilter='All',opener=null;
function render(filter='All'){
 activeFilter=filter;
 const shown=projects.filter(p=>filter==='All'||p.category===filter);
 grid.innerHTML=shown.map(p=>`<button class="project" data-project="${p.id}" aria-label="View ${p.title} case study"><div class="project-image ${p.fit==='contain'?'project-image-contain':''}"><img src="assets/${p.cover}" alt="${p.title}" loading="lazy" width="1080" height="1080">${p.video?'<span class="play-tag">▶ PLAY FILM</span>':''}</div><div class="project-info"><div><h3>${p.title}</h3><span class="category">${p.label}</span></div><span class="arrow" aria-hidden="true">↗</span></div></button>`).join('');
 document.querySelector('#result-status').textContent=`Showing ${shown.length} ${filter==='All'?'':filter.toLowerCase()+' '}projects`;
 document.querySelectorAll('[data-filter]').forEach(b=>{const on=b.dataset.filter===filter;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on))});
}
function openProject(id,trigger){
 const p=projects.find(p=>p.id===id);if(!p)return;
 if(trigger)opener=trigger;
 const next=projects[(projects.indexOf(p)+1)%projects.length];
 const media=(p.video?`<figure class="case-media"><video controls playsinline preload="metadata" poster="assets/${p.cover}" aria-label="${p.title} film"><source src="assets/${p.video}" type="video/mp4">Your browser cannot play this video. <a href="assets/${p.video}">Download the film</a>.</video><figcaption>Play the film · Sound controls available in the player</figcaption></figure>`:'')+p.images.map(([img,caption])=>`<figure class="case-media"><img src="assets/${img}" alt="${caption}" loading="lazy"><figcaption>${caption}</figcaption></figure>`).join('');
 document.querySelector('#case-content').innerHTML=`<div class="case-head"><p class="eyebrow">${p.label}</p><h2 id="case-title">${p.title}</h2><p>${p.intro}</p></div>${media}<div class="case-details"><div><h3>Visual approach</h3><p>${p.focus}</p></div><div><h3>Details & craft</h3><p>${p.details}</p></div></div><div class="case-footer"><a class="text-link" href="mailto:deybor4l@gmail.com?subject=${encodeURIComponent('Project enquiry — '+p.title)}">Discuss a similar project ↗</a><button class="case-next" data-next="${next.id}">Next: ${next.title} →</button></div>`;
 if(!dialog.open){dialog.showModal();document.body.classList.add('modal-open')}
 dialog.scrollTop=0;
 document.querySelector('.close').focus({preventScroll:true});
}
document.addEventListener('click',e=>{
 const filter=e.target.closest('[data-filter]');if(filter)render(filter.dataset.filter);
 const card=e.target.closest('[data-project]');if(card)openProject(card.dataset.project,card);
 const next=e.target.closest('[data-next]');if(next)openProject(next.dataset.next);
});
document.querySelector('.close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
dialog.addEventListener('close',()=>{dialog.querySelectorAll('video').forEach(v=>v.pause());document.body.classList.remove('modal-open');opener?.focus({preventScroll:true})});
render();

const carousel=document.querySelector('.featured-carousel');
const track=carousel.querySelector('.featured-track');
const slides=[...carousel.querySelectorAll('.featured-slide')];
const dots=[...carousel.querySelectorAll('[data-slide]')];
const pauseButton=carousel.querySelector('.featured-pause');
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
let featuredIndex=0,featuredTimer=null,featuredPaused=reducedMotion.matches;
function scheduleFeatured(){
 clearTimeout(featuredTimer);
 if(featuredPaused||document.hidden||dialog.open||carousel.contains(document.activeElement))return;
 featuredTimer=setTimeout(()=>showFeatured(featuredIndex+1),6000);
}
function showFeatured(index,manual=false){
 featuredIndex=(index+slides.length)%slides.length;
 track.style.transform=`translateX(-${featuredIndex*100}%)`;
 slides.forEach((slide,i)=>{slide.inert=i!==featuredIndex;slide.setAttribute('aria-hidden',String(i!==featuredIndex))});
 dots.forEach((dot,i)=>dot.setAttribute('aria-pressed',String(i===featuredIndex)));
 carousel.querySelector('.featured-count').textContent=`0${featuredIndex+1} / 03`;
 if(manual)carousel.querySelector('.featured-status').textContent=slides[featuredIndex].getAttribute('aria-label');
 scheduleFeatured();
}
function syncFeaturedPause(){pauseButton.textContent=featuredPaused?'Play':'Pause';pauseButton.setAttribute('aria-label',featuredPaused?'Play slideshow':'Pause slideshow')}
carousel.querySelector('.featured-prev').addEventListener('click',()=>showFeatured(featuredIndex-1,true));
carousel.querySelector('.featured-next').addEventListener('click',()=>showFeatured(featuredIndex+1,true));
dots.forEach(dot=>dot.addEventListener('click',()=>showFeatured(Number(dot.dataset.slide),true)));
pauseButton.addEventListener('click',()=>{featuredPaused=!featuredPaused;syncFeaturedPause();scheduleFeatured()});
carousel.addEventListener('focusin',()=>clearTimeout(featuredTimer));
carousel.addEventListener('focusout',()=>setTimeout(scheduleFeatured,0));
carousel.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();if(e.target.closest('.featured-slide'))pauseButton.focus();showFeatured(featuredIndex+(e.key==='ArrowRight'?1:-1),true)}});
let touchStart=null,suppressFeaturedClick=false;
const featuredWindow=carousel.querySelector('.featured-window');
featuredWindow.addEventListener('touchstart',e=>{touchStart={x:e.touches[0].clientX,y:e.touches[0].clientY};clearTimeout(featuredTimer)},{passive:true});
featuredWindow.addEventListener('touchend',e=>{if(!touchStart)return;const dx=e.changedTouches[0].clientX-touchStart.x,dy=e.changedTouches[0].clientY-touchStart.y;touchStart=null;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)){suppressFeaturedClick=true;showFeatured(featuredIndex+(dx<0?1:-1),true);setTimeout(()=>suppressFeaturedClick=false,400)}else scheduleFeatured()},{passive:true});
featuredWindow.addEventListener('touchcancel',()=>{touchStart=null;scheduleFeatured()},{passive:true});
featuredWindow.addEventListener('click',e=>{if(suppressFeaturedClick){e.preventDefault();e.stopPropagation();suppressFeaturedClick=false}},true);
document.addEventListener('visibilitychange',scheduleFeatured);
dialog.addEventListener('close',scheduleFeatured);
new MutationObserver(scheduleFeatured).observe(dialog,{attributes:true,attributeFilter:['open']});
reducedMotion.addEventListener('change',()=>{featuredPaused=reducedMotion.matches;syncFeaturedPause();scheduleFeatured()});
syncFeaturedPause();scheduleFeatured();
