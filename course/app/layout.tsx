import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BOM Studios Course - Jeroen",
  description: "Step-by-step course to learn everything needed to operate BOM Studios from zero to fully functional video-generation business.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
