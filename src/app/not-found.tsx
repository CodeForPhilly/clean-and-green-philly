import { ThemeButtonLink } from "@/components/ThemeButton";
import { Header } from "@/components";

export default function NotFound() {
  return (
    <>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow flex items-center justify-center">
          <div className="text-center">
            <h2 className="heading-3xl mb-4">404</h2>
            <p className="body-md mb-4">This page cannot be found.</p>
            <ThemeButtonLink
              href={"/"}
              className="text-[#03141B] mx-auto inline-block"
              color="secondary"
              label="Return to Home"
            />
          </div>
        </main>
      </div>
    </>
  );
}
