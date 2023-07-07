// Get the sidebar and toggle button elements
const sidebar = document.querySelector('.sidebar');
const toggleButton = document.querySelector('.toggle-button');

// Add event listener to the toggle button
toggleButton.addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

// Close the sidebar when clicking outside of it
document.addEventListener('click', (event) => {
  const targetElement = event.target;
  const isClickInsideSidebar = sidebar.contains(targetElement);
  const isClickOnToggleButton = targetElement.classList.contains('toggle-button');

  if (!isClickInsideSidebar && !isClickOnToggleButton) {
    sidebar.classList.remove('open');
  }
});
