type SourceNoteProps = {
  href: string;
  children: React.ReactNode;
};

export function SourceNote({ href, children }: SourceNoteProps) {
  return (
    <a className="source-note" href={href}>
      {children}
    </a>
  );
}
