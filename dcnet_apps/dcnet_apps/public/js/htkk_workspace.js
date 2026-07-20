// Auto-redirect HTKK workspace to Vue list UI
frappe.router.on('change', () => {
  const route = frappe.get_route_str();
  // Handle both possible route formats
  if (route === 'Workspaces/HTKK' || route === 'Workspace/HTKK' || route === 'htkk') {
    // Redirect to Vue list
    window.location.href = '/htkk_list';
  }
});

// Also handle direct navigation via URL
$(document).ready(() => {
  if (window.location.pathname === '/desk/htkk' || window.location.pathname === '/app/htkk') {
    window.location.href = '/htkk_list';
  }
});
