# Miners Hub Portfolio - Technical Specification

## Project Overview

A modern, professional portfolio website for Miners Hub - a leading cryptocurrency mining solution provider operating in UAE and Oman. The site showcases 40MW of mining capacity, advanced cooling technologies, and premium brand positioning.

---

## Brand Identity

### Color Palette
- **Primary Black**: Background and base
- **Gold**: #FFD700 (classic gold) - Used for logo, accents, and CTAs
- **Deep Blue**: #003366 (navy) - Secondary accent color

### Logo
- **Style**: Gold square with "MH" text inside
- **Color**: #FFD700 (gold)
- **Text**: "Miners Hub" next to the square
- **No custom logo file** - Use current gradient square design updated to gold

### Typography
- **Font**: Inter (Next.js default)
- **No custom fonts** required

---

## Core Features

### 1. 3D Interactive Globe (Cobe)
**Status**: Needs full implementation - previous attempts failed

**Implementation Details**:
- **Position**: Right side of hero section (50/50 split with text)
- **Size**: Medium - balanced size, substantial but not overwhelming
- **Base Color**: Black globe
- **Glow Effect**: Gold glow around the globe
- **Surface**: Clean, smooth surface with NO grid/latitude lines

**Markers**:
- **Count**: Multiple markers (10+)
- **Type**: Visual dots on the globe surface
- **Distribution**: Random scatter across UAE and Oman region
- **Data**: Visual only (no real facility locations)
- **Function**: Purely aesthetic, not clickable/informative

**Interactivity**:
- **Rotation**: Manual only (user drags to rotate, NO auto-rotate)
- **Zoom**: Enabled via scroll
- **Drag**: Full drag to rotate
- **Primary Element**: Globe is the main visual in the hero section

**Colors**:
- Globe base: Black
- Markers: Gold (#FFD700) or gold/blue mix
- Atmosphere/Glow: Gold glow effect

---

### 2. Aurora Background
**Status**: Animated but untested on mobile performance

**Behavior**:
- **Animation**: Continuous
- **Performance**: Accept performance tradeoff (no optimization required)
- **Colors**: Update to brand colors (black/gold/blue)
- **Deployment**: Vercel environment

---

### 3. Hero Section
**Layout**:
- **Grid**: 50/50 split - text left, globe right
- **Size**: Globe is primary element
- **Animation**: Immediate fade-in on page load

**Content**:
- **Headline**: "Premium Crypto Mining Solutions" (keep current)
- **Subheadline**: "Access to 40MW of mining capacity..."
- **CTAs**:
  - "Start Mining Today": Decorative only (keep button styling)
  - "Book a Tour": Decorative only (keep button styling)
- **Stats**: 40MW capacity, 15K+ miners, 99.9% uptime, 24/7 support

---

### 4. Cooling Solutions with Videos
**Status**: Video files exist but need optimization

**Videos**:
- **Files**:
  - `/water-cooled.MOV` (Hydro cooling)
  - `/air-cooled.MOV` (Air cooling)
  - `/emmersion.MOV` (Immersion cooling)
- **Optimization**: Required - convert to web-friendly formats (MP4/WebM)
- **Compression**: Required - reduce file size for faster loading

**Loading Strategy**:
- **Primary**: Lazy load on tab switch (load only active video)
- **Fallback**: Image fallback if video fails to load
- **Poster Images**: Need creation (snapshots from videos)

**Content**:
- **Accuracy**: All content (features, benefits, percentages) is complete and accurate
- **Tabs**: Hydro, Air, Immersion
- **Auto-play**: Yes, looped, muted

---

### 5. ASIC Miners Section
**Display**:
- **Images**: Not a priority - keep SVG icons (no product photos)
- **Data**: Static specs only (hashrate, power)
- **Miners**:
  - Antminer S21 (Bitmain): 200 TH/s, 3550W
  - Whatsminer M53 (MicroBT): 230 TH/s, 3204W
  - KS3 (IceRiver): 9.5 TH/s, 3400W

---

### 6. Contact & CTA
**Contact Form**:
- **Action**: Remove form entirely
- **Replacement**: Link to cal.com (future implementation)

**Contact Information**:
- **Phone**: +971 58 862 2898, +971 56 266 3665
- **Email**: team@minershub.ae
- **Location**: Abu Dhabi, United Arab Emirates

**Social Media**:
- **Platforms**: Instagram, TikTok, LinkedIn, Twitter
- **Status**: Placeholders only (no actual URLs)
- **Display**: Show icons, no functional links

---

### 7. Navigation
**Desktop**:
- **Links**: About, ASIC Miners, Cooling Solutions, Contact
- **Behavior**: Scroll to sections
- **CTA**: "Get Started" button (LiquidButton)

**Mobile**:
- **Strategy**: Scrolling is fine (no mobile menu needed)
- **Behavior**: Users scroll through all sections

---

### 8. Footer
**Layout**: Keep current 4-column layout
**Links**: Display as static text (non-interactive, remove anchor tags)
- Services: ASIC Miner Sales, Hosting Services, Repair & Maintenance, Cooling Solutions
- Company: About Us, Careers, Blog, Contact

**Social**: Display placeholder icons for Instagram, TikTok, LinkedIn, Twitter

---

## Technical Requirements

### Performance & Optimization
**AuroraBackground**:
- Animation: Continuous, no optimization needed
- Performance: Accept tradeoff

**Videos**:
- Lazy loading: On tab switch
- Fallback: Image fallback
- Optimization: Required (compression, format conversion)
- Poster images: Need creation

**Analytics**: None (do not implement)

---

### Deployment
**Platform**: Vercel
**URL**: Vercel default URL (no custom domain)
**Environment**: Production-ready with Next.js 14

---

### Browser Support
**Target**: Modern browsers only
- Latest Chrome
- Latest Safari
- Latest Firefox
- Latest Edge
- No legacy browser support (no IE11)

**Technical Impact**: Cobe and modern ES6+ features may not work on older browsers - acceptable tradeoff

---

### Accessibility
**Level**: Basic support
- Keyboard navigation: Not required
- Screen reader: Not required
- Color contrast: Not required
- ARIA labels: Not required

---

### Multi-language
**Support**: English only
- No Arabic RTL support required
- No translation system required

---

### SEO Strategy
**Focus**: Local SEO targeting UAE and Oman
- Target keywords: Crypto mining, UAE, Oman, MENA region
- Meta tags: Comprehensive (not yet implemented in current code)
- Open Graph tags: Required
- Structured data: Optional (future consideration)

---

## Known Issues & Blockers

### 1. 3D Globe Implementation
**Issue**: Previous implementation attempts failed
**Status**: Needs debugging help
**Action**: Full implementation required

**Potential Issues**:
- Library import/configuration errors
- Component rendering issues
- Missing dependencies
- Canvas/WebGL initialization failures

---

## Page Structure

### Sections (in order)
1. **Navigation** - Fixed, backdrop blur
2. **Hero Section** - 50/50 split, globe on right
3. **Value Propositions** - 4 cards (Scale, Expert Management, Advanced Cooling, Sustainable)
4. **ASIC Miners** - 3 miner cards with static specs
5. **Cooling Solutions** - Tabbed video showcase
6. **CTA Section** - Gradient background, decorative buttons
7. **Contact Section** - Contact info only (no form)
8. **Footer** - 4 columns, static text links

---

## Design Guidelines

### Visual Hierarchy
- **Primary**: 3D globe (hero), gold accents
- **Secondary**: Deep blue accents, stats
- **Tertiary**: Gray text, supporting content

### Color Usage
- **Black**: Background, base
- **Gold (#FFD700)**: Logo, highlights, CTAs, globe glow
- **Deep Blue (#003366)**: Secondary accents, supporting elements
- **Gradients**: Blue to purple (current) - update to black/gold/blue

### Component Styling
- **Buttons**: MetalButton (gold), LiquidButton (blue/glass effect)
- **Cards**: Slate backgrounds with hover states
- **Borders**: Slate-700 with blue-500 hover

---

## Animation & Transitions

### Hero Section
- **Entry**: Immediate fade-in on page load
- **Globe**: Manual rotation (drag to interact)
- **Scroll-triggered**: No (only immediate)

### AuroraBackground
- **Behavior**: Continuous animation
- **Performance**: No optimization needed (accept tradeoff)

### Scroll Animations
- **Strategy**: Immediate on load (not scroll-triggered)
- **Reason**: No scroll-triggered animations required

---

## Future Enhancements (Not in Initial Scope)

1. **Contact Form Integration** - Cal.com booking system
2. **Real Globe Data** - Facility locations with informational markers
3. **Social Media Links** - Actual URLs when accounts are ready
4. **Additional Pages** - About, Careers, Blog (footer links)
5. **Analytics** - User engagement tracking (not required)
6. **Multi-language** - Arabic RTL support (not required)

---

## Dependencies

### Core
- Next.js 14 (App Router)
- React 18.3.1
- TypeScript 5
- Tailwind CSS 3.4.1

### UI Components
- @radix-ui/react-slot: ^1.2.4
- class-variance-authority: ^0.7.1
- clsx: ^2.1.1
- tailwind-merge: ^3.5.0

### 3D Graphics
- cobe: ^2.0.1 (globe visualization - **needs implementation**)

### Build Tools
- autoprefixer: ^10.4.27
- postcss: ^8

---

## File Structure

```
miners-hub-portfolio/
├── app/
│   ├── globals.css          # Tailwind + custom styles
│   ├── layout.tsx           # Root layout with metadata (needs SEO update)
│   └── page.tsx             # Main portfolio page (single-page)
├── components/
│   └── ui/
│       ├── globe.tsx           # 3D globe (MISSING - needs implementation)
│       ├── liquid-glass-button.tsx  # Metal & Liquid buttons
│       └── aurora-background.tsx    # Animated background (present)
├── lib/
│   └── utils.ts             # cn() utility
├── public/
│   ├── water-cooled.MOV     # Hydro cooling video (needs optimization)
│   ├── air-cooled.MOV       # Air cooling video (needs optimization)
│   └── emmersion.MOV       # Immersion cooling video (needs optimization)
└── tailwind.config.ts       # Update with brand colors (#FFD700, #003366)
```

---

## Development Tasks (Priority Order)

### 1. Critical Path (MVP)
1. **Implement 3D Globe** (Cobe)
   - Create `components/ui/globe.tsx`
   - Black globe with gold glow
   - Multiple random visual dots
   - Manual rotation (drag/zoom)
   - Clean surface (no grid)
   - Position in hero right side (50/50)

2. **Update Brand Colors**
   - Update `tailwind.config.ts` with #FFD700 and #003366
   - Apply gold to logo (MH square)
   - Update AuroraBackground to brand colors
   - Replace blue/purple gradients with black/gold/blue

3. **Remove Contact Form**
   - Remove form from contact section
   - Keep contact info (phone, email, location)
   - Add placeholder for future Cal.com link

4. **Update Footer Links**
   - Convert anchor tags to static text
   - Keep 4-column layout
   - Social media: placeholder icons, no links

### 2. Optimization
5. **Video Optimization**
   - Convert .MOV to MP4/WebM
   - Compress file sizes
   - Create poster images (thumbnails)
   - Implement lazy loading on tab switch
   - Add image fallback

### 3. SEO Enhancement
6. **Meta Tags** (in `app/layout.tsx`)
   - Add comprehensive meta description
   - Add Open Graph tags
   - Add Twitter Card tags
   - Target UAE/Oman crypto mining keywords

### 4. Deployment
7. **Deploy to Vercel**
   - Use default Vercel URL
   - Verify 3D globe renders
   - Test video loading on mobile
   - Confirm all animations work

---

## Acceptance Criteria

### Must Have (MVP)
- ✅ 3D globe renders in hero section
- ✅ Globe is interactive (drag/zoom)
- ✅ Black globe with gold glow
- ✅ Multiple visual dots (UAE/Oman region)
- ✅ Brand colors applied (#FFD700 gold, #003366 blue)
- ✅ Logo updated to gold square MH
- ✅ Contact form removed
- ✅ Footer links as static text
- ✅ Videos lazy load on tab switch
- ✅ Images fall back if videos fail
- ✅ Deployed to Vercel

### Should Have
- ⏳ Videos optimized (compressed, web format)
- ⏳ Poster images for videos
- ⏳ Comprehensive SEO meta tags
- ⏳ AuroraBackground uses brand colors

### Nice to Have
- 🔮 Actual facility locations on globe
- 🔮 Real product images for miners
- 🔮 Social media URLs
- 🔮 Cal.com integration
- 🔮 Additional pages (About, Careers, Blog)

---

## Notes & Assumptions

1. **Performance Tradeoffs**: AuroraBackground animation is accepted even if untested on mobile - no optimization required
2. **Browser Support**: Modern browsers only - Cobe features won't work on legacy browsers
3. **Analytics**: No user tracking or analytics implementation required
4. **Accessibility**: Basic support sufficient - no WCAG compliance required
5. **Multi-language**: English only - no Arabic support needed
6. **Content**: All cooling solutions content is accurate and complete
7. **Miner Images**: Product photos not a priority - SVG icons acceptable
8. **Deployment**: Vercel default URL (no custom domain)

---

## Contact Information

**Project Owner**: Miners Hub
**Location**: Abu Dhabi, United Arab Emirates
**Email**: team@minershub.ae
**Phone**: +971 58 862 2898, +971 56 266 3665

---

*Specification Version: 1.0*
*Last Updated: March 24, 2026*
*Status: Ready for Implementation*
