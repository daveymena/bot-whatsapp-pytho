'use client'

import { useState } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ProductGalleryProps {
  images: string[]
  productName: string
}

export function ProductGallery({ images, productName }: ProductGalleryProps) {
  const [selectedImage, setSelectedImage] = useState(0)
  
  // Filtrar imágenes válidas
  const validImages = images.filter(img => img && img.trim() !== '')
  
  if (validImages.length === 0) {
    return (
      <div className="bg-white rounded-lg p-8">
        <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
          <span className="text-gray-400 text-lg">Sin imagen</span>
        </div>
      </div>
    )
  }

  const nextImage = () => {
    setSelectedImage((prev) => (prev + 1) % validImages.length)
  }

  const prevImage = () => {
    setSelectedImage((prev) => (prev - 1 + validImages.length) % validImages.length)
  }

  return (
    <div className="bg-white rounded-lg p-4 md:p-8">
      {/* Imagen Principal */}
      <div className="relative aspect-square mb-4 bg-gray-50 rounded-lg overflow-hidden group">
        <img
          src={validImages[selectedImage]}
          alt={`${productName} - Imagen ${selectedImage + 1}`}
          className="w-full h-full object-contain"
        />
        
        {/* Navegación de Imágenes */}
        {validImages.length > 1 && (
          <>
            <Button
              variant="ghost"
              size="icon"
              className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={prevImage}
            >
              <ChevronLeft className="h-6 w-6" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={nextImage}
            >
              <ChevronRight className="h-6 w-6" />
            </Button>
          </>
        )}

        {/* Indicador de Imagen */}
        {validImages.length > 1 && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
            {selectedImage + 1} / {validImages.length}
          </div>
        )}
      </div>

      {/* Miniaturas */}
      {validImages.length > 1 && (
        <div className="grid grid-cols-4 gap-2">
          {validImages.map((image, index) => (
            <button
              key={index}
              onClick={() => setSelectedImage(index)}
              className={`aspect-square rounded-lg overflow-hidden border-2 transition-all ${
                selectedImage === index
                  ? 'border-pink-500 ring-2 ring-pink-200'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <img
                src={image}
                alt={`Miniatura ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
