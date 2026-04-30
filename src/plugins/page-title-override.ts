import type { StarlightPlugin } from '@astrojs/starlight/types';

/**
 * Re-applies the custom PageTitle override after other plugins
 * (like starlight-sidebar-topics) have run.
 *
 * Starlight's `updateConfig` shallow-merges at the top level — passing
 * `{ components: { PageTitle } }` would wipe out Head, Search, Footer,
 * and Sidebar overrides that earlier plugins/user config set. So we
 * spread `config.components` first to preserve everything.
 */
export default function pageTitleOverride(): StarlightPlugin {
  return {
    name: 'page-title-override',
    hooks: {
      'config:setup'({ config, updateConfig }) {
        updateConfig({
          components: {
            ...config.components,
            PageTitle: './src/components/CustomPageTitle.astro',
          },
        });
      },
    },
  };
}
