# Marketplace Connector Plugin

Plugin để kết nối và đồng bộ dữ liệu với các sàn thương mại điện tử (marketplace) sử dụng Factory Pattern.

## 🎯 Tính năng

- ✅ Kết nối với nhiều sàn thương mại điện tử
- ✅ Đồng bộ sản phẩm 2 chiều (lên sàn và về CRM)
- ✅ Đồng bộ đơn hàng từ sàn về CRM
- ✅ Cập nhật tồn kho real-time
- ✅ Cập nhật trạng thái đơn hàng
- ✅ Hỗ trợ mở rộng dễ dàng với Factory Pattern
- ✅ Tự động retry khi API call fails
- ✅ Token caching và refresh tự động
- ✅ Rate limiting handling

## 🏪 Các sàn được hỗ trợ

1. **Shopee** ✅ (Đã implement đầy đủ)
2. **Lazada** 🚧 (Template sẵn sàng)
3. **Tiki** 🚧 (Template sẵn sàng)
4. **TikTok Shop** 🚧 (Template sẵn sàng)
5. **Sendo** 🚧 (Template sẵn sàng)

## 🏗️ Kiến trúc

### Factory Pattern Structure

```
Webkul\Marketplace\
├── Contracts/
│   └── MarketplaceConnectorInterface.php    # Interface chung cho tất cả connector
├── DTOs/
│   ├── ConnectionConfig.php                 # DTO cho config kết nối
│   ├── ProductData.php                      # DTO cho sản phẩm
│   └── OrderData.php                        # DTO cho đơn hàng
├── Connectors/
│   ├── AbstractMarketplaceConnector.php     # Base class với logic chung
│   ├── ShopeeConnector.php                  # Shopee connector
│   ├── LazadaConnector.php                  # Lazada connector
│   ├── TikiConnector.php                    # Tiki connector
│   ├── TikTokShopConnector.php              # TikTok Shop connector
│   └── SendoConnector.php                   # Sendo connector
├── Factories/
│   └── MarketplaceConnectorFactory.php      # Factory để tạo connector instances
├── Services/
│   └── MarketplaceService.php               # Service layer để sử dụng
└── Exceptions/
    ├── MarketplaceException.php
    └── MarketplaceConnectionException.php
```

## 📖 Cách sử dụng

### 1. Kết nối với marketplace

```php
use Dcnet\Marketplace\DTOs\ConnectionConfig;
use Dcnet\Marketplace\Services\MarketplaceService;

$service = new MarketplaceService();

// Tạo config
$config = new ConnectionConfig(
    apiKey: 'your-api-key',
    apiSecret: 'your-api-secret',
    shopId: '12345678',
    partnerId: '87654321',
    accessToken: 'your-access-token',
    refreshToken: 'your-refresh-token',
    isSandbox: true,
);

// Kết nối
$service->connect('shopee', $config);
```

### 2. Đồng bộ sản phẩm lên marketplace

```php
use Dcnet\Marketplace\DTOs\ProductData;

$product = new ProductData(
    name: 'Áo thun nam cotton',
    description: 'Áo thun nam chất liệu cotton cao cấp',
    price: 199000,
    sku: 'ATN-001',
    stock: 100,
    images: ['https://example.com/image1.jpg'],
    category: '12345',
);

$service->syncProductToMarketplace('shopee', $product);
```

### 3. Lấy danh sách sản phẩm từ marketplace

```php
$products = $service->syncProductsFromMarketplace('shopee', [
    'offset' => 0,
    'page_size' => 20,
    'status' => 'NORMAL',
]);

foreach ($products as $product) {
    echo $product->name . "\n";
}
```

### 4. Lấy danh sách đơn hàng

```php
$orders = $service->syncOrdersFromMarketplace('shopee', [
    'time_from' => strtotime('-7 days'),
    'time_to' => time(),
    'order_status' => 'READY_TO_SHIP',
]);
```

### 5. Cập nhật tồn kho

```php
$service->updateInventory(
    marketplace: 'shopee',
    productId: '123456789',
    quantity: 50
);
```

### 6. Cập nhật trạng thái đơn hàng

```php
$service->updateOrderStatus(
    marketplace: 'shopee',
    orderId: '210123456789',
    status: 'SHIPPED'
);
```

## 🔧 Mở rộng với sàn mới

### Cách 1: Tạo connector mới (Được khuyến nghị)

```php
use Dcnet\Marketplace\Connectors\AbstractMarketplaceConnector;

class MyNewMarketplaceConnector extends AbstractMarketplaceConnector
{
    public function getName(): string
    {
        return 'mynewmarketplace';
    }

    protected function getBaseUrl(): string
    {
        return 'https://api.mynewmarketplace.com';
    }

    protected function getApiVersion(): string
    {
        return 'v1';
    }

    protected function authenticate(): void
    {
        // Implement authentication logic
    }

    // Implement other required methods...
}
```

### Cách 2: Đăng ký connector từ bên ngoài

```php
use Dcnet\Marketplace\Factories\MarketplaceConnectorFactory;

MarketplaceConnectorFactory::register(
    'mynewmarketplace',
    MyNewMarketplaceConnector::class
);

// Sử dụng
$service->connect('mynewmarketplace', $config);
```

## 🎨 Design Patterns sử dụng

1. **Factory Method Pattern**: `MarketplaceConnectorFactory` để tạo connector instances
2. **Strategy Pattern**: Mỗi connector là một strategy riêng
3. **DTO Pattern**: Data Transfer Objects cho type-safe data
4. **Template Method Pattern**: `AbstractMarketplaceConnector` định nghĩa skeleton algorithm

## 🔑 Lợi ích của kiến trúc này

- ✅ **Dễ mở rộng**: Thêm sàn mới chỉ cần tạo class mới implement interface
- ✅ **Tái sử dụng code**: Logic chung được đặt trong AbstractMarketplaceConnector
- ✅ **Type-safe**: Sử dụng DTOs với typed properties
- ✅ **Loosely coupled**: Các component độc lập, dễ test
- ✅ **SOLID principles**: Tuân thủ các nguyên tắc thiết kế OOP
- ✅ **Maintainable**: Code rõ ràng, dễ maintain

## 📝 TODO

- [ ] Hoàn thiện implementation cho Lazada connector
- [ ] Hoàn thiện implementation cho Tiki connector  
- [ ] Hoàn thiện implementation cho TikTok Shop connector
- [ ] Hoàn thiện implementation cho Sendo connector
- [ ] Thêm webhook handlers cho các sàn
- [ ] Tạo Filament resources để quản lý connections
- [ ] Tạo các migrations cho database tables
- [ ] Viết unit tests
- [ ] Tạo documentation chi tiết cho từng sàn

## 🧪 Testing

```php
// Run ví dụ
use Dcnet\Marketplace\Examples\UsageExample;

$example = new UsageExample();
$example->runAll();
```

## 📚 Tài liệu API các sàn

- [Shopee Open API](https://open.shopee.com/documents)
- [Lazada Open Platform](https://open.lazada.com/doc)
- [Tiki Open API](https://open.tiki.vn/docs)
- [TikTok Shop API](https://partner.tiktokshop.com/doc)
- [Sendo Open API](https://openapi.sendo.vn/docs)

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết
