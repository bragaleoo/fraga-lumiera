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
  const lookbookContainer = document.querySelector('.lookbook-container');
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
    if (filter === 'lookbook') {
      // Hide product grid and show lookbook slider
      productsGrid.style.display = 'none';
      lookbookContainer.classList.add('active');
    } else {
      // Show product grid and hide lookbook slider
      productsGrid.style.display = 'grid';
      lookbookContainer.classList.remove('active');
      
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
  }

  // Lookbook Slider Interaction
  const lookbookSlider = document.querySelector('.lookbook-slider');
  const slides = document.querySelectorAll('.lookbook-slide');
  const prevBtn = document.querySelector('.lookbook-arrow.prev');
  const nextBtn = document.querySelector('.lookbook-arrow.next');
  const pagCurrent = document.querySelector('.lookbook-page-current');
  const pagTotal = document.querySelector('.lookbook-page-total');
  const lookbookTabBtns = document.querySelectorAll('.lookbook-tab-btn');

  let currentSlide = 0;
  let activeCatalog = 'home_care'; // home_care or professional
  let totalPages = 7;
  
  if (pagTotal) pagTotal.textContent = totalPages;

  // Render initial lookbook state based on active catalog
  updateLookbookSlides();

  lookbookTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      lookbookTabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCatalog = btn.getAttribute('data-catalog');
      currentSlide = 0;
      updateLookbookSlides();
    });
  });

  if (prevBtn && nextBtn && lookbookSlider) {
    nextBtn.addEventListener('click', () => {
      if (currentSlide < totalPages - 1) {
        currentSlide++;
        slideLookbook();
      } else {
        currentSlide = 0; // Wrap around
        slideLookbook();
      }
    });

    prevBtn.addEventListener('click', () => {
      if (currentSlide > 0) {
        currentSlide--;
        slideLookbook();
      } else {
        currentSlide = totalPages - 1; // Wrap around
        slideLookbook();
      }
    });
  }

  function updateLookbookSlides() {
    totalPages = activeCatalog === 'home_care' ? 7 : 11;
    if (pagTotal) pagTotal.textContent = totalPages;

    if (lookbookSlider) {
      lookbookSlider.innerHTML = '';
      for (let i = 1; i <= totalPages; i++) {
        const slide = document.createElement('div');
        slide.classList.add('lookbook-slide');
        
        const img = document.createElement('img');
        img.src = `assets/pages/${activeCatalog}_page_${i}.jpg`;
        img.alt = `Catálogo ${activeCatalog === 'home_care' ? 'Home Care' : 'Profissional'} - Página ${i}`;
        
        slide.appendChild(img);
        lookbookSlider.appendChild(slide);
      }
    }
    currentSlide = 0;
    slideLookbook();
  }

  function slideLookbook() {
    if (lookbookSlider) {
      lookbookSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
      if (pagCurrent) pagCurrent.textContent = currentSlide + 1;
    }
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

  // Intersection Observer for scroll-reveal micro-animations
  const sections = document.querySelectorAll('section');
  const animOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('section-visible');
        observer.unobserve(entry.target);
      }
    });
  }, animOptions);

  // Set animation classes
  sections.forEach(sec => {
    sec.style.opacity = '0';
    sec.style.transform = 'translateY(25px)';
    sec.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
    observer.observe(sec);
  });

  // Custom CSS style insert for section reveal
  const styleSheet = document.createElement("style");
  styleSheet.innerText = `
    .section-visible {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  `;
  document.head.appendChild(styleSheet);
});
