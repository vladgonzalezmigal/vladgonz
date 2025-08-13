class SiteHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <header>
        <div style="display: flex; align-items: center; gap: 1rem;">
          <a href="https://youtu.be/byk9a1Mmf58?si=FRcVi2BZJMF6iHc3" target="_blank" rel="noopener">
            <img src="img/carlson.JPG" alt="Profile" style="width:56px;height:56px;object-fit:cover;border-radius:50%;border:2px solid #eee;">
          </a>
          <h1 style="margin: 0;">Vladimir Gonzalez</h1>
        </div>
        <nav class="top-links">
          <ul>
            <li><a href="index.html#professional-experience">Professional Experience</a></li>
            <li><a href="index.html#portfolio-philosophy">Portfolio Philosophy</a></li>
            <li><a href="index.html#tools-section">Tools</a></li>
          </ul>
        </nav>
      </header>
    `;
  }
}

customElements.define('site-header', SiteHeader);
