<script>
	import Blob from "./components/blob.svelte";
	import SwiperCore, { A11y } from "swiper";
	import { Swiper, SwiperSlide } from "swiper/svelte";
	import "swiper/swiper-bundle.css";

	SwiperCore.use([A11y]);
</script>

<main>
	<h1>Mysteriet på <br /> Harefjell Vinterresort</h1>
	<Swiper
		style="padding: 2rem 0; margin-bottom: -4rem"
		centeredSlides={true}
		slidesPerView={1.3}
		spaceBetween={20}
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
		}}
	>
		<SwiperSlide>
			<div class="slide-element">
				<img
					src="/img/mysteriet_på_harefjell.png"
					alt="Påske Haren sitter forskrekket foran skjermer som har gått i blått. Fem dyr står i sirkel bak Påske Haren: en mus, en pingvin, vaskebjørn, rev og ulv."
				/>
			</div>
		</SwiperSlide>
	</Swiper>
	<Blob>
		<h2>Påskenøtter</h2>
		<p>
			Hva skjer på Harefjell? Er det ugler i elgen? Eller kanskje de har
			kamuflert seg med moose? Følg med fra torsdag 1. April klokken 10:00,
			kanskje du kan løse mysteriet!
		</p>
	</Blob>
	<h3>Påskenøtter presentert av PST</h3>
</main>

<style>
	h1 {
		display: inline-block;
		position: relative;
		left: 50%;
		color: #dbbf23;
		text-align: center;
		text-shadow: 3px 0 black, -3px 0 black, 0 3px black, 0 -3px black;
		transform: translateX(-50%) rotate(-6.5deg);
		font-size: clamp(2rem, -0.25rem + 10vw, 5rem);
		letter-spacing: 2px;
		margin-top: 3.5rem;
	}

	h2 {
		text-align: center;
		font-size: clamp(1.6rem, -0.2rem + 8vw, 4rem);
		text-shadow: 2px 0 0 black, -1px 0 black, 0 2px black, 0 -1px black;
		margin: 1.5rem 0;
		letter-spacing: 1px;
	}

	h3 {
		color: #dbbf23;
		text-align: center;
		font-size: 1.5rem;
		text-shadow: 2px 0 0 black, -1px 0 black, 0 2px black, 0 -1px black;
		margin-top: 10rem;
		letter-spacing: 1px;
	}

	p {
		max-width: 650px;
		margin: 0 auto;
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

	.slide-element > img {
		width: 100%;
		max-width: 1200px;
		height: auto;
	}
</style>
