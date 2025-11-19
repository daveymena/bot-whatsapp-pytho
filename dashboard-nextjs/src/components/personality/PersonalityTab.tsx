'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Bot, Save, Sparkles } from 'lucide-react'
import { toast } from 'sonner'

export function PersonalityTab() {
  const [personality, setPersonality] = useState({
    name: 'Asistente Virtual',
    tone: 'friendly',
    style: 'professional',
    greeting: '¡Hola! 👋 Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?',
    farewell: '¡Gracias por tu tiempo! Si necesitas algo más, aquí estaré. 😊',
    language: 'es',
    emoji_usage: 'moderate'
  })

  const handleSave = async () => {
    try {
      // Aquí iría la lógica para guardar en el backend
      toast.success('Personalidad guardada correctamente')
    } catch (error) {
      toast.error('Error al guardar la personalidad')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Personalidad del Bot</h2>
        <p className="text-gray-600 mt-1">Define cómo se comporta y comunica tu bot</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Formulario */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Configuración de Personalidad</CardTitle>
              <CardDescription>Personaliza el comportamiento del bot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Nombre del Bot</Label>
                <Input
                  id="name"
                  value={personality.name}
                  onChange={(e) => setPersonality({ ...personality, name: e.target.value })}
                  placeholder="Asistente Virtual"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="tone">Tono de Comunicación</Label>
                  <Select
                    value={personality.tone}
                    onValueChange={(value) => setPersonality({ ...personality, tone: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="friendly">Amigable</SelectItem>
                      <SelectItem value="professional">Profesional</SelectItem>
                      <SelectItem value="casual">Casual</SelectItem>
                      <SelectItem value="formal">Formal</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="style">Estilo de Respuesta</Label>
                  <Select
                    value={personality.style}
                    onValueChange={(value) => setPersonality({ ...personality, style: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="concise">Conciso</SelectItem>
                      <SelectItem value="detailed">Detallado</SelectItem>
                      <SelectItem value="professional">Profesional</SelectItem>
                      <SelectItem value="conversational">Conversacional</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="greeting">Mensaje de Bienvenida</Label>
                <Textarea
                  id="greeting"
                  value={personality.greeting}
                  onChange={(e) => setPersonality({ ...personality, greeting: e.target.value })}
                  placeholder="Mensaje inicial..."
                  rows={3}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="farewell">Mensaje de Despedida</Label>
                <Textarea
                  id="farewell"
                  value={personality.farewell}
                  onChange={(e) => setPersonality({ ...personality, farewell: e.target.value })}
                  placeholder="Mensaje de despedida..."
                  rows={3}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="language">Idioma</Label>
                  <Select
                    value={personality.language}
                    onValueChange={(value) => setPersonality({ ...personality, language: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="es">Español</SelectItem>
                      <SelectItem value="en">English</SelectItem>
                      <SelectItem value="pt">Português</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="emoji">Uso de Emojis</Label>
                  <Select
                    value={personality.emoji_usage}
                    onValueChange={(value) => setPersonality({ ...personality, emoji_usage: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">Sin emojis</SelectItem>
                      <SelectItem value="minimal">Mínimo</SelectItem>
                      <SelectItem value="moderate">Moderado</SelectItem>
                      <SelectItem value="frequent">Frecuente</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          <Button onClick={handleSave} className="w-full">
            <Save className="w-4 h-4 mr-2" />
            Guardar Personalidad
          </Button>
        </div>

        {/* Vista previa */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Vista Previa</CardTitle>
              <CardDescription>Ejemplo de conversación</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Mensaje del bot */}
                <div className="flex items-start gap-2">
                  <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-green-50 rounded-lg p-3 max-w-[80%]">
                    <p className="text-sm text-gray-900">{personality.greeting}</p>
                  </div>
                </div>

                {/* Mensaje del usuario */}
                <div className="flex items-start gap-2 justify-end">
                  <div className="bg-gray-100 rounded-lg p-3 max-w-[80%]">
                    <p className="text-sm text-gray-900">Hola, quiero información sobre productos</p>
                  </div>
                </div>

                {/* Respuesta del bot */}
                <div className="flex items-start gap-2">
                  <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-green-50 rounded-lg p-3 max-w-[80%]">
                    <p className="text-sm text-gray-900">
                      {personality.tone === 'friendly' && '¡Claro! 😊 '}
                      {personality.tone === 'professional' && 'Por supuesto. '}
                      {personality.tone === 'casual' && '¡Dale! '}
                      Tengo varios productos disponibles. ¿Qué tipo de producto te interesa?
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
            <CardContent className="pt-6">
              <div className="text-center">
                <Sparkles className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <p className="text-sm text-gray-700 mb-2 font-medium">
                  Personalidad Inteligente
                </p>
                <p className="text-xs text-gray-600">
                  El bot adapta su personalidad según el contexto y el cliente
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
