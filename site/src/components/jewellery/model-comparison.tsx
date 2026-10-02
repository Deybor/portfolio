import { useRef, useState, type CSSProperties, type PointerEvent } from "react";

const asset = "/jewellery/amara-nest/model49/";

export function ModelComparison() {
  const [split, setSplit] = useState(50);
  const stage = useRef<HTMLDivElement>(null);
  const moveSplit = (event: PointerEvent<HTMLDivElement>) => {
    const bounds = stage.current?.getBoundingClientRect();
    if (bounds)
      setSplit(
        Math.round(
          Math.max(0, Math.min(100, ((event.clientX - bounds.left) / bounds.width) * 100)),
        ),
      );
  };
  return (
    <figure className="amara-model-comparison">
      <div className="amara-model-toolbar">
        <span>Blender / Amara Nest</span>
        <span>Material &amp; wireframe comparison</span>
      </div>
      <div
        ref={stage}
        className="amara-model-split"
        style={{ "--model-split": `${split}%` } as CSSProperties}
      >
        <img
          src={`${asset}oblique-render-hdri.webp`}
          alt="Amara Nest model with its gold and stone materials"
          width={1200}
          height={1000}
          loading="lazy"
        />
        <div className="amara-model-wire">
          <img
            src={`${asset}oblique-wire.webp`}
            alt="The matching Amara Nest view with actual mesh edges visible"
            width={1200}
            height={1000}
            loading="lazy"
          />
        </div>
        <span className="amara-model-label is-wire">Wireframe</span>
        <span className="amara-model-label is-render">Render</span>
        <div
          className="amara-model-divider"
          role="slider"
          tabIndex={0}
          aria-label="Drag to compare wireframe and render"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={split}
          aria-valuetext={`${split}% wireframe, ${100 - split}% render`}
          onPointerDown={(event) => {
            event.currentTarget.setPointerCapture(event.pointerId);
            moveSplit(event);
          }}
          onPointerMove={(event) => {
            if (event.currentTarget.hasPointerCapture(event.pointerId)) moveSplit(event);
          }}
          onPointerUp={(event) => {
            if (event.currentTarget.hasPointerCapture(event.pointerId))
              event.currentTarget.releasePointerCapture(event.pointerId);
          }}
          onKeyDown={(event) => {
            const step = event.shiftKey ? 10 : 1;
            const values: Record<string, number> = {
              ArrowLeft: split - step,
              ArrowDown: split - step,
              ArrowRight: split + step,
              ArrowUp: split + step,
              Home: 0,
              End: 100,
            };
            if (event.key in values) {
              event.preventDefault();
              setSplit(Math.max(0, Math.min(100, values[event.key])));
            }
          }}
        >
          <b aria-hidden="true">↔︎</b>
        </div>
      </div>
      <figcaption>
        <label htmlFor="amara-model-split">Compare wireframe and render</label>
        <input
          id="amara-model-split"
          type="range"
          min="0"
          max="100"
          value={split}
          onChange={(event) => setSplit(Number(event.target.value))}
          aria-valuetext={`${split}% wireframe, ${100 - split}% render`}
        />
      </figcaption>
    </figure>
  );
}
