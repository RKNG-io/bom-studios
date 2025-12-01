import { Hero } from "@/components/sections/hero";
import { WhyBom } from "@/components/sections/why-bom";
import { HowItWorks } from "@/components/sections/how-it-works";
import { Packages } from "@/components/sections/packages";
import { Examples } from "@/components/sections/examples";
import { About } from "@/components/sections/about";
import { FinalCta } from "@/components/sections/final-cta";

export default function HomePage() {
  return (
    <>
      <Hero />
      <WhyBom />
      <HowItWorks />
      <Packages />
      <Examples />
      <About />
      <FinalCta />
    </>
  );
}
