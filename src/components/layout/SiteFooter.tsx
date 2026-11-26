export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="shell site-footer__inner">
        <div className="site-footer__brand">
          <span className="brand__mark brand__mark--small" aria-hidden="true">
            JM
          </span>
          <div>
            <p className="site-footer__name">
              jobmatch<span className="brand__period">.</span>ai
            </p>
            <p className="site-footer__line">
              Deterministic by design. Your resume stays in memory.
            </p>
          </div>
        </div>
        <p className="site-footer__status mono">
          <span className="status-led" aria-hidden="true" />
          V0.2.0 · STUDENT-SIDE DECISION SUPPORT
        </p>
      </div>
    </footer>
  );
}
