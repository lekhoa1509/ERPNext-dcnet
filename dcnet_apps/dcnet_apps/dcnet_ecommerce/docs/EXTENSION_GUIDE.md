# Hướng dẫn Mở rộng Plugin Marketplace Connector

Tài liệu này hướng dẫn chi tiết cách thêm một marketplace mới vào plugin.

## 📋 Checklist để thêm marketplace mới

- [ ] Tạo class Connector mới
- [ ] Đăng ký connector trong Factory
- [ ] Implement các phương thức required
- [ ] Tạo config cho marketplace
- [ ] Test kết nối
- [ ] Viết documentation

## 🎯 Bước 1: Tạo Connector Class

Tạo file mới trong `src/Connectors/YourMarketplaceConnector.php`:

```php
<?php

namespace Dcnet\Marketplace\Connectors;

use Dcnet\Marketplace\DTOs\ProductData;
use Dcnet\Marketplace\DTOs\OrderData;

/**
 * Your Marketplace Connector
 * Documentation: https://api.yourmarketplace.com/docs
 */
class YourMarketplaceConnector extends AbstractMarketplaceConnector
{
    private const SANDBOX_URL = 'https://sandbox-api.yourmarketplace.com';
    private const PRODUCTION_URL = 'https://api.yourmarketplace.com';
    private const API_VERSION = 'v1';

    public function getName(): string
    {
        return 'yourmarketplace';
    }

    protected function getBaseUrl(): string
    {
        return $this->config->isSandbox ? self::SANDBOX_URL : self::PRODUCTION_URL;
    }

    protected function getApiVersion(): string
    {
        return self::API_VERSION;
    }

    protected function authenticate(): void
    {
        // Implement authentication logic
        // Ví dụ: OAuth 2.0, API Key, JWT, etc.
        
        // Check cached token
        $cachedToken = $this->getCachedToken();
        if ($cachedToken) {
            $this->accessToken = $cachedToken;
            return;
        }

        // Authenticate with API
        $response = $this->makeApiRequest('POST', '/auth/token', [
            'grant_type' => 'client_credentials',
            'client_id' => $this->config->apiKey,
            'client_secret' => $this->config->apiSecret,
        ]);

        $this->accessToken = $response['access_token'];
        $ttl = $response['expires_in'] ?? 3600;
        $this->cacheToken($this->accessToken, $ttl);
    }

    public function getProducts(array $filters = []): array
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('GET', '/products', [
            'page' => $filters['page'] ?? 1,
            'limit' => $filters['limit'] ?? 50,
        ]);

        $products = [];
        foreach ($response['data'] ?? [] as $item) {
            $products[] = $this->mapToProductData($item);
        }

        return $products;
    }

    public function getProduct(string $productId): ?ProductData
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('GET', "/products/{$productId}");
        
        if (!isset($response['data'])) {
            return null;
        }

        return $this->mapToProductData($response['data']);
    }

    public function syncProduct(ProductData $product): bool
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('POST', '/products', 
            $this->mapFromProductData($product)
        );

        return isset($response['data']['id']);
    }

    public function updateProduct(string $productId, ProductData $product): bool
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('PUT', "/products/{$productId}",
            $this->mapFromProductData($product)
        );

        return isset($response['data']['id']);
    }

    public function deleteProduct(string $productId): bool
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('DELETE', "/products/{$productId}");

        return ($response['success'] ?? false) === true;
    }

    public function getOrders(array $filters = []): array
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('GET', '/orders', [
            'created_from' => $filters['created_from'] ?? null,
            'created_to' => $filters['created_to'] ?? null,
            'status' => $filters['status'] ?? null,
        ]);

        $orders = [];
        foreach ($response['data'] ?? [] as $item) {
            $orders[] = $this->mapToOrderData($item);
        }

        return $orders;
    }

    public function getOrder(string $orderId): ?OrderData
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('GET', "/orders/{$orderId}");
        
        if (!isset($response['data'])) {
            return null;
        }

        return $this->mapToOrderData($response['data']);
    }

    public function updateOrderStatus(string $orderId, string $status): bool
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('PATCH', "/orders/{$orderId}/status", [
            'status' => $status,
        ]);

        return isset($response['data']['id']);
    }

    public function syncInventory(string $productId, int $quantity): bool
    {
        $this->ensureConnected();

        $response = $this->makeApiRequest('PATCH', "/products/{$productId}/inventory", [
            'quantity' => $quantity,
        ]);

        return isset($response['data']['id']);
    }

    /**
     * Helper methods
     */
    private function ensureConnected(): void
    {
        if (!$this->isConnected()) {
            throw new \Exception('Not connected to marketplace');
        }
    }

    private function mapToProductData(array $data): ProductData
    {
        return ProductData::fromArray([
            'id' => (string) $data['id'],
            'name' => $data['name'],
            'description' => $data['description'] ?? '',
            'price' => $data['price'] ?? 0,
            'original_price' => $data['compare_at_price'] ?? null,
            'sku' => $data['sku'] ?? '',
            'stock' => $data['inventory_quantity'] ?? 0,
            'images' => $data['images'] ?? [],
            'category' => $data['category_id'] ?? null,
            'status' => $data['status'] ?? 'active',
            'metadata' => [
                'marketplace_id' => $data['id'],
            ],
        ]);
    }

    private function mapFromProductData(ProductData $product): array
    {
        return [
            'name' => $product->name,
            'description' => $product->description,
            'price' => $product->price,
            'compare_at_price' => $product->originalPrice,
            'sku' => $product->sku,
            'inventory_quantity' => $product->stock,
            'images' => $product->images,
            'category_id' => $product->category,
            'status' => $product->status,
        ];
    }

    private function mapToOrderData(array $data): OrderData
    {
        return OrderData::fromArray([
            'id' => (string) $data['id'],
            'order_number' => $data['order_number'],
            'status' => $data['status'],
            'total_amount' => $data['total_price'],
            'items' => $data['line_items'] ?? [],
            'customer' => [
                'name' => $data['customer']['name'] ?? '',
                'email' => $data['customer']['email'] ?? '',
                'phone' => $data['customer']['phone'] ?? '',
            ],
            'shippingAddress' => $data['shipping_address'] ?? [],
            'created_at' => $data['created_at'],
            'updated_at' => $data['updated_at'],
        ]);
    }
}
```

## 🎯 Bước 2: Đăng ký trong Factory

Mở file `src/Factories/MarketplaceConnectorFactory.php` và thêm vào array `$connectors`:

```php
protected static array $connectors = [
    'shopee' => \Webkul\Marketplace\Connectors\ShopeeConnector::class,
    'lazada' => \Webkul\Marketplace\Connectors\LazadaConnector::class,
    'tiki' => \Webkul\Marketplace\Connectors\TikiConnector::class,
    'tiktokshop' => \Webkul\Marketplace\Connectors\TikTokShopConnector::class,
    'sendo' => \Webkul\Marketplace\Connectors\SendoConnector::class,
    'yourmarketplace' => \Webkul\Marketplace\Connectors\YourMarketplaceConnector::class, // ← Thêm dòng này
];
```

## 🎯 Bước 3: Tạo Config File

Tạo hoặc cập nhật `config/marketplace.php`:

```php
<?php

return [
    'yourmarketplace' => [
        'api_key' => env('YOURMARKETPLACE_API_KEY'),
        'api_secret' => env('YOURMARKETPLACE_API_SECRET'),
        'shop_id' => env('YOURMARKETPLACE_SHOP_ID'),
        'access_token' => env('YOURMARKETPLACE_ACCESS_TOKEN'),
        'refresh_token' => env('YOURMARKETPLACE_REFRESH_TOKEN'),
        'is_sandbox' => env('YOURMARKETPLACE_SANDBOX', true),
    ],
];
```

## 🎯 Bước 4: Thêm vào .env

```env
YOURMARKETPLACE_API_KEY=your_api_key_here
YOURMARKETPLACE_API_SECRET=your_api_secret_here
YOURMARKETPLACE_SHOP_ID=your_shop_id
YOURMARKETPLACE_ACCESS_TOKEN=
YOURMARKETPLACE_REFRESH_TOKEN=
YOURMARKETPLACE_SANDBOX=true
```

## 🎯 Bước 5: Test Connector

### Test qua Command Line

```bash
php artisan marketplace:test yourmarketplace
```

### Test qua Code

```php
use Dcnet\Marketplace\DTOs\ConnectionConfig;
use Dcnet\Marketplace\Services\MarketplaceService;

$service = new MarketplaceService();

$config = new ConnectionConfig(
    apiKey: config('marketplace.yourmarketplace.api_key'),
    apiSecret: config('marketplace.yourmarketplace.api_secret'),
    isSandbox: true,
);

// Test connection
$connector = $service->connect('yourmarketplace', $config);

// Test get products
$products = $connector->getProducts();
dd($products);
```

## 📝 Tips & Best Practices

### 1. Error Handling

Luôn handle errors một cách graceful:

```php
public function getProducts(array $filters = []): array
{
    try {
        $this->ensureConnected();
        
        $response = $this->makeApiRequest('GET', '/products', $filters);
        
        return array_map([$this, 'mapToProductData'], $response['data'] ?? []);
        
    } catch (\Exception $e) {
        Log::error("Failed to get products from {$this->getName()}", [
            'error' => $e->getMessage(),
            'filters' => $filters,
        ]);
        
        throw $e;
    }
}
```

### 2. Rate Limiting

Implement rate limiting info nếu API cung cấp:

```php
public function getRateLimitInfo(): array
{
    return [
        'limit' => $this->lastResponseHeaders['X-RateLimit-Limit'] ?? null,
        'remaining' => $this->lastResponseHeaders['X-RateLimit-Remaining'] ?? null,
        'reset' => $this->lastResponseHeaders['X-RateLimit-Reset'] ?? null,
    ];
}
```

### 3. Caching

Sử dụng cache cho data ít thay đổi:

```php
public function getCategories(): array
{
    return Cache::remember(
        "marketplace.{$this->getName()}.categories",
        3600, // 1 hour
        fn() => $this->makeApiRequest('GET', '/categories')['data']
    );
}
```

### 4. Pagination

Handle pagination đúng cách:

```php
public function getProducts(array $filters = []): array
{
    $allProducts = [];
    $page = 1;
    
    do {
        $response = $this->makeApiRequest('GET', '/products', [
            'page' => $page,
            'limit' => 100,
        ]);
        
        $products = array_map(
            [$this, 'mapToProductData'],
            $response['data'] ?? []
        );
        
        $allProducts = array_merge($allProducts, $products);
        
        $hasMore = $response['pagination']['has_more'] ?? false;
        $page++;
        
    } while ($hasMore && count($allProducts) < ($filters['max_products'] ?? 1000));
    
    return $allProducts;
}
```

### 5. Webhooks (Nếu marketplace hỗ trợ)

Tạo webhook handler:

```php
namespace Dcnet\Marketplace\Webhooks;

use Illuminate\Http\Request;

class YourMarketplaceWebhookHandler
{
    public function handle(Request $request): void
    {
        $event = $request->input('event');
        
        match ($event) {
            'order.created' => $this->handleOrderCreated($request->input('data')),
            'order.updated' => $this->handleOrderUpdated($request->input('data')),
            'product.updated' => $this->handleProductUpdated($request->input('data')),
            default => Log::warning("Unknown webhook event: {$event}"),
        };
    }
    
    private function handleOrderCreated(array $data): void
    {
        // Process new order
    }
}
```

## 🧪 Testing

Tạo test case:

```php
namespace Tests\Feature\Marketplace;

use Tests\TestCase;
use Dcnet\Marketplace\Connectors\YourMarketplaceConnector;
use Dcnet\Marketplace\DTOs\ConnectionConfig;

class YourMarketplaceConnectorTest extends TestCase
{
    private YourMarketplaceConnector $connector;
    
    protected function setUp(): void
    {
        parent::setUp();
        
        $this->connector = new YourMarketplaceConnector();
        $this->connector->connect(new ConnectionConfig(
            apiKey: 'test_key',
            apiSecret: 'test_secret',
            isSandbox: true,
        ));
    }
    
    public function test_can_connect(): void
    {
        $this->assertTrue($this->connector->isConnected());
    }
    
    public function test_can_get_products(): void
    {
        $products = $this->connector->getProducts();
        
        $this->assertIsArray($products);
        $this->assertNotEmpty($products);
    }
}
```

## 📚 Tài liệu tham khảo

- [MarketplaceConnectorInterface](../src/Contracts/MarketplaceConnectorInterface.php) - Interface bắt buộc
- [AbstractMarketplaceConnector](../src/Connectors/AbstractMarketplaceConnector.php) - Base class với helper methods
- [ShopeeConnector](../src/Connectors/ShopeeConnector.php) - Ví dụ implementation đầy đủ
- [ProductData](../src/DTOs/ProductData.php) - DTO cho sản phẩm
- [OrderData](../src/DTOs/OrderData.php) - DTO cho đơn hàng

## ❓ FAQ

**Q: Làm sao để handle marketplace không support feature nào đó?**

A: Throw exception hoặc return giá trị mặc định:

```php
public function syncInventory(string $productId, int $quantity): bool
{
    throw new \BadMethodCallException(
        "{$this->getName()} does not support inventory sync"
    );
}
```

**Q: Làm sao để test mà không gọi API thật?**

A: Sử dụng HTTP faking của Laravel:

```php
Http::fake([
    'api.yourmarketplace.com/*' => Http::response([
        'data' => [/* mock data */]
    ]),
]);
```

**Q: Marketplace có nhiều region khác nhau thì xử lý sao?**

A: Thêm region vào config:

```php
protected function getBaseUrl(): string
{
    $region = $this->config->additionalConfig['region'] ?? 'vn';
    return "https://api-{$region}.yourmarketplace.com";
}
```
