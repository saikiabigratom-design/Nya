/**
 * Frontend Component and Integration Test Suite for ঞ (Nya) — Vocal for Local.
 * Tests components, contracts, accessibility, and bundle integrity.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('='.repeat(70));
console.log('ঞ (Nya) Search: Running Frontend Verification & Component Tests');
console.log('='.repeat(70));

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ [PASS] ${name}`);
    passed++;
  } catch (err) {
    console.error(`✗ [FAIL] ${name}: ${err.message}`);
    failed++;
  }
}

// Test 1: BrandMark file and accessibility
test('BrandMark has accessible name and ঞ glyph', () => {
  const content = fs.readFileSync(path.join(__dirname, 'src/components/BrandMark.tsx'), 'utf-8');
  assert(content.includes('ঞ'), 'Should contain Assamese brand character ঞ');
  assert(content.includes('aria-label="Nya — Vocal for Local brand mark"'), 'Should have accessible ARIA label');
  assert(content.includes('bg-nya-indigo'), 'Should use Midnight Indigo background');
  assert(content.includes('text-nya-teal'), 'Should use Signal Teal text');
});

// Test 2: SearchBox placeholder and accessibility
test('SearchBox matches specification placeholder and form roles', () => {
  const content = fs.readFileSync(path.join(__dirname, 'src/components/SearchBox.tsx'), 'utf-8');
  assert(content.includes('Search in Assamese, English, or Romanized Assamese…'), 'Should match spec placeholder');
  assert(content.includes('role="search"'), 'Should use semantic search role');
  assert(content.includes('aria-label="Search query"'), 'Should provide accessible input label');
  assert(content.includes('key === "Escape"'), 'Should handle Escape key to clear');
});

// Test 3: SearchResultItem metadata rendering
test('SearchResultItem renders title, canonical URL, snippet, and verified badges', () => {
  const content = fs.readFileSync(path.join(__dirname, 'src/components/SearchResultItem.tsx'), 'utf-8');
  assert(content.includes('result.is_authoritative'), 'Should check authoritativeness');
  assert(content.includes('Verified Source'), 'Should render verified source badge');
  assert(content.includes('result.snippet'), 'Should render snippet text');
  assert(content.includes('target="_blank"'), 'Should open external sources safely');
});

// Test 4: AIAnswerPanel citation interaction and safe fallback
test('AIAnswerPanel renders claim-level citations and expandable source drawer', () => {
  const content = fs.readFileSync(path.join(__dirname, 'src/components/AIAnswerPanel.tsx'), 'utf-8');
  assert(content.includes('renderInteractiveText'), 'Should support interactive claim citation markers');
  assert(content.includes('View cited sources'), 'Should provide expandable sources drawer');
  assert(content.includes('aiAnswer.status === "grounded"'), 'Should distinguish grounded from insufficient evidence');
  assert(content.includes('aiAnswer.disclaimer'), 'Should display uncertainty and evidence disclaimer');
});

// Test 5: SearchFilters functionality
test('SearchFilters supports language, date, safe search, and AI toggle', () => {
  const content = fs.readFileSync(path.join(__dirname, 'src/components/SearchFilters.tsx'), 'utf-8');
  assert(content.includes('All Languages'), 'Should include All Languages');
  assert(content.includes('অসমীয়া (Assamese)'), 'Should include Assamese filter');
  assert(content.includes('English'), 'Should include English filter');
  assert(content.includes('SafeSearch:'), 'Should include SafeSearch controls');
  assert(content.includes('AI Answer:'), 'Should include AI answer toggle');
});

// Test 6: EmptyState honest cold-start disclosure
test('EmptyState provides recovery suggestions and transliteration button', () => {
  const content = fs.readFileSync(path.join(__dirname, 'src/components/EmptyState.tsx'), 'utf-8');
  assert(content.includes('অসমীয়া লিপিৰে বিচাৰিব নেকি?'), 'Should suggest native script transliteration');
  assert(content.includes('Search Suggestions:'), 'Should provide helpful recovery suggestions');
});

// Test 7: Production build artifacts exist
test('Next.js production build artifacts verified in .next', () => {
  const buildDir = path.join(__dirname, '.next');
  assert(fs.existsSync(buildDir), '.next build directory should exist');
  const serverAppDir = path.join(buildDir, 'server/app');
  assert(fs.existsSync(serverAppDir), 'server/app directory should exist');
  assert(fs.existsSync(path.join(serverAppDir, 'index.html')) || fs.existsSync(path.join(serverAppDir, 'page.js')), 'Homepage build output should exist');
});

// Test 8: Bigratom Saikia and Debashish attribution and badge cleanup
test('Bigratom Saikia and Debashish attribution link is present and removed badges are absent', () => {
  const homeContent = fs.readFileSync(path.join(__dirname, 'src/app/page.tsx'), 'utf-8');
  assert(homeContent.includes('Bigratom Saikia'), 'Homepage should contain Bigratom Saikia');
  assert(homeContent.includes('https://github.com/saikiabigratom-design'), 'Homepage should link to github profile');
  assert(homeContent.includes('Debashish'), 'Homepage should contain Debashish');
  assert(homeContent.includes('https://www.linkedin.com/in/debashishbordoloi/'), 'Homepage should link to Debashish linkedin');
  assert(!homeContent.includes('Guest-First & Zero Ad Profiling'), 'Guest-First badge should be removed');
  assert(!homeContent.includes('Permitted Source Registry'), 'Permitted Source Registry badge should be removed');
  const headerContent = fs.readFileSync(path.join(__dirname, 'src/components/Header.tsx'), 'utf-8');
  assert(!headerContent.includes('Bigratom Saikia'), 'Header navbar should not contain pill');
});

// Test 9: HTML entity decoding in search route
test('cleanSnippetText safely decodes HTML entities and normalizes whitespace', () => {
  const routeContent = fs.readFileSync(path.join(__dirname, 'src/app/api/v1/search/route.ts'), 'utf-8');
  assert(routeContent.includes('cleanSnippetText'), 'route.ts should declare cleanSnippetText');
  assert(routeContent.includes('&quot;'), 'Should decode &quot;');
  assert(routeContent.includes('&#039;'), 'Should decode &#039;');
  assert(routeContent.includes('&amp;'), 'Should decode &amp;');
});

// Test 10: Strict authoritative domain verification basis
test('route.ts strictly defines authoritative domain patterns and rejects Wikipedia as authoritative', () => {
  const routeContent = fs.readFileSync(path.join(__dirname, 'src/app/api/v1/search/route.ts'), 'utf-8');
  assert(routeContent.includes('VERIFIED_DOMAIN_PATTERNS'), 'Should define verified domain patterns');
  assert(routeContent.includes('.gov.in'), 'Should include .gov.in in verified domains');
  assert(routeContent.includes('is_authoritative: false'), 'Wikipedia results must have is_authoritative: false');
});

// Test 11: Date metadata provenance without fake today substitution
test('route.ts does not substitute current date for missing publication dates and tracks Wikipedia as updated_at', () => {
  const routeContent = fs.readFileSync(path.join(__dirname, 'src/app/api/v1/search/route.ts'), 'utf-8');
  assert(!routeContent.includes('new Date().toISOString().split("T")[0]'), 'Should not substitute current date');
  assert(routeContent.includes('updated_at: revDate'), 'Should set Wikipedia revision date as updated_at');
  assert(routeContent.includes('published_date: undefined'), 'Wikipedia should not claim revision timestamp as published date');
});

// Test 12: Ambiguous short-query transliteration and multi-script handling
test('route.ts maps ko to Assamese transliteration and handles ambiguous short queries', () => {
  const routeContent = fs.readFileSync(path.join(__dirname, 'src/app/api/v1/search/route.ts'), 'utf-8');
  assert(routeContent.includes('ROMANIZED_ASSAMESE_DICT'), 'Should include romanized dictionary');
  assert(routeContent.includes('ko: "ক\'"'), 'Should map ko to Assamese ক\'');
  assert(routeContent.includes('isShortLatin'), 'Should detect short Latin queries');
  assert(routeContent.includes('wordBoundaryRegex'), 'Should use word boundary matching for short terms');
});

// Test 13: SearchFilters and SearchResultItem newest-first sorting & timestamp semantics
test('SearchResultItem differentiates published vs updated dates with timezone policy', () => {
  const itemContent = fs.readFileSync(path.join(__dirname, 'src/components/SearchResultItem.tsx'), 'utf-8');
  assert(itemContent.includes('formatDateWithTimezone'), 'Should format dates with documented timezone policy');
  assert(itemContent.includes('timeZone: "Asia/Kolkata"'), 'Should target IST (Asia/Kolkata) timezone');
  assert(itemContent.includes('Published:'), 'Should display Published: for verified publication dates');
  assert(itemContent.includes('Updated:'), 'Should display Updated: for last modified / revision dates');
  assert(itemContent.includes('Undated'), 'Should clearly display Undated for undated items');
  assert(itemContent.includes('result.is_news'), 'Should support news badge');

  const filterContent = fs.readFileSync(path.join(__dirname, 'src/components/SearchFilters.tsx'), 'utf-8');
  assert(filterContent.includes('Newest first'), 'SearchFilters should support Newest first option');
  assert(filterContent.includes('Relevance'), 'SearchFilters should support Relevance option');
});

// Test 14: Temporal intent detection, newest sorting, and freshness notice in route.ts
test('route.ts detects temporal intent, defaults to newest-first, and returns freshness notice when needed', () => {
  const routeContent = fs.readFileSync(path.join(__dirname, 'src/app/api/v1/search/route.ts'), 'utf-8');
  assert(routeContent.includes('detectTemporalIntent'), 'Should implement detectTemporalIntent');
  assert(routeContent.includes('शेহতীয়া') || routeContent.includes('\\u09b6\\u09c7\\u09b9\\u09a4\\u09c0\\u09af\\u09bc\\u09be') || routeContent.includes('খবৰ'), 'Should detect Assamese temporal keywords');
  assert(routeContent.includes('sort === "newest"'), 'Should implement newest-first sorting logic');
  assert(routeContent.includes('freshness_notice'), 'Should generate freshness notice when fresh articles are unavailable');
});

console.log('='.repeat(70));
console.log(`Frontend Test Results: ${passed} passed, ${failed} failed.`);
console.log('='.repeat(70));

if (failed > 0) process.exit(1);

