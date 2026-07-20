# Hướng dẫn Phân quyền cho Marketplace Plugin

## 📋 Tổng quan

Marketplace plugin sử dụng **Laravel Policy** để quản lý permissions. Hệ thống permissions tích hợp với **Filament Shield** và **Spatie Permission** package.

## 🏗️ Cấu trúc Permissions

### 1. Models

Plugin có 2 models chính cần quản lý permissions:

- **MarketplaceConnection** - Quản lý kết nối với các sàn
- **MarketplaceSyncLog** - Logs của quá trình đồng bộ

### 2. Policies

Mỗi model có một Policy tương ứng:

```
src/Policies/
├── MarketplaceConnectionPolicy.php
└── MarketplaceSyncLogPolicy.php
```

## 🔐 Danh sách Permissions

### MarketplaceConnection Permissions

| Permission | Description | Policy Method |
|-----------|-------------|---------------|
| `view_any_marketplace_connection` | Xem danh sách connections | `viewAny()` |
| `view_marketplace_connection` | Xem chi tiết connection | `view()` |
| `create_marketplace_connection` | Tạo connection mới | `create()` |
| `update_marketplace_connection` | Cập nhật connection | `update()` |
| `delete_marketplace_connection` | Xóa connection | `delete()` |
| `delete_any_marketplace_connection` | Xóa nhiều connections | `deleteAny()` |
| `force_delete_marketplace_connection` | Xóa vĩnh viễn | `forceDelete()` |
| `force_delete_any_marketplace_connection` | Xóa vĩnh viễn nhiều | `forceDeleteAny()` |
| `restore_marketplace_connection` | Khôi phục connection đã xóa | `restore()` |
| `restore_any_marketplace_connection` | Khôi phục nhiều connections | `restoreAny()` |
| `replicate_marketplace_connection` | Nhân bản connection | `replicate()` |
| `reorder_marketplace_connection` | Sắp xếp lại | `reorder()` |
| **`test_marketplace_connection`** | **Test kết nối** ⭐ | `testConnection()` |
| **`sync_marketplace_connection`** | **Đồng bộ dữ liệu** ⭐ | `sync()` |

⭐ = Custom permissions đặc biệt cho marketplace

### MarketplaceSyncLog Permissions

| Permission | Description | Policy Method |
|-----------|-------------|---------------|
| `view_any_marketplace_sync_log` | Xem danh sách logs | `viewAny()` |
| `view_marketplace_sync_log` | Xem chi tiết log | `view()` |
| `delete_marketplace_sync_log` | Xóa log | `delete()` |
| `delete_any_marketplace_sync_log` | Xóa nhiều logs | `deleteAny()` |
| **`retry_marketplace_sync`** | **Retry sync thất bại** ⭐ | `retry()` |

**Note**: Sync logs là read-only, không cho phép create/update

## 📝 Cách thức hoạt động

### 1. Policy Registration

Trong [`MarketplaceServiceProvider.php`](file:///Users/doancuong/Documents/dcnetcloud-crm/flow_crm/plugins/webkul/marketplace/src/MarketplaceServiceProvider.php):

```php
protected function registerPolicies(): void
{
    Gate::policy(MarketplaceConnection::class, MarketplaceConnectionPolicy::class);
    Gate::policy(MarketplaceSyncLog::class, MarketplaceSyncLogPolicy::class);
}

public function packageBooted(): void
{
    $this->registerPolicies();
    // ...
}
```

### 2. Policy Implementation

Ví dụ trong [`MarketplaceConnectionPolicy.php`](file:///Users/doancuong/Documents/dcnetcloud-crm/flow_crm/plugins/webkul/marketplace/src/Policies/MarketplaceConnectionPolicy.php):

```php
public function viewAny(User $user): bool
{
    return $user->can('view_any_marketplace_connection');
}

public function create(User $user): bool
{
    return $user->can('create_marketplace_connection');
}

// Custom permission
public function testConnection(User $user, MarketplaceConnection $connection): bool
{
    return $user->can('test_marketplace_connection');
}
```

### 3. Sử dụng trong Code

```php
// Check permission
if (auth()->user()->can('create_marketplace_connection')) {
    // User có quyền tạo connection
}

// Check với model instance
if (auth()->user()->can('update', $connection)) {
    // User có quyền update connection này
}

// Check custom permission
if (auth()->user()->can('testConnection', $connection)) {
    // User có quyền test connection này
}
```

### 4. Sử dụng trong Filament Resource

```php
use Dcnet\Marketplace\Models\MarketplaceConnection;

class MarketplaceConnectionResource extends Resource
{
    protected static ?string $model = MarketplaceConnection::class;
    
    // Filament tự động check permissions dựa trên policy
    
    public static function canViewAny(): bool
    {
        // Tự động check 'view_any_marketplace_connection'
        return parent::canViewAny();
    }
    
    // Custom action với permission check
    public function testAction(): Action
    {
        return Action::make('test')
            ->label('Test Connection')
            ->requiresConfirmation()
            ->authorize('testConnection') // Check custom permission
            ->action(function (MarketplaceConnection $record) {
                // Test connection logic
            });
    }
}
```

## 🎯 Setup Permissions

### Bước 1: Tạo Permissions trong Database

Tạo migration để insert permissions:

```php
use Spatie\Permission\Models\Permission;

// Tạo các permissions cho MarketplaceConnection
$permissions = [
    'view_any_marketplace_connection',
    'view_marketplace_connection',
    'create_marketplace_connection',
    'update_marketplace_connection',
    'delete_marketplace_connection',
    'delete_any_marketplace_connection',
    'force_delete_marketplace_connection',
    'force_delete_any_marketplace_connection',
    'restore_marketplace_connection',
    'restore_any_marketplace_connection',
    'replicate_marketplace_connection',
    'reorder_marketplace_connection',
    'test_marketplace_connection',
    'sync_marketplace_connection',
];

foreach ($permissions as $permission) {
    Permission::create(['name' => $permission]);
}

// Tạo các permissions cho MarketplaceSyncLog
$logPermissions = [
    'view_any_marketplace_sync_log',
    'view_marketplace_sync_log',
    'delete_marketplace_sync_log',
    'delete_any_marketplace_sync_log',
    'retry_marketplace_sync',
];

foreach ($logPermissions as $permission) {
    Permission::create(['name' => $permission]);
}
```

### Bước 2: Gán Permissions cho Roles

```php
use Spatie\Permission\Models\Role;

$adminRole = Role::findByName('admin');

// Admin có tất cả permissions
$adminRole->givePermissionTo([
    'view_any_marketplace_connection',
    'create_marketplace_connection',
    'update_marketplace_connection',
    'delete_marketplace_connection',
    'test_marketplace_connection',
    'sync_marketplace_connection',
    // ... all permissions
]);

$managerRole = Role::findByName('manager');

// Manager chỉ có quyền view và test
$managerRole->givePermissionTo([
    'view_any_marketplace_connection',
    'view_marketplace_connection',
    'test_marketplace_connection',
]);
```

### Bước 3: Guard trong Controller/Action

```php
// Trong Controller
public function store(Request $request)
{
    $this->authorize('create', MarketplaceConnection::class);
    
    // Create logic
}

public function testConnection(MarketplaceConnection $connection)
{
    $this->authorize('testConnection', $connection);
    
    // Test logic
}

// Trong Filament Action
Actions\Action::make('sync')
    ->authorize('sync')
    ->action(function (MarketplaceConnection $record) {
        // Sync logic
    });
```

## 🔒 Best Practices

### 1. Luôn kiểm tra permissions

```php
// ❌ Bad
public function sync()
{
    // No permission check
    $this->marketplaceService->sync();
}

// ✅ Good
public function sync(MarketplaceConnection $connection)
{
    $this->authorize('sync', $connection);
    
    $this->marketplaceService->sync($connection);
}
```

### 2. Sử dụng Gate facade cho complex logic

```php
use Illuminate\Support\Facades\Gate;

// Check multiple permissions
if (Gate::any(['test_marketplace_connection', 'sync_marketplace_connection'], $connection)) {
    // User có ít nhất một trong hai quyền
}

// Check với additional logic
Gate::define('advanced-sync', function (User $user, MarketplaceConnection $connection) {
    return $user->can('sync_marketplace_connection') 
        && $connection->is_active
        && !$connection->isTokenExpired();
});
```

### 3. Custom Error Messages

```php
public function testConnection(MarketplaceConnection $connection)
{
    abort_unless(
        auth()->user()->can('testConnection', $connection),
        403,
        'Bạn không có quyền test kết nối marketplace này.'
    );
    
    // Test logic
}
```

## 📚 Tài liệu tham khảo

- [Laravel Authorization](https://laravel.com/docs/authorization)
- [Spatie Laravel Permission](https://spatie.be/docs/laravel-permission)
- [Filament Authorization](https://filamentphp.com/docs/panels/users#authorization)

## 💡 Tips

1. **Permission Naming Convention**: Sử dụng pattern `{verb}_{resource}` 
   - Ví dụ: `view_marketplace_connection`, `create_marketplace_connection`

2. **Custom Permissions**: Thêm prefix để phân biệt
   - Standard: `view_`, `create_`, `update_`, `delete_`
   - Custom: `test_`, `sync_`, `retry_`

3. **Role-based vs Resource-based**: 
   - Resource-based (có model): `$user->can('update', $connection)`
   - Role-based (không model): `$user->can('create_marketplace_connection')`

4. **Testing Permissions**:
```php
// In tests
$this->actingAs($user)
     ->post('/api/marketplace/connections')
     ->assertForbidden(); // 403

$user->givePermissionTo('create_marketplace_connection');

$this->actingAs($user)
     ->post('/api/marketplace/connections')
     ->assertSuccessful(); // 200
```
