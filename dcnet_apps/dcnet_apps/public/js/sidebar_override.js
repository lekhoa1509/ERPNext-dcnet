// Override sidebar URL links to open in same tab (SPA navigation)
// Use capture phase to intercept before Frappe's router

document.addEventListener('click', function(e) {
	// Find closest anchor tag
	const link = e.target.closest('.sidebar-item-container a[href^="/app/"]');

	if (link && link.getAttribute('target') === '_blank') {
		const href = link.getAttribute('href');

		if (href) {
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();

			// Use Frappe SPA navigation
			frappe.set_route(href);
		}
	}
}, true); // true = capture phase (runs before bubble phase)


// ========================================
// Sidebar Accordion Behavior
// When one section opens, close other sections
// ========================================

(function() {
	'use strict';

	// Use MutationObserver to detect when sections open/close
	let observer = null;

	$(document).ready(function() {
		setTimeout(setupSidebarAccordion, 500);
	});

	$(document).on('page-change', function() {
		setTimeout(setupSidebarAccordion, 500);
	});

	function setupSidebarAccordion() {
		const sidebar = document.querySelector('.body-sidebar');
		if (!sidebar) return;

		// Disconnect existing observer
		if (observer) {
			observer.disconnect();
		}

		// Watch for changes in drop-icon (chevron direction changes)
		observer = new MutationObserver(function(mutations) {
			mutations.forEach(function(mutation) {
				if (mutation.type === 'attributes' && mutation.attributeName === 'href') {
					const target = mutation.target;
					if (target.tagName === 'use' && target.closest('.drop-icon')) {
						const newHref = target.getAttribute('href');
						// If this icon just changed to "open" state
						if (newHref === '#icon-chevron-down') {
							const container = target.closest('.sidebar-item-container.section-item');
							if (container) {
								closeOtherSections(container, sidebar);
							}
						}
					}
				}
			});
		});

		// Observe all drop-icon use elements
		const dropIcons = sidebar.querySelectorAll('.sidebar-item-container.section-item .drop-icon use');
		dropIcons.forEach(function(icon) {
			observer.observe(icon, { attributes: true, attributeFilter: ['href'] });
		});

		console.log('[Accordion] Watching', dropIcons.length, 'section icons');
	}

	function closeOtherSections(currentContainer, sidebar) {
		const sectionItems = sidebar.querySelectorAll('.sidebar-item-container.section-item');

		sectionItems.forEach(function(container) {
			if (container === currentContainer) return;

			const dropIcon = container.querySelector('.drop-icon use');
			if (!dropIcon) return;

			// Check if this section is open
			const isOpen = dropIcon.getAttribute('href') === '#icon-chevron-down';

			if (isOpen) {
				// Click the standard-sidebar-item to close it
				const clickableItem = container.querySelector('.standard-sidebar-item');
				if (clickableItem) {
					clickableItem.click();
				}
			}
		});
	}
})();
