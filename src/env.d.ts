/// <reference path="../.astro/types.d.ts" />

// Starlight resolves these at build time via Vite virtual modules so it can
// hand a *Starlight-aware* version of each component to overrides like
// `CustomPageSidebar.astro` and `FeedbackFooter.astro`. They have no runtime
// `.d.ts` shipped from `@astrojs/starlight`, so we declare them here as
// `*.astro` modules to keep `astro check` clean.
declare module 'virtual:starlight/components/Pagination' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}

declare module 'virtual:starlight/components/TableOfContents' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}

declare module 'virtual:starlight/components/MobileTableOfContents' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}

declare module 'virtual:starlight/components/SiteTitle' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}

declare module 'virtual:starlight/components/SocialIcons' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}

declare module 'virtual:starlight/components/ThemeSelect' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}

declare module 'virtual:starlight/components/LanguageSelect' {
	const Component: typeof import('astro').AstroComponentFactory;
	export default Component;
}
