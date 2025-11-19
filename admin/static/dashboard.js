// Dashboard JavaScript - Funcionalidades completas

let currentTab = 'whatsapp';
let statsInterval = null;
let whatsappStatusInterval = null;

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});

function initDashboard() {
    loadStats();
    loadWhatsAppStatus();
    loadActivity();
    
    // Auto-refresh cada 30 segundos
    statsInterval = setInterval(loadStats, 30000);
    whatsappStatusInterval = setInterval(loadWhatsAppStatus, 5000);
}

// Cargar estadísticas
async function loadStats() {
    try {
        const res = await fetch('/admin/stats');
        const data = await res.json();
        
        document.getElementById('stat-conversations').textContent = data.active_conversations;
        document.getElementById('stat-orders').textContent = data.orders_today;
        document.getElementById('stat-sales').textContent = `$${data.sales_today.toLocaleString()}`;
        document.getElementById('stat-conversion').textContent = `${data.conversion_rate}%`;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Cargar estado de WhatsApp
async function loadWhatsAppStatus() {
    try {
        const res = await fetch('/admin/whatsapp/status');
        const data = await res.json();
        
        if (data.success) {
            updateWhatsAppUI(data);
        }
    } catch (error) {
        console.error('Error loading WhatsApp status:', error);
    }
}

function updateWhatsAppUI(data) {
    const isConnected = data.status === 'CONNECTED';
    const hasQR = data.qrCode && data.status === 'QR_PENDING';
    
    // Actualizar badge de estado
    const statusBadge = document.getElementById('whatsapp-status-badge');
    if (statusBadge) {
        if (isConnected) {
            statusBadge.className = 'flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-lg font-medium';
            statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Conectado';
        } else if (hasQR) {
            statusBadge.className = 'flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg font-medium';
            statusBadge.innerHTML = '<i class="fas fa-qrcode"></i> Escanea el QR';
        } else {
            statusBadge.className = 'flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg font-medium';
            statusBadge.innerHTML = '<i class="fas fa-times-circle"></i> Desconectado';
        }
    }
    
    // Mostrar/ocultar secciones
    const qrSection = document.getElementById('qr-section');
    const connectedSection = document.getElementById('connected-section');
    const disconnectedSection = document.getElementById('disconnected-section');
    
    if (hasQR) {
        // Mostrar QR code
        if (qrSection) {
            qrSection.classList.remove('hidden');
            const qrImage = document.getElementById('qr-code-image');
            if (qrImage) {
                qrImage.src = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(data.qrCode)}`;
            }
        }
        if (connectedSection) connectedSection.classList.add('hidden');
        if (disconnectedSection) disconnectedSection.classList.add('hidden');
    } else if (isConnected) {
        // Mostrar info de conexión
        if (qrSection) qrSection.classList.add('hidden');
        if (connectedSection) connectedSection.classList.remove('hidden');
        if (disconnectedSection) disconnectedSection.classList.add('hidden');
        
        // Actualizar datos
        if (data.connection) {
            const phoneEl = document.getElementById('phone-number');
            const lastConnEl = document.getElementById('last-connection');
            
            if (phoneEl && data.connection.phoneNumber) {
                phoneEl.textContent = data.connection.phoneNumber;
            }
            if (lastConnEl && data.connection.lastConnectedAt) {
                lastConnEl.textContent = new Date(data.connection.lastConnectedAt).toLocaleString('es-ES');
            }
        }
    } else {
        // Mostrar desconectado
        if (qrSection) qrSection.classList.add('hidden');
        if (connectedSection) connectedSection.classList.add('hidden');
        if (disconnectedSection) disconnectedSection.classList.remove('hidden');
    }
}

// Desconectar WhatsApp
async function disconnectWhatsApp() {
    if (!confirm('¿Estás seguro de que quieres desconectar WhatsApp?')) return;
    
    try {
        const res = await fetch('/admin/whatsapp/disconnect', { method: 'POST' });
        const data = await res.json();
        
        if (data.success) {
            showNotification('WhatsApp desconectado correctamente', 'success');
            loadWhatsAppStatus();
        }
    } catch (error) {
        showNotification('Error al desconectar WhatsApp', 'error');
    }
}

// Reconectar WhatsApp
async function reconnectWhatsApp() {
    showNotification('Reconectando WhatsApp...', 'info');
    
    try {
        const res = await fetch('/admin/whatsapp/reconnect', { method: 'POST' });
        const data = await res.json();
        
        if (data.success) {
            showNotification('WhatsApp reconectado correctamente', 'success');
            loadWhatsAppStatus();
        }
    } catch (error) {
        showNotification('Error al reconectar WhatsApp', 'error');
    }
}

// Cargar actividad reciente
async function loadActivity() {
    try {
        const res = await fetch('/admin/conversations/recent');
        const data = await res.json();
        
        const container = document.getElementById('recent-activity');
        if (!container) return;
        
        if (data.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">No hay actividad reciente</p>';
            return;
        }
        
        container.innerHTML = data.map(conv => `
            <div class="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg mb-2 cursor-pointer" onclick="viewConversation('${conv.phone}')">
                <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-user text-green-600"></i>
                </div>
                <div class="flex-1">
                    <div class="flex items-center justify-between">
                        <p class="font-medium text-gray-900">${conv.phone}</p>
                        <span class="text-xs text-gray-500">${new Date(conv.created_at).toLocaleTimeString()}</span>
                    </div>
                    <p class="text-sm text-gray-600 mt-1">${conv.message.substring(0, 100)}...</p>
                    <div class="flex gap-2 mt-2">
                        <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">${conv.intent || 'unknown'}</span>
                        <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">${conv.sentiment || 'neutral'}</span>
                        <span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded">${conv.agent_type || 'bot'}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading activity:', error);
    }
}

// Ver conversación completa
function viewConversation(phone) {
    showNotification(`Ver conversación con ${phone}`, 'info');
    // Aquí puedes abrir un modal con la conversación completa
}

// Cambiar de tab
function changeTab(tab) {
    // Ocultar todos los tabs
    document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.add('hidden'));
    
    // Mostrar el tab seleccionado
    const tabEl = document.getElementById('tab-' + tab);
    if (tabEl) tabEl.classList.remove('hidden');
    
    // Actualizar sidebar
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    if (event && event.target) {
        event.target.closest('.sidebar-item').classList.add('active');
    }
    
    currentTab = tab;
    
    // Cargar datos específicos del tab
    if (tab === 'productos') loadProducts();
    if (tab === 'clientes') loadCustomers();
    if (tab === 'whatsapp') loadWhatsAppStatus();
}

// Cargar productos
async function loadProducts() {
    try {
        const res = await fetch('/admin/products');
        const products = await res.json();
        
        const container = document.getElementById('products-list');
        if (!container) return;
        
        container.innerHTML = products.map(p => `
            <div class="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <h3 class="font-semibold text-gray-900">${p.name}</h3>
                <p class="text-sm text-gray-600 mt-1">${p.description || ''}</p>
                <div class="flex items-center justify-between mt-3">
                    <span class="text-lg font-bold text-green-600">$${p.price.toLocaleString()}</span>
                    <span class="text-sm text-gray-500">Stock: ${p.stock}</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Cargar clientes
async function loadCustomers() {
    try {
        const res = await fetch('/admin/customers');
        const customers = await res.json();
        
        const container = document.getElementById('customers-list');
        if (!container) return;
        
        container.innerHTML = customers.map(c => `
            <div class="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                        <i class="fas fa-user text-green-600"></i>
                    </div>
                    <div class="flex-1">
                        <h3 class="font-semibold text-gray-900">${c.name || 'Sin nombre'}</h3>
                        <p class="text-sm text-gray-600">${c.phone}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm font-medium text-gray-900">$${c.total_purchases.toLocaleString()}</p>
                        <p class="text-xs text-gray-500">${c.purchase_count} compras</p>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

// Toggle sidebar
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('-translate-x-full');
}

// Mostrar notificación
function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500',
        warning: 'bg-yellow-500'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-20 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}


// ========================================
// GESTIÓN DE PRODUCTOS
// ========================================

let allProducts = [];
let currentEditingProduct = null;

// Cargar productos
async function loadProducts() {
    try {
        const res = await fetch('/admin/products');
        allProducts = await res.json();
        displayProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Error cargando productos', 'error');
    }
}

// Mostrar productos
function displayProducts(products) {
    const container = document.getElementById('products-list');
    if (!container) return;
    
    if (products.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-box-open text-6xl text-gray-300 mb-4"></i>
                <p class="text-gray-500 text-lg">No hay productos</p>
                <button onclick="showAddProductModal()" class="mt-4 px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">
                    Agregar Primer Producto
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = products.map(p => `
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
            ${p.image_url ? `
                <img src="${p.image_url}" alt="${p.name}" class="w-full h-48 object-cover">
            ` : `
                <div class="w-full h-48 bg-gray-100 flex items-center justify-center">
                    <i class="fas fa-image text-4xl text-gray-300"></i>
                </div>
            `}
            
            <div class="p-4">
                <div class="flex items-start justify-between mb-2">
                    <h3 class="font-semibold text-gray-900 text-lg">${p.name}</h3>
                    <span class="px-2 py-1 bg-${p.stock > 0 ? 'green' : 'red'}-100 text-${p.stock > 0 ? 'green' : 'red'}-700 text-xs rounded-full">
                        ${p.stock > 0 ? 'Disponible' : 'Sin stock'}
                    </span>
                </div>
                
                <p class="text-sm text-gray-600 mb-3 line-clamp-2">${p.description || 'Sin descripción'}</p>
                
                <div class="flex items-center justify-between mb-3">
                    <span class="text-2xl font-bold text-emerald-600">$${p.price.toLocaleString()}</span>
                    <span class="text-sm text-gray-500">Stock: ${p.stock}</span>
                </div>
                
                <div class="flex gap-2 mb-3">
                    <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">${p.category || 'Sin categoría'}</span>
                    ${p.is_digital ? '<span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded">Digital</span>' : ''}
                    ${p.is_dropshipping ? '<span class="px-2 py-1 bg-orange-100 text-orange-700 text-xs rounded">Dropshipping</span>' : ''}
                </div>
                
                <div class="flex gap-2">
                    <button onclick="editProduct(${p.id})" class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button onclick="deleteProduct(${p.id})" class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 text-sm">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Filtrar productos
function filterProducts() {
    const search = document.getElementById('search-products')?.value.toLowerCase() || '';
    const category = document.getElementById('filter-category')?.value || '';
    const status = document.getElementById('filter-status')?.value || '';
    
    let filtered = allProducts.filter(p => {
        const matchSearch = p.name.toLowerCase().includes(search) || 
                          (p.description && p.description.toLowerCase().includes(search));
        const matchCategory = !category || p.category === category;
        const matchStatus = !status || 
                          (status === 'available' && p.stock > 0) ||
                          (status === 'out_of_stock' && p.stock === 0);
        
        return matchSearch && matchCategory && matchStatus;
    });
    
    displayProducts(filtered);
}

// Mostrar modal agregar
function showAddProductModal() {
    currentEditingProduct = null;
    document.getElementById('modal-title').textContent = 'Nuevo Producto';
    document.getElementById('product-form').reset();
    document.getElementById('product-id').value = '';
    document.getElementById('product-modal').classList.remove('hidden');
}

// Cerrar modal
function closeProductModal() {
    document.getElementById('product-modal').classList.add('hidden');
    currentEditingProduct = null;
}

// Editar producto
async function editProduct(id) {
    const product = allProducts.find(p => p.id === id);
    if (!product) return;
    
    currentEditingProduct = product;
    document.getElementById('modal-title').textContent = 'Editar Producto';
    document.getElementById('product-id').value = product.id;
    document.getElementById('product-name').value = product.name;
    document.getElementById('product-description').value = product.description || '';
    document.getElementById('product-price').value = product.price;
    document.getElementById('product-stock').value = product.stock;
    document.getElementById('product-category').value = product.category || 'Físicos';
    document.getElementById('product-warranty').value = product.warranty || '';
    document.getElementById('product-image').value = product.image_url || '';
    document.getElementById('product-is-digital').checked = product.is_digital || false;
    document.getElementById('product-is-dropshipping').checked = product.is_dropshipping || false;
    
    document.getElementById('product-modal').classList.remove('hidden');
}

// Guardar producto
async function saveProduct(event) {
    event.preventDefault();
    
    const productData = {
        name: document.getElementById('product-name').value,
        description: document.getElementById('product-description').value,
        price: parseFloat(document.getElementById('product-price').value),
        stock: parseInt(document.getElementById('product-stock').value) || 0,
        category: document.getElementById('product-category').value,
        warranty: document.getElementById('product-warranty').value,
        image_url: document.getElementById('product-image').value,
        is_digital: document.getElementById('product-is-digital').checked,
        is_dropshipping: document.getElementById('product-is-dropshipping').checked
    };
    
    const productId = document.getElementById('product-id').value;
    
    try {
        const url = productId ? `/admin/products/${productId}` : '/admin/products';
        const method = productId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData)
        });
        
        if (res.ok) {
            showNotification(productId ? 'Producto actualizado' : 'Producto creado', 'success');
            closeProductModal();
            loadProducts();
        } else {
            showNotification('Error guardando producto', 'error');
        }
    } catch (error) {
        console.error('Error saving product:', error);
        showNotification('Error guardando producto', 'error');
    }
}

// Eliminar producto
async function deleteProduct(id) {
    if (!confirm('¿Estás seguro de eliminar este producto?')) return;
    
    try {
        const res = await fetch(`/admin/products/${id}`, { method: 'DELETE' });
        
        if (res.ok) {
            showNotification('Producto eliminado', 'success');
            loadProducts();
        } else {
            showNotification('Error eliminando producto', 'error');
        }
    } catch (error) {
        console.error('Error deleting product:', error);
        showNotification('Error eliminando producto', 'error');
    }
}

// Importar productos
function importProducts() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json,.csv';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                let products;
                if (file.name.endsWith('.json')) {
                    products = JSON.parse(event.target.result);
                } else {
                    // TODO: Implementar parser CSV
                    showNotification('Formato CSV próximamente', 'info');
                    return;
                }
                
                const res = await fetch('/admin/products/import', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ products })
                });
                
                if (res.ok) {
                    const data = await res.json();
                    showNotification(`${data.imported} productos importados`, 'success');
                    loadProducts();
                } else {
                    showNotification('Error importando productos', 'error');
                }
            } catch (error) {
                console.error('Error importing:', error);
                showNotification('Error procesando archivo', 'error');
            }
        };
        reader.readAsText(file);
    };
    input.click();
}

// Exportar productos
async function exportProducts() {
    try {
        const res = await fetch('/admin/products');
        const products = await res.json();
        
        const dataStr = JSON.stringify(products, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `productos_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        showNotification('Productos exportados', 'success');
    } catch (error) {
        console.error('Error exporting:', error);
        showNotification('Error exportando productos', 'error');
    }
}
