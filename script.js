/* ==========================================================================
   Fraga Lumiéra - Premium Visual Identity Logic
   Vanilla JS Master Script
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Navigation Scroll Effect
  const header = document.querySelector('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // Mobile Navigation Menu Toggle
  const mobileToggle = document.querySelector('.mobile-menu-toggle');
  const navMenu = document.querySelector('nav');
  
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      // Toggle menu icon state (hamburger / close)
      const isExpanded = navMenu.classList.contains('active');
      mobileToggle.innerHTML = isExpanded ? '&#x2715;' : '&#x2630;';
    });

    // Close menu when clicking nav links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        mobileToggle.innerHTML = '&#x2630;';
      });
    });
  }

  // Catalog Filtering System (SEO-friendly HTML toggle)
  const tabBtns = document.querySelectorAll('.tab-btn');
  const productsGrid = document.querySelector('.products-grid');
  const productCards = document.querySelectorAll('.product-card');

  // Set initial default tab view (Linha Home Care is default)
  filterCatalog('home-care');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Remove active from all tabs
      tabBtns.forEach(b => b.classList.remove('active'));
      // Add active to clicked tab
      btn.classList.add('active');
      
      const filterValue = btn.getAttribute('data-filter');
      filterCatalog(filterValue);
    });
  });

  function filterCatalog(filter) {
    productsGrid.style.display = 'grid';
    
    // Toggle professional OBS note and PDF download buttons styling
    const obsNote = document.querySelector('.professional-obs-note');
    const btnHomeCare = document.getElementById('btn-download-home-care');
    const btnProfessional = document.getElementById('btn-download-professional');
    
    if (obsNote) {
      obsNote.style.display = filter === 'professional' ? 'block' : 'none';
    }
    
    if (btnHomeCare && btnProfessional) {
      if (filter === 'professional') {
        // Professional active
        btnProfessional.className = 'btn-primary';
        btnProfessional.style.background = 'var(--gold-metallic)';
        btnProfessional.style.color = 'var(--bg-dark)';
        btnProfessional.style.border = 'none';
        
        btnHomeCare.className = 'btn-secondary';
        btnHomeCare.style.background = 'transparent';
        btnHomeCare.style.color = 'var(--text-primary)';
        btnHomeCare.style.border = '1px solid rgba(255, 255, 255, 0.2)';
      } else {
        // Home Care active
        btnHomeCare.className = 'btn-primary';
        btnHomeCare.style.background = 'var(--gold-metallic)';
        btnHomeCare.style.color = 'var(--bg-dark)';
        btnHomeCare.style.border = 'none';
        
        btnProfessional.className = 'btn-secondary';
        btnProfessional.style.background = 'transparent';
        btnProfessional.style.color = 'var(--text-primary)';
        btnProfessional.style.border = '1px solid rgba(255, 255, 255, 0.2)';
      }
    }
    
    // Filter cards by class
    productCards.forEach(card => {
      if (card.classList.contains(`${filter}-product`)) {
        card.style.display = 'flex';
        // Trigger a quick layout redraw and fade-in animation
        card.style.opacity = '0';
        card.style.transform = 'translateY(10px)';
        setTimeout(() => {
          card.style.transition = 'var(--transition-smooth)';
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }, 50);
      } else {
        card.style.display = 'none';
      }
    });
  }

  // WhatsApp Order Pre-filled Message Generator
  const orderButtons = document.querySelectorAll('.btn-catalog-action');
  orderButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      
      const card = btn.closest('.product-card');
      const pName = card.querySelector('.product-title').textContent;
      const pId = card.querySelector('.product-id').textContent;
      const pLine = card.classList.contains('professional-product') ? 'Profissional' : 'Home Care';
      
      // Extract cash price
      const pPrice = card.querySelector('.price-value-cash').textContent;
      
      const phoneNum = '5579991389757'; // Brazil (+55) Aracaju (79)
      const textMsg = `Olá, Fraga Lumiéra! Gostaria de fazer um pedido ou saber mais sobre o produto do catálogo:\n\n*Produto:* ${pName} (${pId})\n*Linha:* ${pLine}\n*Valor:* ${pPrice}\n\nComo posso finalizar a compra?`;
      const encodedMsg = encodeURIComponent(textMsg);
      
      const waUrl = `https://wa.me/${phoneNum}?text=${encodedMsg}`;
      window.open(waUrl, '_blank');
    });
  });

});
