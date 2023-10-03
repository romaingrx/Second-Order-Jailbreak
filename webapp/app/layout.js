import ClientProvider from "@/components/clientProvider";
import "./globals.css";
import { Inter } from "next/font/google";


const inter = Inter({ subsets: ["latin"] });


const title = "Second-order Jailbreaks";
const description = "We examine the risk of powerful malignant intelligent actors spreading their influence over networks of agents with varying intelligence and motivations.";
export const metadata = {
  title: title,
  description: description,
  url: "https://second-order-jailbreak.romaingrx.com",
  image: "https://second-order-jailbreak.romaingrx.com/oa-image.png",
  openGraph: {
    title: title,
    description: description,
    url: 'https://second-order-jailbreak.romaingrx.com',
    siteName: 'Second-order Jailbreaks',
    images: [
      {
        url: 'https://second-order-jailbreak.romaingrx.com/oa-image.png',
        width: 800,
        height: 600,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ClientProvider>{children}</ClientProvider>
      </body>
    </html>
  );
}
