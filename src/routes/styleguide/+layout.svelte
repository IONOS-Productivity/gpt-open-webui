<script lang="ts">
  import { page } from '$app/stores';

  const links = [
		{ name: 'Buttons', path: '/styleguide/buttons' },
		{ name: 'PWA Notification', path: '/styleguide/pwa-notification' },
	];
</script>

<div class="min-h-screen bg-gray-50 flex">
  <!-- Sidebar Navigation -->
  <nav class="w-64 bg-white shadow-lg border-r border-gray-200 flex-shrink-0">
    <div class="p-6 border-b border-gray-200">
      <h1 class="text-2xl font-bold text-gray-900">Style Guide</h1>
      <p class="text-sm text-gray-500 mt-1">Component Library</p>
    </div>
    
    <div class="p-4">
      <ul class="space-y-2">
        {#each links as link}
          <li>
            <a
              href={link.path}
              class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-150 ease-in-out hover:bg-gray-100 {$page.url.pathname === link.path 
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' 
                : 'text-gray-700 hover:text-gray-900'}"
            >
              <span class="w-2 h-2 rounded-full mr-3 {$page.url.pathname === link.path ? 'bg-blue-500' : 'bg-gray-300'}"></span>
              {link.name}
            </a>
          </li>
        {/each}
      </ul>
    </div>
  </nav>

  <!-- Main Content Area -->
  <main class="flex-1 overflow-auto">
    <div class="max-w-6xl mx-auto p-8">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 min-h-[600px]">
        <div class="p-8">
          <slot />
        </div>
      </div>
    </div>
  </main>
</div>