<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  const links = [
		{ name: 'Buttons', path: '/styleguide/buttons' },
		{ name: 'PWA Notification', path: '/styleguide/pwa-notification' },
	];

  let isMobileMenuOpen = false;
  let innerWidth = 0;

  // Close mobile menu when clicking outside or when route changes
  $: if ($page.url.pathname) {
    isMobileMenuOpen = false;
  }

  onMount(() => {
    const handleClickOutside = (event) => {
      const sidebar = document.getElementById('mobile-sidebar');
      const menuButton = document.getElementById('mobile-menu-button');
      
      if (isMobileMenuOpen && sidebar && !sidebar.contains(event.target) && !menuButton.contains(event.target)) {
        isMobileMenuOpen = false;
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  });
</script>

<svelte:window bind:innerWidth />

<div class="min-h-screen bg-gray-50 flex">
  <!-- Mobile Menu Button -->
  <div class="lg:hidden fixed top-4 left-4 z-50">
    <button
      id="mobile-menu-button"
      on:click={() => isMobileMenuOpen = !isMobileMenuOpen}
      class="p-2 rounded-md bg-white shadow-md border border-gray-200 text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
      aria-label="Toggle navigation menu"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        {#if isMobileMenuOpen}
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        {:else}
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        {/if}
      </svg>
    </button>
  </div>

  <!-- Mobile Overlay -->
  {#if isMobileMenuOpen}
    <div class="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40" aria-hidden="true"></div>
  {/if}

  <!-- Sidebar Navigation -->
  <nav 
    id="mobile-sidebar"
    class="
      {isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      fixed lg:static inset-y-0 left-0 z-40
      w-64 lg:w-48 xl:w-64
      bg-white shadow-lg border-r border-gray-200
      transform transition-transform duration-300 ease-in-out
      lg:transform-none
    "
  >
    <div class="p-4 lg:p-6 border-b border-gray-200">
      <h1 class="text-xl lg:text-2xl font-bold text-gray-900">Style Guide</h1>
      <p class="text-xs lg:text-sm text-gray-500 mt-1">Component Library</p>
    </div>

    <div class="p-3 lg:p-4 overflow-y-auto h-full pb-20">
      <ul class="space-y-1 lg:space-y-2">
        {#each links as link}
          <li>
            <a
              href={link.path}
              class="flex items-center px-3 lg:px-4 py-2 lg:py-3 text-sm font-medium rounded-lg transition-colors duration-150 ease-in-out hover:bg-gray-100 {$page.url.pathname === link.path
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                : 'text-gray-700 hover:text-gray-900'}"
            >
              <span class="w-2 h-2 rounded-full mr-2 lg:mr-3 {$page.url.pathname === link.path ? 'bg-blue-500' : 'bg-gray-300'}"></span>
              <span class="truncate">{link.name}</span>
            </a>
          </li>
        {/each}
      </ul>
    </div>
  </nav>

  <!-- Main Content Area -->
  <main class="flex-1 overflow-auto lg:ml-0 {innerWidth < 1024 ? 'ml-0' : ''}">
    <div class="max-w-6xl mx-auto p-4 lg:p-8 {innerWidth < 1024 ? 'pt-16' : ''}">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 min-h-[400px] lg:min-h-[600px]">
        <div class="p-4 lg:p-8">
          <slot />
        </div>
      </div>
    </div>
  </main>
</div>