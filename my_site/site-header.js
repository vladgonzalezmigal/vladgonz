class SiteHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <header>
        <h1>Vladimir Gonzalez</h1>
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
