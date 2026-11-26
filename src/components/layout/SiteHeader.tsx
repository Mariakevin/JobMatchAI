export function SiteHeader() {
  return (
    <header className="site-header" id="top">
      <div className="shell site-header__inner">
        <a className="brand" href="#top" aria-label="JobMatch AI home">
          <span className="brand__mark" aria-hidden="true">
            JM
          </span>
          <span className="brand__word">
            jobmatch<span className="brand__period">.</span>ai
          </span>
        </a>
        <p className="site-header__meta">
          <span className="site-header__dot" aria-hidden="true" />
          <span className="mono">DETERMINISTIC · EVIDENCE-BACKED</span>
        </p>
      </div>
    </header>
  );
}
