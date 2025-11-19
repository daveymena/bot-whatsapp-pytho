'use client'

import { ShoppingCart, Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

interface ShopHeaderProps {
  cartCount: number
}

export function ShopHeader({ cartCount }: ShopHeaderProps) {
  return (
    <header className="bg-gradient-to-r from-gray-900 to-gray-800 text-white sticky top-0 z-50 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/shop" className="flex items-center gap-3">
            <div className="bg-blue-600 rounded-lg p-2">
              <span className="text-white font-bold text-xl">SSB</span>
            </div>
            <span className="font-bold text-xl hidden md:block">Smart Sales Bot</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/shop" className="hover:text-blue-400 transition-colors">
              Productos
            </Link>
            <Link href="/shop/about" className="hover:text-blue-400 transition-colors">
              Nosotros
            </Link>
            <Link href="/shop/contact" className="hover:text-blue-400 transition-colors">
              Contacto
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-4">
            {/* Currency Selector */}
            <select className="bg-gray-700 text-white px-3 py-1 rounded-md text-sm border-none outline-none">
              <option value="COP">🇨🇴 COP</option>
              <option value="USD">🇺🇸 USD</option>
              <option value="EUR">🇪🇺 EUR</option>
            </select>

            {/* Cart */}
            <Link href="/shop/cart">
              <Button variant="ghost" className="relative text-white hover:bg-gray-700">
                <ShoppingCart className="h-5 w-5" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-600 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </Button>
            </Link>

            {/* Mobile Menu */}
            <Button variant="ghost" className="md:hidden text-white">
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
