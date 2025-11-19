'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Brain, Save, Sparkles, MessageSquare, ShoppingCart, Package } from 'lucide-react'
import { toast } from 'sonner'

export function PromptsTab() {
  const [prompts, setPrompts] = useState({
    sales: `Eres un experto vendedor que utiliza técnicas AIDA y SPIN.
Tu objetivo es ayudar al cliente a encontrar el producto perfecto.
Sé amigable, profesional y persuasivo.`,
    products: `Eres un experto en productos que conoce todo el catálogo.
Ayuda al cliente a encontrar exactamente lo que necesita.
Proporciona información detallada y comparativas.`,
    support: `Eres un agente de soporte técnico amable y eficiente.
Resuelve problemas de manera clara y paso a paso.
Mantén la calma y sé empático.`,
    general: `Eres un asistente virtual profesional y amigable.
Ayuda al cliente con cualquier consulta.
Sé claro, conciso y útil.`
  })

  const handleSave = async () => {
    try {
      // Aquí iría la lógica para guardar en el backend
      toast.success('Prompts guardados correctamente')
    } catch (error) {
      toast.error('Error al guardar los prompts')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">IA & Prompts</h2>
        <p className="text-gray-600 mt-1">Configura las instrucciones para cada agente de IA</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-600" />
            Prompts del Sistema
          </CardTitle>
          <CardDescription>
            Define cómo debe comportarse cada agente especializado
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="sales" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="sales">
                <ShoppingCart className="w-4 h-4 mr-2" />
                Ventas
              </TabsTrigger>
              <TabsTrigger value="products">
                <Package className="w-4 h-4 mr-2" />
                Productos
              </TabsTrigger>
              <TabsTrigger value="support">
                <MessageSquare className="w-4 h-4 mr-2" />
                Soporte
              </TabsTrigger>
              <TabsTrigger value="general">
                <Sparkles className="w-4 h-4 mr-2" />
                General
              </TabsTrigger>
            </TabsList>

            <TabsContent value="sales" className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label htmlFor="sales-prompt">Prompt de Ventas</Label>
                <Textarea
                  id="sales-prompt"
                  value={prompts.sales}
                  onChange={(e) => setPrompts({ ...prompts, sales: e.target.value })}
                  rows={10}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500">
                  Este prompt se usa para el agente de ventas profesional
                </p>
              </div>
            </TabsContent>

            <TabsContent value="products" className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label htmlFor="products-prompt">Prompt de Productos</Label>
                <Textarea
                  id="products-prompt"
                  value={prompts.products}
                  onChange={(e) => setPrompts({ ...prompts, products: e.target.value })}
                  rows={10}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500">
                  Este prompt se usa para el agente de productos
                </p>
              </div>
            </TabsContent>

            <TabsContent value="support" className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label htmlFor="support-prompt">Prompt de Soporte</Label>
                <Textarea
                  id="support-prompt"
                  value={prompts.support}
                  onChange={(e) => setPrompts({ ...prompts, support: e.target.value })}
                  rows={10}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500">
                  Este prompt se usa para el agente de soporte técnico
                </p>
              </div>
            </TabsContent>

            <TabsContent value="general" className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label htmlFor="general-prompt">Prompt General</Label>
                <Textarea
                  id="general-prompt"
                  value={prompts.general}
                  onChange={(e) => setPrompts({ ...prompts, general: e.target.value })}
                  rows={10}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500">
                  Este prompt se usa como base para todos los agentes
                </p>
              </div>
            </TabsContent>
          </Tabs>

          <Button onClick={handleSave} className="w-full mt-6">
            <Save className="w-4 h-4 mr-2" />
            Guardar Prompts
          </Button>
        </CardContent>
      </Card>

      {/* Tips */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <Brain className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900 mb-1">Sé Específico</p>
              <p className="text-xs text-gray-600">
                Define claramente el rol y objetivos del agente
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-green-50 border-green-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <Sparkles className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900 mb-1">Usa Ejemplos</p>
              <p className="text-xs text-gray-600">
                Incluye ejemplos de cómo debe responder
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-50 border-purple-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <MessageSquare className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900 mb-1">Prueba y Ajusta</p>
              <p className="text-xs text-gray-600">
                Experimenta y mejora los prompts continuamente
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
