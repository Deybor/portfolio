import source from "./printed-objects.json";
export type ObjectView = {
  label?: string;
  kind: string;
  index: number;
  source: string;
  width: number;
  height: number;
  image: string;
  full: string;
};
export type PrintedObject = {
  slug: string;
  title: string;
  modelSource: string;
  card: string;
  views: ObjectView[];
  dimensions?: { width: number; depth: number; height: number };
};
export const printedObjects: PrintedObject[] = source;
export const awardSketches = [
  { page: 2, title: "Rough sketches" },
  { page: 3, title: "Bibles · award designs" },
  { page: 4, title: "Bibles · category designs" },
  { page: 7, title: "Books · award designs" },
  { page: 8, title: "Books · category designs" },
];
