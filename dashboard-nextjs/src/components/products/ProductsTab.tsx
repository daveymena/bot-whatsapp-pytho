'use client'

import { useState, useEffect } from 'react'
import {
  Plus,
  Search,
  Edit,
  Trash2,
  Package,
  DollarSign,
  Upload,
  Download,
  X,
  Loader2
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'

interface Product {
  id: string
  name: string
  description?: string
  price: number
  currency: string
  category: string
  status: string
  stock?: number
  image_url?: string
  images: string[]
  tags: string[]
  views: number
  sales_count: number
}

const statusColors: Record<string, string> = {
  AVAILABLE: 'bg-green-100 text-green-800',
  OUT_OF_STOCK: 'bg-red-100 text-red-800',
  DISCONTINUED: 'bg-gray-100 text-gray-800'
}

const statusLabels: Record<string, string> = {
  AVAILABLE: 'Disponible',
  OUT_OF_STOCK: 'Agotado',
  DISCONTINUED: 'Descontinuado'
}

export function ProductsTab() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState<Product | null>(null)
  const [importing, setImporting] = useState(false)
  const [exporting, setExporting] = useState(false)
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    currency: 'COP',
    category: 'PHYSICAL',
    status: 'AVAILABLE',
    stock: '',
    image_url: '',
    images: '',
    tags: ''
  })

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:5000/api/products')
      if (response.ok) {
        const data = await response.json()
        setProducts(data.products || [])
      }
    } catch (error) {
      console.error('Error fetching products:', error)
      toast.error('Error al cargar productos')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const productData = {
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price),
        currency: formData.currency,
        category: formData.category,
        status: formData.status,
        stock: formData.stock ? parseInt(formData.stock) : null,
        image_url: formData.image_url,
        images: formData.images ? formData.images.split(',').map(s => s.trim()) : [],
        tags: formData.tags ? formData.tags.split(',').map(s => s.trim()) : []
      }

      const url = editingProduct 
        ? `http://localhost:5000/api/products/${editingProduct.id}` 
        : 'http://localhost:5000/api/products'
      const method = editingProduct ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productData)
      })

      if (response.ok) {
        toast.success(editingProduct ? 'Producto actualizado' : 'Producto creado')
        setIsDialogOpen(false)
        setEditingProduct(null)
        resetForm()
        fetchProducts()
      } else {
        const error = await response.json()
        toast.error(error.detail || 'Error al guardar producto')
      }
    } catch (error) {
      console.error('Error:', error)
      toast.error('Error al guardar producto')
    }
  }

  const handleEdit = (product: Product) => {
    setEditingProduct(product)
    setFormData({
      name: product.name,
      description: product.description || '',
      price: product.price.toString(),
      currency: product.currency,
      category: product.category,
      status: product.status,
      stock: product.stock?.toString() || '',
      image_url: product.image_url || '',
      images: product.images.join(', '),
      tags: product.tags.join(', ')
    })
    setIsDialogOpen(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('¿Estás seguro de eliminar este producto?')) return

    try {
      const response = await fetch(`http://localhost:5000/api/products/${id}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        toast.success('Producto eliminado')
        fetchProducts()
      } else {
        toast.error('Error al eliminar producto')
      }
    } catch (error) {
      console.error('Error:', error)
      toast.error('Error al eliminar producto')
    }
  }

  const handleImport = async (file: File) => {
    setImporting(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:5000/api/products/import', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const data = await response.json()
        toast.success(`✅ ${data.count} productos importados`)
        fetchProducts()
      } else {
        toast.error('Error al importar productos')
      }
    } catch (error) {
      toast.error('Error al importar productos')
    } finally {
      setImporting(false)
    }
  }

  const handleExport = async () => {
    setExporting(true)
    try {
      const response = await fetch('http://localhost:5000/api/products/export/json')
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `productos-${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
        toast.success('✅ Productos exportados')
      } else {
        toast.error('Error al exportar productos')
      }
    } catch (error) {
      toast.error('Error al exportar productos')
    } finally {
      setExporting(false)
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      price: '',
      currency: 'COP',
      category: 'PHYSICAL',
      status: 'AVAILABLE',
      stock: '',
      image_url: '',
      images: '',
      tags: ''
    })
  }

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = categoryFilter === 'all' || product.category === categoryFilter
    const matchesStatus = statusFilter === 'all' || product.status === statusFilter
    return matchesSearch && matchesCategory && matchesStatus
  })

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-green-600" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Productos</h2>
          <p className="text-gray-600 mt-1">Gestiona tu catálogo de productos</p>
        </div>
        
        <div className="flex gap-2">
          {/* Import */}
          <div className="relative">
            <input
              id="file-import"
              type="file"
              accept=".json"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  handleImport(e.target.files[0])
                }
              }}
              className="hidden"
              disabled={importing}
            />
            <Button
              variant="outline"
              onClick={() => document.getElementById('file-import')?.click()}
              disabled={importing}
            >
              <Upload className="w-4 h-4 mr-2" />
              {importing ? 'Importando...' : 'Importar'}
            </Button>
          </div>

          {/* Export */}
          <Button
            variant="outline"
            onClick={handleExport}
            disabled={exporting}
          >
            <Download className="w-4 h-4 mr-2" />
            {exporting ? 'Exportando...' : 'Exportar'}
          </Button>

          {/* New Product */}
          <Button
            onClick={() => {
              resetForm()
              setEditingProduct(null)
              setIsDialogOpen(true)
            }}
            className="bg-green-600 hover:bg-green-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Nuevo Producto
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="Buscar productos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Categoría" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas las categorías</SelectItem>
                <SelectItem value="PHYSICAL">Físico</SelectItem>
                <SelectItem value="DIGITAL">Digital</SelectItem>
                <SelectItem value="SERVICE">Servicio</SelectItem>
              </SelectContent>
            </Select>

            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Estado" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los estados</SelectItem>
                <SelectItem value="AVAILABLE">Disponible</SelectItem>
                <SelectItem value="OUT_OF_STOCK">Agotado</SelectItem>
                <SelectItem value="DISCONTINUED">Descontinuado</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Products Grid */}
      {filteredProducts.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No hay productos
            </h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || categoryFilter !== 'all' || statusFilter !== 'all'
                ? 'No se encontraron productos con los filtros aplicados'
                : 'Comienza agregando tu primer producto al catálogo'}
            </p>
            {!searchTerm && categoryFilter === 'all' && statusFilter === 'all' && (
              <Button onClick={() => setIsDialogOpen(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Agregar Producto
              </Button>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredProducts.map((product) => {
            const imageUrl = product.images && product.images.length > 0
              ? product.images[0]
              : product.image_url

            return (
              <Card key={product.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-4">
                  {imageUrl && (
                    <div className="w-full h-48 bg-gray-100 rounded-lg mb-3 overflow-hidden">
                      <img
                        src={imageUrl}
                        alt={product.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none'
                        }}
                      />
                    </div>
                  )}
                  
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-lg line-clamp-1">{product.name}</h3>
                    <Badge className={statusColors[product.status]}>
                      {statusLabels[product.status]}
                    </Badge>
                  </div>

                  {product.description && (
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {product.description}
                    </p>
                  )}

                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-1">
                      <DollarSign className="w-4 h-4 text-green-600" />
                      <span className="font-bold text-lg text-green-600">
                        ${product.price.toLocaleString()} {product.currency}
                      </span>
                    </div>
                    {product.stock !== null && product.stock !== undefined && (
                      <div className="flex items-center gap-1 text-sm text-gray-600">
                        <Package className="w-4 h-4" />
                        <span>{product.stock}</span>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      className="flex-1"
                      onClick={() => handleEdit(product)}
                    >
                      <Edit className="w-4 h-4 mr-1" />
                      Editar
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDelete(product.id)}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {editingProduct ? 'Editar Producto' : 'Nuevo Producto'}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label>Nombre *</Label>
              <Input
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                placeholder="Nombre del producto"
              />
            </div>

            <div>
              <Label>Descripción</Label>
              <Textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={3}
                placeholder="Descripción detallada del producto"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Precio *</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  required
                  placeholder="0.00"
                />
              </div>

              <div>
                <Label>Moneda</Label>
                <Select value={formData.currency} onValueChange={(value) => setFormData({ ...formData, currency: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="COP">COP</SelectItem>
                    <SelectItem value="USD">USD</SelectItem>
                    <SelectItem value="EUR">EUR</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Categoría</Label>
                <Select value={formData.category} onValueChange={(value) => setFormData({ ...formData, category: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="PHYSICAL">Físico</SelectItem>
                    <SelectItem value="DIGITAL">Digital</SelectItem>
                    <SelectItem value="SERVICE">Servicio</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>Estado</Label>
                <Select value={formData.status} onValueChange={(value) => setFormData({ ...formData, status: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="AVAILABLE">Disponible</SelectItem>
                    <SelectItem value="OUT_OF_STOCK">Agotado</SelectItem>
                    <SelectItem value="DISCONTINUED">Descontinuado</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <Label>Stock</Label>
              <Input
                type="number"
                value={formData.stock}
                onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                placeholder="Cantidad disponible"
              />
            </div>

            <div>
              <Label>URL de Imagen Principal</Label>
              <Input
                value={formData.image_url}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                placeholder="https://ejemplo.com/imagen.jpg"
              />
            </div>

            <div>
              <Label>URLs de Imágenes Adicionales (separadas por coma)</Label>
              <Input
                value={formData.images}
                onChange={(e) => setFormData({ ...formData, images: e.target.value })}
                placeholder="url1, url2, url3"
              />
            </div>

            <div>
              <Label>Tags (separados por coma)</Label>
              <Input
                value={formData.tags}
                onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                placeholder="nuevo, oferta, destacado"
              />
            </div>

            <div className="flex justify-end gap-2 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  setIsDialogOpen(false)
                  setEditingProduct(null)
                  resetForm()
                }}
              >
                Cancelar
              </Button>
              <Button type="submit" className="bg-green-600 hover:bg-green-700">
                {editingProduct ? 'Actualizar' : 'Crear'}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}
