<script>
	import SwiperCore, {
		HashNavigation,
		A11y,
		Pagination,
		Keyboard,
	} from "swiper";
	import { Swiper, SwiperSlide } from "swiper/svelte";
	import "swiper/swiper-bundle.css";

	SwiperCore.use([HashNavigation, A11y, Pagination, Keyboard]);

	export let challenges = [];
	export let selectedChallenge = undefined;
</script>

<div class="wrapper">
	<Swiper
		centeredSlides={true}
		slidesPerView={1.3}
		pagination={{ clickable: true }}
		keyboard={true}
		spaceBetween={20}
		hashNavigation={{ replaceState: true }}
		on:slideChange={({ detail }) =>
			(selectedChallenge = challenges[detail[0][0].activeIndex])}
		on:swiper={({ detail }) =>
			(selectedChallenge = challenges[detail[0].activeIndex])}
		breakpoints={{
			420: {
				spaceBetween: 30,
			},
			520: {
				spaceBetween: 40,
			},
			800: {
				spaceBetween: 50,
				slidesPerView: 1.2,
			},
			1700: {
				spaceBetween: 80,
			},
		}}
		a11y={{
			containerMessage:
				"Bildekarusell med påskenøtter i tegneserieform. Det slippet ett bilde hver dag i påsken.",
			containerRoleDescriptionMessage:
				"Bildekarusell for å navigere blant påskenøttene.",
			firstSlideMessage: "Dette er det første bildet",
			lastSlideMessage: "Dette er det siste bildet",
			nextSlideMessage: "Neste bilde",
			prevSlideMessage: "Forrige bilde",
			paginationBulletMessage: "Gå til bilde {{index}}",
		}}
	>
		{#each challenges as challenge}
			<SwiperSlide data-hash={challenge.slug.current}>
				<div class="slide-element">
					<img src={challenge.image.url} alt={challenge.image.alt} />
				</div>
			</SwiperSlide>
		{/each}
	</Swiper>
</div>

<style>
	.wrapper :global(.swiper-container) {
		padding: 2rem 0;
		margin-bottom: -4rem;
	}

	.wrapper :global(.swiper-pagination-bullet) {
		opacity: 0.5;
		background-color: #ffffff;
	}

	.wrapper :global(.swiper-pagination-bullet-active) {
		opacity: 1;
	}

	.slide-element {
		background-color: white;
		color: black;
		box-shadow: 6px 6px 10px 5px rgb(0 0 0 / 25%);
		border-radius: 10px;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 1rem;
	}

	.slide-element img {
		width: 100%;
		max-width: 1200px;
		height: auto;
	}
</style>
