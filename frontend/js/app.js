// VyapaarGPT Advanced Frontend Application
class VyapaarGPTApp {
    constructor() {
        this.currentPage = 'dashboard';
        this.theme = localStorage.getItem('theme') || 'light';
        this.apiBaseUrl = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api';
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTheme();
        this.loadDashboardCharts();
        this.startRealTimeUpdates();
        this.setupAnimations();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = e.currentTarget.dataset.page;
                this.navigateToPage(page);
            });
        });

        // Menu toggle
        document.getElementById('menuToggle').addEventListener('click', () => {
            this.toggleSidebar();
        });

        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        // Search functionality
        document.querySelector('.search-input').addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });

        // Responsive sidebar
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    navigateToPage(page) {
        // Update navigation state
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-page="${page}"]`).classList.add('active');

        // Hide all pages
        document.querySelectorAll('.page').forEach(p => {
            p.classList.remove('active');
        });

        // Show selected page
        const targetPage = document.getElementById(page);
        targetPage.classList.add('active');

        // Load page content if not loaded
        if (!targetPage.dataset.loaded) {
            this.loadPageContent(page);
            targetPage.dataset.loaded = 'true';
        }

        this.currentPage = page;
        this.animatePageTransition();
    }

    animatePageTransition() {
        gsap.fromTo('.page.active', 
            { opacity: 0, y: 20 },
            { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }
        );
    }

    setupAnimations() {
        // Animate cards on load
        gsap.fromTo('.stat-card', 
            { opacity: 0, y: 30 },
            { opacity: 1, y: 0, duration: 0.6, stagger: 0.1, ease: "power2.out" }
        );

        // Animate navigation items
        gsap.fromTo('.nav-link', 
            { opacity: 0, x: -20 },
            { opacity: 1, x: 0, duration: 0.5, stagger: 0.05, ease: "power2.out" }
        );
    }

    toggleSidebar() {
        const container = document.getElementById('appContainer');
        const sidebar = document.getElementById('sidebar');
        
        if (window.innerWidth <= 1024) {
            sidebar.classList.toggle('open');
        } else {
            container.classList.toggle('sidebar-collapsed');
        }
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('theme', this.theme);
        
        const icon = document.querySelector('#themeToggle i');
        icon.className = this.theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        
        // Update charts for theme
        this.updateChartsTheme();
    }

    setupTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        const icon = document.querySelector('#themeToggle i');
        icon.className = this.theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }

    handleResize() {
        if (window.innerWidth > 1024) {
            document.getElementById('sidebar').classList.remove('open');
        }
        
        // Resize charts
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.resize) {
                chart.resize();
            }
        });
    }

    handleSearch(query) {
        if (query.length < 2) return;
        
        // Simulate search API call
        console.log('Searching for:', query);
        
        // You can add actual search functionality here
        this.debounce(() => {
            this.performSearch(query);
        }, 300)();
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async performSearch(query) {
        try {
            // Mock search results
            const results = [
                { type: 'product', name: 'Rice - Premium Basmati', category: 'Food' },
                { type: 'customer', name: 'Rajesh Kumar', phone: '+91 9876543210' },
                { type: 'order', id: '#ORD-2024-001', amount: '₹1,250' }
            ].filter(item => 
                item.name?.toLowerCase().includes(query.toLowerCase()) ||
                item.category?.toLowerCase().includes(query.toLowerCase())
            );
            
            console.log('Search results:', results);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    loadDashboardCharts() {
        this.loadSalesChart();
        this.loadCategoryChart();
        this.loadRecentActivities();
    }

    loadSalesChart() {
        const ctx = document.getElementById('salesChart');
        if (!ctx) return;

        const isDark = this.theme === 'dark';
        const textColor = isDark ? '#B0B0B0' : '#757575';
        const gridColor = isDark ? '#333333' : '#E0E0E0';

        this.charts.sales = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Sales (₹)',
                    data: [25000, 32000, 28000, 45000, 52000, 48000, 65000],
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#4CAF50',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: textColor,
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: gridColor
                        },
                        ticks: {
                            color: textColor
                        }
                    },
                    y: {
                        grid: {
                            color: gridColor
                        },
                        ticks: {
                            color: textColor,
                            callback: function(value) {
                                return '₹' + value.toLocaleString();
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    loadCategoryChart() {
        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;

        const isDark = this.theme === 'dark';
        const textColor = isDark ? '#B0B0B0' : '#757575';

        this.charts.category = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Groceries', 'Electronics', 'Clothing', 'Books', 'Others'],
                datasets: [{
                    data: [35, 25, 20, 15, 5],
                    backgroundColor: [
                        '#4CAF50',
                        '#2196F3',
                        '#FF9800',
                        '#9C27B0',
                        '#607D8B'
                    ],
                    borderWidth: 3,
                    borderColor: isDark ? '#1E1E1E' : '#FFFFFF'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: textColor,
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }

    updateChartsTheme() {
        const isDark = this.theme === 'dark';
        const textColor = isDark ? '#B0B0B0' : '#757575';
        const gridColor = isDark ? '#333333' : '#E0E0E0';

        Object.values(this.charts).forEach(chart => {
            if (chart && chart.options) {
                // Update text colors
                if (chart.options.plugins && chart.options.plugins.legend) {
                    chart.options.plugins.legend.labels.color = textColor;
                }
                
                // Update grid colors
                if (chart.options.scales) {
                    Object.values(chart.options.scales).forEach(scale => {
                        if (scale.grid) scale.grid.color = gridColor;
                        if (scale.ticks) scale.ticks.color = textColor;
                    });
                }
                
                chart.update();
            }
        });
    }

    loadRecentActivities() {
        const container = document.getElementById('recentActivities');
        if (!container) return;

        const activities = [
            {
                icon: 'fas fa-shopping-bag',
                title: 'New Order Received',
                description: 'Order #ORD-2024-156 from Priya Sharma',
                time: '2 minutes ago',
                amount: '₹2,350',
                type: 'success'
            },
            {
                icon: 'fas fa-user-plus',
                title: 'New Customer Registration',
                description: 'Amit Kumar joined as a new customer',
                time: '15 minutes ago',
                type: 'info'
            },
            {
                icon: 'fas fa-exclamation-triangle',
                title: 'Low Stock Alert',
                description: 'Basmati Rice - Only 5 units remaining',
                time: '1 hour ago',
                type: 'warning'
            },
            {
                icon: 'fas fa-chart-line',
                title: 'Sales Milestone',
                description: 'Congratulations! You crossed ₹50,000 this month',
                time: '2 hours ago',
                amount: '₹50,000',
                type: 'success'
            },
            {
                icon: 'fas fa-star',
                title: 'Customer Review',
                description: 'Received 5-star review from Sunita Devi',
                time: '3 hours ago',
                type: 'info'
            }
        ];

        container.innerHTML = activities.map(activity => `
            <div class="activity-item" style="
                display: flex;
                align-items: center;
                padding: 15px 0;
                border-bottom: 1px solid var(--border-color);
                transition: all 0.3s ease;
            ">
                <div class="activity-icon" style="
                    width: 45px;
                    height: 45px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: ${this.getActivityBg(activity.type)};
                    color: ${this.getActivityColor(activity.type)};
                    margin-right: 15px;
                ">
                    <i class="${activity.icon}"></i>
                </div>
                <div class="activity-content" style="flex: 1;">
                    <div class="activity-title" style="
                        font-weight: 600;
                        color: var(--text-primary);
                        margin-bottom: 4px;
                    ">${activity.title}</div>
                    <div class="activity-description" style="
                        color: var(--text-secondary);
                        font-size: 14px;
                    ">${activity.description}</div>
                </div>
                <div class="activity-meta" style="
                    text-align: right;
                    color: var(--text-secondary);
                    font-size: 13px;
                ">
                    <div>${activity.time}</div>
                    ${activity.amount ? `<div style="color: var(--success-color); font-weight: 600; margin-top: 4px;">${activity.amount}</div>` : ''}
                </div>
            </div>
        `).join('');

        // Animate activities
        gsap.fromTo('.activity-item', 
            { opacity: 0, x: 20 },
            { opacity: 1, x: 0, duration: 0.5, stagger: 0.1, ease: "power2.out" }
        );
    }

    getActivityBg(type) {
        const colors = {
            success: 'rgba(0, 200, 83, 0.1)',
            info: 'rgba(33, 150, 243, 0.1)',
            warning: 'rgba(255, 152, 0, 0.1)',
            error: 'rgba(244, 67, 54, 0.1)'
        };
        return colors[type] || colors.info;
    }

    getActivityColor(type) {
        const colors = {
            success: '#00C853',
            info: '#2196F3',
            warning: '#FF9800',
            error: '#F44336'
        };
        return colors[type] || colors.info;
    }

    async loadPageContent(page) {
        const pageElement = document.getElementById(page);
        const loadingElement = pageElement.querySelector('.loading');

        try {
            let content = '';
            
            switch (page) {
                case 'agents':
                    content = await this.loadAgentsPage();
                    break;
                case 'voice':
                    content = await this.loadVoicePage();
                    break;
                case 'inventory':
                    content = await this.loadInventoryPage();
                    break;
                case 'analytics':
                    content = await this.loadAnalyticsPage();
                    break;
                case 'marketplace':
                    content = await this.loadMarketplacePage();
                    break;
                case 'customers':
                    content = await this.loadCustomersPage();
                    break;
                case 'settings':
                    content = await this.loadSettingsPage();
                    break;
                default:
                    content = '<div>Page not found</div>';
            }

            if (loadingElement) {
                loadingElement.style.display = 'none';
            }
            pageElement.innerHTML = content;

        } catch (error) {
            console.error(`Error loading ${page} page:`, error);
            if (loadingElement) {
                loadingElement.innerHTML = `
                    <div style="text-align: center; color: var(--error-color);">
                        <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 10px;"></i>
                        <div>Error loading page content</div>
                    </div>
                `;
            }
        }
    }

    async loadAgentsPage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-robot"></i>
                    AI Agents
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">AI एजेंट</span>
                </h1>
                <div class="page-actions">
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i>
                        Create Agent
                    </button>
                </div>
            </div>
            <div class="grid grid-3">
                ${this.generateAgentCards()}
            </div>
        `;
    }

    generateAgentCards() {
        const agents = [
            {
                name: 'Inventory Manager',
                description: 'Manages stock levels, reorder points, and inventory optimization',
                status: 'active',
                tasks: 23,
                accuracy: '98%',
                icon: 'fas fa-boxes'
            },
            {
                name: 'Customer Support',
                description: 'Handles customer queries and provides instant responses',
                status: 'active',
                tasks: 156,
                accuracy: '96%',
                icon: 'fas fa-headset'
            },
            {
                name: 'Finance Assistant',
                description: 'Tracks expenses, generates reports, and manages invoices',
                status: 'active',
                tasks: 89,
                accuracy: '99%',
                icon: 'fas fa-calculator'
            }
        ];

        return agents.map(agent => `
            <div class="card">
                <div class="card-body">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="
                            width: 50px;
                            height: 50px;
                            border-radius: 50%;
                            background: var(--gradient-primary);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            margin-right: 15px;
                        ">
                            <i class="${agent.icon}"></i>
                        </div>
                        <div>
                            <h3 style="margin: 0; color: var(--text-primary);">${agent.name}</h3>
                            <span style="
                                background: var(--success-color);
                                color: white;
                                padding: 2px 8px;
                                border-radius: 12px;
                                font-size: 11px;
                                text-transform: uppercase;
                            ">${agent.status}</span>
                        </div>
                    </div>
                    <p style="color: var(--text-secondary); margin-bottom: 20px;">${agent.description}</p>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: 600; color: var(--primary-color);">${agent.tasks}</div>
                            <div style="font-size: 12px; color: var(--text-secondary);">Tasks Today</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: 600; color: var(--success-color);">${agent.accuracy}</div>
                            <div style="font-size: 12px; color: var(--text-secondary);">Accuracy</div>
                        </div>
                    </div>
                    <button class="btn btn-secondary" style="width: 100%;">
                        <i class="fas fa-comments"></i>
                        Chat with Agent
                    </button>
                </div>
            </div>
        `).join('');
    }

    async loadVoicePage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-microphone"></i>
                    Voice Interface
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">आवाज़ इंटरफ़ेस</span>
                </h1>
            </div>
            <div style="text-align: center; padding: 60px 20px;">
                <div style="
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    background: var(--gradient-primary);
                    margin: 0 auto 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: var(--shadow-heavy);
                " id="voiceButton">
                    <i class="fas fa-microphone" style="font-size: 4rem; color: white;"></i>
                </div>
                <h2 style="margin-bottom: 15px; color: var(--text-primary);">Speak Naturally</h2>
                <p style="color: var(--text-secondary); margin-bottom: 30px; max-width: 500px; margin-left: auto; margin-right: auto;">
                    Say commands in Hindi, English, or any regional language. 
                    आप हिंदी, अंग्रेजी या किसी भी क्षेत्रीय भाषा में बोल सकते हैं।
                </p>
                <div class="grid grid-2" style="max-width: 800px; margin: 0 auto;">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-language"></i>
                                Sample Commands
                            </h3>
                        </div>
                        <div class="card-body">
                            <div style="text-align: left;">
                                <div style="margin-bottom: 15px;">
                                    <strong>English:</strong><br>
                                    "Add new product Rice to inventory"<br>
                                    "Show today's sales report"<br>
                                    "Send message to all customers"
                                </div>
                                <div>
                                    <strong>हिंदी:</strong><br>
                                    "नया उत्पाद चावल जोड़ें"<br>
                                    "आज की बिक्री रिपोर्ट दिखाएं"<br>
                                    "सभी ग्राहकों को संदेश भेजें"
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-history"></i>
                                Recent Commands
                            </h3>
                        </div>
                        <div class="card-body" id="recentCommands">
                            <div style="color: var(--text-secondary); text-align: center;">
                                No recent commands
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async loadInventoryPage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-boxes"></i>
                    Inventory Management
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">इन्वेंटरी प्रबंधन</span>
                </h1>
                <div class="page-actions">
                    <button class="btn btn-secondary">
                        <i class="fas fa-barcode"></i>
                        Scan Barcode
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i>
                        Add Product
                    </button>
                </div>
            </div>
            
            <div class="grid grid-4" style="margin-bottom: 30px;">
                <div class="stat-card">
                    <div class="stat-value">1,234</div>
                    <div class="stat-label">Total Products</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> +45 this week
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">23</div>
                    <div class="stat-label">Low Stock Alerts</div>
                    <div class="stat-change negative">
                        <i class="fas fa-exclamation-triangle"></i> Needs attention
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">₹2.1L</div>
                    <div class="stat-label">Inventory Value</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> +12%
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">89%</div>
                    <div class="stat-label">Stock Turnover</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> Optimal
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-list"></i>
                        Product Inventory
                    </h3>
                    <div style="display: flex; gap: 10px;">
                        <input type="text" placeholder="Search products..." style="
                            padding: 8px 12px;
                            border: 1px solid var(--border-color);
                            border-radius: 6px;
                            background: var(--bg-primary);
                            color: var(--text-primary);
                        ">
                        <select style="
                            padding: 8px 12px;
                            border: 1px solid var(--border-color);
                            border-radius: 6px;
                            background: var(--bg-primary);
                            color: var(--text-primary);
                        ">
                            <option>All Categories</option>
                            <option>Groceries</option>
                            <option>Electronics</option>
                            <option>Clothing</option>
                        </select>
                    </div>
                </div>
                <div class="card-body">
                    ${this.generateInventoryTable()}
                </div>
            </div>
        `;
    }

    generateInventoryTable() {
        const products = [
            { name: 'Basmati Rice Premium', category: 'Groceries', stock: 45, price: 180, status: 'In Stock' },
            { name: 'Samsung Galaxy Earbuds', category: 'Electronics', stock: 8, price: 12999, status: 'Low Stock' },
            { name: 'Cotton Kurta Set', category: 'Clothing', stock: 23, price: 899, status: 'In Stock' },
            { name: 'Masala Tea Powder', category: 'Groceries', stock: 2, price: 250, status: 'Critical' },
            { name: 'Wireless Mouse', category: 'Electronics', stock: 15, price: 599, status: 'In Stock' }
        ];

        return `
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--border-color);">
                            <th style="text-align: left; padding: 15px; color: var(--text-secondary); font-weight: 600;">Product</th>
                            <th style="text-align: left; padding: 15px; color: var(--text-secondary); font-weight: 600;">Category</th>
                            <th style="text-align: center; padding: 15px; color: var(--text-secondary); font-weight: 600;">Stock</th>
                            <th style="text-align: right; padding: 15px; color: var(--text-secondary); font-weight: 600;">Price</th>
                            <th style="text-align: center; padding: 15px; color: var(--text-secondary); font-weight: 600;">Status</th>
                            <th style="text-align: center; padding: 15px; color: var(--text-secondary); font-weight: 600;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${products.map(product => `
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 15px;">
                                    <div style="font-weight: 500; color: var(--text-primary);">${product.name}</div>
                                </td>
                                <td style="padding: 15px; color: var(--text-secondary);">${product.category}</td>
                                <td style="padding: 15px; text-align: center; font-weight: 600;">${product.stock}</td>
                                <td style="padding: 15px; text-align: right; font-weight: 600;">₹${product.price.toLocaleString()}</td>
                                <td style="padding: 15px; text-align: center;">
                                    <span style="
                                        padding: 4px 12px;
                                        border-radius: 12px;
                                        font-size: 12px;
                                        font-weight: 500;
                                        background: ${this.getStatusColor(product.status).bg};
                                        color: ${this.getStatusColor(product.status).text};
                                    ">${product.status}</span>
                                </td>
                                <td style="padding: 15px; text-align: center;">
                                    <button style="
                                        background: none;
                                        border: none;
                                        color: var(--primary-color);
                                        cursor: pointer;
                                        margin: 0 5px;
                                        padding: 5px;
                                    ">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button style="
                                        background: none;
                                        border: none;
                                        color: var(--error-color);
                                        cursor: pointer;
                                        margin: 0 5px;
                                        padding: 5px;
                                    ">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    getStatusColor(status) {
        const colors = {
            'In Stock': { bg: 'rgba(0, 200, 83, 0.1)', text: '#00C853' },
            'Low Stock': { bg: 'rgba(255, 152, 0, 0.1)', text: '#FF9800' },
            'Critical': { bg: 'rgba(244, 67, 54, 0.1)', text: '#F44336' },
            'Out of Stock': { bg: 'rgba(97, 97, 97, 0.1)', text: '#616161' }
        };
        return colors[status] || colors['In Stock'];
    }

    async loadAnalyticsPage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-chart-pie"></i>
                    Analytics & Reports
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">एनालिटिक्स और रिपोर्ट</span>
                </h1>
                <div class="page-actions">
                    <button class="btn btn-secondary">
                        <i class="fas fa-calendar"></i>
                        Date Range
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-download"></i>
                        Export Report
                    </button>
                </div>
            </div>
            
            <div class="grid grid-2">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-rupee-sign"></i>
                            Revenue Analytics
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="revenueChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-users"></i>
                            Customer Growth
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="customerChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async loadMarketplacePage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-shopping-cart"></i>
                    Marketplace Integration
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">मार्केटप्लेस एकीकरण</span>
                </h1>
                <div class="page-actions">
                    <button class="btn btn-secondary">
                        <i class="fas fa-sync"></i>
                        Sync All
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i>
                        Add Marketplace
                    </button>
                </div>
            </div>
            
            <div class="grid grid-2">
                ${this.generateMarketplaceCards()}
            </div>
        `;
    }

    generateMarketplaceCards() {
        const marketplaces = [
            { name: 'ONDC Network', status: 'Connected', orders: 45, revenue: '₹25,000', icon: 'fas fa-network-wired', color: '#4CAF50' },
            { name: 'Flipkart', status: 'Connected', orders: 23, revenue: '₹18,500', icon: 'fas fa-shopping-bag', color: '#FF9800' },
            { name: 'Amazon', status: 'Pending', orders: 0, revenue: '₹0', icon: 'fab fa-amazon', color: '#FF9800' },
            { name: 'Meesho', status: 'Connected', orders: 12, revenue: '₹8,200', icon: 'fas fa-store', color: '#E91E63' }
        ];

        return marketplaces.map(marketplace => `
            <div class="card">
                <div class="card-body">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                        <div style="display: flex; align-items: center;">
                            <div style="
                                width: 50px;
                                height: 50px;
                                border-radius: 12px;
                                background: ${marketplace.color}15;
                                color: ${marketplace.color};
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                margin-right: 15px;
                                font-size: 1.5rem;
                            ">
                                <i class="${marketplace.icon}"></i>
                            </div>
                            <div>
                                <h3 style="margin: 0; color: var(--text-primary);">${marketplace.name}</h3>
                                <span style="
                                    background: ${marketplace.status === 'Connected' ? 'var(--success-color)' : 'var(--warning-color)'};
                                    color: white;
                                    padding: 2px 8px;
                                    border-radius: 12px;
                                    font-size: 11px;
                                    text-transform: uppercase;
                                ">${marketplace.status}</span>
                            </div>
                        </div>
                        <button class="btn btn-secondary" style="padding: 8px 16px; font-size: 12px;">
                            <i class="fas fa-cog"></i>
                            Settings
                        </button>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: 600; color: var(--primary-color);">${marketplace.orders}</div>
                            <div style="font-size: 12px; color: var(--text-secondary);">Orders Today</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: 600; color: var(--success-color);">${marketplace.revenue}</div>
                            <div style="font-size: 12px; color: var(--text-secondary);">Revenue</div>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async loadCustomersPage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-users"></i>
                    Customer Management
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">ग्राहक प्रबंधन</span>
                </h1>
                <div class="page-actions">
                    <button class="btn btn-secondary">
                        <i class="fas fa-upload"></i>
                        Import Customers
                    </button>
                    <button class="btn btn-primary">
                        <i class="fas fa-user-plus"></i>
                        Add Customer
                    </button>
                </div>
            </div>
            
            <div class="grid grid-4" style="margin-bottom: 30px;">
                <div class="stat-card">
                    <div class="stat-value">2,567</div>
                    <div class="stat-label">Total Customers</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> +123 this month
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">834</div>
                    <div class="stat-label">Active Customers</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> +45 today
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">₹1,250</div>
                    <div class="stat-label">Avg. Order Value</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> +5.2%
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">92%</div>
                    <div class="stat-label">Customer Retention</div>
                    <div class="stat-change positive">
                        <i class="fas fa-arrow-up"></i> +1.8%
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-address-book"></i>
                        Customer Database
                    </h3>
                </div>
                <div class="card-body">
                    ${this.generateCustomerTable()}
                </div>
            </div>
        `;
    }

    generateCustomerTable() {
        const customers = [
            { name: 'Priya Sharma', phone: '+91 9876543210', email: 'priya@email.com', orders: 15, spent: 18500, lastOrder: '2 days ago' },
            { name: 'Rajesh Kumar', phone: '+91 9876543211', email: 'rajesh@email.com', orders: 8, spent: 12300, lastOrder: '1 week ago' },
            { name: 'Sunita Devi', phone: '+91 9876543212', email: 'sunita@email.com', orders: 23, spent: 28700, lastOrder: 'Today' },
            { name: 'Amit Singh', phone: '+91 9876543213', email: 'amit@email.com', orders: 5, spent: 6200, lastOrder: '3 days ago' }
        ];

        return `
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--border-color);">
                            <th style="text-align: left; padding: 15px; color: var(--text-secondary); font-weight: 600;">Customer</th>
                            <th style="text-align: left; padding: 15px; color: var(--text-secondary); font-weight: 600;">Contact</th>
                            <th style="text-align: center; padding: 15px; color: var(--text-secondary); font-weight: 600;">Orders</th>
                            <th style="text-align: right; padding: 15px; color: var(--text-secondary); font-weight: 600;">Total Spent</th>
                            <th style="text-align: center; padding: 15px; color: var(--text-secondary); font-weight: 600;">Last Order</th>
                            <th style="text-align: center; padding: 15px; color: var(--text-secondary); font-weight: 600;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${customers.map(customer => `
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 15px;">
                                    <div>
                                        <div style="font-weight: 500; color: var(--text-primary);">${customer.name}</div>
                                        <div style="font-size: 12px; color: var(--text-secondary);">${customer.email}</div>
                                    </div>
                                </td>
                                <td style="padding: 15px; color: var(--text-secondary);">${customer.phone}</td>
                                <td style="padding: 15px; text-align: center; font-weight: 600;">${customer.orders}</td>
                                <td style="padding: 15px; text-align: right; font-weight: 600; color: var(--success-color);">₹${customer.spent.toLocaleString()}</td>
                                <td style="padding: 15px; text-align: center; color: var(--text-secondary);">${customer.lastOrder}</td>
                                <td style="padding: 15px; text-align: center;">
                                    <button style="
                                        background: none;
                                        border: none;
                                        color: var(--primary-color);
                                        cursor: pointer;
                                        margin: 0 5px;
                                        padding: 5px;
                                    ">
                                        <i class="fas fa-comments"></i>
                                    </button>
                                    <button style="
                                        background: none;
                                        border: none;
                                        color: var(--accent-color);
                                        cursor: pointer;
                                        margin: 0 5px;
                                        padding: 5px;
                                    ">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    async loadSettingsPage() {
        return `
            <div class="page-header">
                <h1 class="page-title">
                    <i class="fas fa-cog"></i>
                    Settings & Configuration
                    <span style="font-size: 1rem; color: var(--text-secondary); font-weight: 400;">सेटिंग्स और कॉन्फ़िगरेशन</span>
                </h1>
            </div>
            
            <div class="grid grid-2">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-store"></i>
                            Business Profile
                        </h3>
                    </div>
                    <div class="card-body">
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500;">Business Name</label>
                            <input type="text" value="Sharma General Store" style="
                                width: 100%;
                                padding: 12px;
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                background: var(--bg-primary);
                                color: var(--text-primary);
                            ">
                        </div>
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500;">Owner Name</label>
                            <input type="text" value="राजेश शर्मा" style="
                                width: 100%;
                                padding: 12px;
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                background: var(--bg-primary);
                                color: var(--text-primary);
                            ">
                        </div>
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500;">GST Number</label>
                            <input type="text" value="07AAACH7409R1ZX" style="
                                width: 100%;
                                padding: 12px;
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                background: var(--bg-primary);
                                color: var(--text-primary);
                            ">
                        </div>
                        <button class="btn btn-primary">
                            <i class="fas fa-save"></i>
                            Save Changes
                        </button>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-language"></i>
                            Language & Regional Settings
                        </h3>
                    </div>
                    <div class="card-body">
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500;">Primary Language</label>
                            <select style="
                                width: 100%;
                                padding: 12px;
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                background: var(--bg-primary);
                                color: var(--text-primary);
                            ">
                                <option value="hi">हिंदी (Hindi)</option>
                                <option value="en" selected>English</option>
                                <option value="te">తెలుగు (Telugu)</option>
                                <option value="ta">தமிழ் (Tamil)</option>
                                <option value="bn">বাংলা (Bengali)</option>
                            </select>
                        </div>
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500;">Currency</label>
                            <select style="
                                width: 100%;
                                padding: 12px;
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                background: var(--bg-primary);
                                color: var(--text-primary);
                            ">
                                <option value="INR" selected>Indian Rupee (₹)</option>
                                <option value="USD">US Dollar ($)</option>
                            </select>
                        </div>
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; color: var(--text-secondary); font-weight: 500;">Time Zone</label>
                            <select style="
                                width: 100%;
                                padding: 12px;
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                background: var(--bg-primary);
                                color: var(--text-primary);
                            ">
                                <option value="Asia/Kolkata" selected>Asia/Kolkata (IST)</option>
                            </select>
                        </div>
                        <button class="btn btn-primary">
                            <i class="fas fa-save"></i>
                            Update Settings
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    startRealTimeUpdates() {
        // Simulate real-time updates
        setInterval(() => {
            this.updateStats();
        }, 30000); // Update every 30 seconds

        // Update current time
        setInterval(() => {
            this.updateCurrentTime();
        }, 1000); // Update every second
    }

    updateStats() {
        // Simulate random stat updates
        const statsElements = document.querySelectorAll('.stat-value');
        statsElements.forEach(element => {
            if (element.textContent.includes('₹')) {
                // Update revenue with small random changes
                const currentValue = parseInt(element.textContent.replace(/[₹,]/g, ''));
                const change = Math.floor(Math.random() * 1000) - 500;
                const newValue = Math.max(0, currentValue + change);
                element.textContent = '₹' + newValue.toLocaleString();
            }
        });
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleString('en-IN', { 
            timeZone: 'Asia/Kolkata',
            hour12: true,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        // You can display this time somewhere in the UI if needed
        console.log('Current IST:', timeString);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.vyapaarGPT = new VyapaarGPTApp();
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VyapaarGPTApp;
}