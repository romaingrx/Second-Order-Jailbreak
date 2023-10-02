import ClientProvider from '@/components/clientProvider'
import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Second-order Jailbreaks',
  description: 'We examine the risk of powerful malignant intelligent actors spreading their influence over networks of agents with varying intelligence and motivations.',
  url: 'https://second-order-jailbreak.romaingrx.com',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ClientProvider>
          {children}
        </ClientProvider>
      </body>
    </html>
  )
}
