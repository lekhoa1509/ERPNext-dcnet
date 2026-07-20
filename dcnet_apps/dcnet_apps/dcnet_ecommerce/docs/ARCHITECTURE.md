# Marketplace Connector - Architecture Diagram

## Class Diagram

```mermaid
classDiagram
    class MarketplaceConnectorInterface {
        <<interface>>
        +getName() string
        +connect(config) bool
        +isConnected() bool
        +disconnect() void
        +getProducts(filters) array
        +getProduct(id) ProductData
        +syncProduct(product) bool
        +updateProduct(id, product) bool
        +deleteProduct(id) bool
        +getOrders(filters) array
        +getOrder(id) OrderData
        +updateOrderStatus(id, status) bool
        +syncInventory(id, quantity) bool
        +getRateLimitInfo() array
    }

    class AbstractMarketplaceConnector {
        <<abstract>>
        #config ConnectionConfig
        #connected bool
        #accessToken string
        +connect(config) bool
        +isConnected() bool
        +disconnect() void
        #authenticate() void*
        #getBaseUrl() string*
        #getApiVersion() string*
        #makeApiRequest() array
        #refreshAccessToken() void
        #cacheToken() void
        #getCachedToken() string
    }

    class ShopeeConnector {
        -SANDBOX_URL string
        -PRODUCTION_URL string
        +getName() string
        +getProducts(filters) array
        +getProduct(id) ProductData
        +syncProduct(product) bool
        +updateProduct(id, product) bool
        +deleteProduct(id) bool
        +getOrders(filters) array
        +getOrder(id) OrderData
        +updateOrderStatus(id, status) bool
        +syncInventory(id, quantity) bool
        #authenticate() void
        #getBaseUrl() string
        #getApiVersion() string
    }

    class LazadaConnector {
        +getName() string
        #authenticate() void
        #getBaseUrl() string
        #getApiVersion() string
    }

    class TikiConnector {
        +getName() string
        #authenticate() void
        #getBaseUrl() string
        #getApiVersion() string
    }

    class TikTokShopConnector {
        +getName() string
        #authenticate() void
        #getBaseUrl() string
        #getApiVersion() string
    }

    class SendoConnector {
        +getName() string
        #authenticate() void
        #getBaseUrl() string
        #getApiVersion() string
    }

    class MarketplaceConnectorFactory {
        -connectors array~string,string~
        +create(marketplace) MarketplaceConnectorInterface$
        +register(marketplace, class) void$
        +getSupportedMarketplaces() array$
        +isSupported(marketplace) bool$
    }

    class MarketplaceService {
        -connections array
        +connect(marketplace, config) MarketplaceConnectorInterface
        +getConnector(marketplace) MarketplaceConnectorInterface
        +syncProductToMarketplace(marketplace, product) bool
        +syncProductsFromMarketplace(marketplace, filters) array
        +syncOrdersFromMarketplace(marketplace, filters) array
        +updateInventory(marketplace, id, quantity) bool
        +updateOrderStatus(marketplace, id, status) bool
        +getSupportedMarketplaces() array
        +disconnect(marketplace) void
        +disconnectAll() void
    }

    class ConnectionConfig {
        +apiKey string
        +apiSecret string
        +shopId string
        +partnerId string
        +accessToken string
        +refreshToken string
        +isSandbox bool
        +additionalConfig array
        +fromArray(data) ConnectionConfig$
        +toArray() array
    }

    class ProductData {
        +id string
        +name string
        +description string
        +price float
        +sku string
        +stock int
        +images array
        +category string
        +attributes array
        +variations array
        +status string
        +fromArray(data) ProductData$
        +toArray() array
    }

    class OrderData {
        +id string
        +orderNumber string
        +status string
        +totalAmount float
        +items array
        +customer array
        +shippingAddress array
        +fromArray(data) OrderData$
        +toArray() array
    }

    MarketplaceConnectorInterface <|.. AbstractMarketplaceConnector
    AbstractMarketplaceConnector <|-- ShopeeConnector
    AbstractMarketplaceConnector <|-- LazadaConnector
    AbstractMarketplaceConnector <|-- TikiConnector
    AbstractMarketplaceConnector <|-- TikTokShopConnector
    AbstractMarketplaceConnector <|-- SendoConnector
    
    MarketplaceConnectorFactory ..> MarketplaceConnectorInterface : creates
    MarketplaceConnectorFactory ..> ShopeeConnector : instantiates
    MarketplaceConnectorFactory ..> LazadaConnector : instantiates
    MarketplaceConnectorFactory ..> TikiConnector : instantiates
    MarketplaceConnectorFactory ..> TikTokShopConnector : instantiates
    MarketplaceConnectorFactory ..> SendoConnector : instantiates
    
    MarketplaceService --> MarketplaceConnectorFactory : uses
    MarketplaceService --> MarketplaceConnectorInterface : manages
    
    AbstractMarketplaceConnector --> ConnectionConfig : uses
    MarketplaceConnectorInterface --> ProductData : returns
    MarketplaceConnectorInterface --> OrderData : returns
```

## Sequence Diagram - Kết nối và Đồng bộ Sản phẩm

```mermaid
sequenceDiagram
    participant Client
    participant Service as MarketplaceService
    participant Factory as MarketplaceConnectorFactory
    participant Connector as ShopeeConnector
    participant API as Shopee API

    Client->>Service: connect('shopee', config)
    Service->>Factory: create('shopee')
    Factory->>Connector: new ShopeeConnector()
    Factory-->>Service: connector instance
    Service->>Connector: connect(config)
    Connector->>Connector: authenticate()
    Connector->>API: POST /auth/token
    API-->>Connector: access_token
    Connector->>Connector: cacheToken(token)
    Connector-->>Service: true
    Service->>Service: store in connections[]
    Service-->>Client: connector

    Note over Client,API: Connector đã sẵn sàng

    Client->>Service: syncProductToMarketplace('shopee', product)
    Service->>Service: getConnector('shopee')
    Service->>Connector: syncProduct(product)
    Connector->>Connector: ensureConnected()
    Connector->>API: POST /product/add_item
    API-->>Connector: {item_id: 123}
    Connector-->>Service: true
    Service-->>Client: true
```

## Flow Diagram - Quy trình xử lý API Request với Retry

```mermaid
flowchart TD
    Start([Start API Request]) --> PrepareRequest[Prepare Request]
    PrepareRequest --> SetAttempt[Set attempt = 0]
    SetAttempt --> CheckAttempts{attempt < maxRetries?}
    
    CheckAttempts -->|Yes| MakeRequest[Make HTTP Request]
    CheckAttempts -->|No| ThrowError[Throw Exception]
    
    MakeRequest --> CheckSuccess{Response Successful?}
    
    CheckSuccess -->|Yes| ReturnData[Return Response Data]
    CheckSuccess -->|No| CheckStatus{Check Status Code}
    
    CheckStatus -->|429 Rate Limited| WaitRetry[Wait Retry-After seconds]
    CheckStatus -->|401 Unauthorized| RefreshToken[Refresh Access Token]
    CheckStatus -->|Other Error| IncrementAttempt[Increment attempt]
    
    WaitRetry --> IncrementAttempt
    RefreshToken --> UpdateHeaders[Update Headers with new token]
    UpdateHeaders --> IncrementAttempt
    
    IncrementAttempt --> ExponentialBackoff[Sleep with exponential backoff]
    ExponentialBackoff --> CheckAttempts
    
    ReturnData --> End([End])
    ThrowError --> End
```

## Component Diagram - Tổng quan hệ thống

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Client Application]
    end

    subgraph "Service Layer"
        MS[MarketplaceService]
    end

    subgraph "Factory Layer"
        Factory[MarketplaceConnectorFactory]
    end

    subgraph "Connector Layer"
        Abstract[AbstractMarketplaceConnector]
        Shopee[ShopeeConnector]
        Lazada[LazadaConnector]
        Tiki[TikiConnector]
        TikTok[TikTokShopConnector]
        Sendo[SendoConnector]
    end

    subgraph "DTO Layer"
        Config[ConnectionConfig]
        Product[ProductData]
        Order[OrderData]
    end

    subgraph "External Systems"
        ShopeeAPI[Shopee API]
        LazadaAPI[Lazada API]
        TikiAPI[Tiki API]
        TikTokAPI[TikTok Shop API]
        SendoAPI[Sendo API]
    end

    Client --> MS
    MS --> Factory
    Factory --> Shopee
    Factory --> Lazada
    Factory --> Tiki
    Factory --> TikTok
    Factory --> Sendo

    Shopee -.-> Abstract
    Lazada -.-> Abstract
    Tiki -.-> Abstract
    TikTok -.-> Abstract
    Sendo -.-> Abstract

    Shopee --> Config
    Shopee --> Product
    Shopee --> Order

    Shopee --> ShopeeAPI
    Lazada --> LazadaAPI
    Tiki --> TikiAPI
    TikTok --> TikTokAPI
    Sendo --> SendoAPI

    style Abstract fill:#f9f,stroke:#333,stroke-width:2px
    style Factory fill:#bbf,stroke:#333,stroke-width:2px
    style MS fill:#bfb,stroke:#333,stroke-width:2px
```

## Design Patterns Applied

### 1. Factory Method Pattern
```mermaid
graph LR
    Client[Client Code] -->|requests| Factory[MarketplaceConnectorFactory]
    Factory -->|creates| Interface[MarketplaceConnectorInterface]
    Interface -.implements.- Shopee[ShopeeConnector]
    Interface -.implements.- Lazada[LazadaConnector]
    Interface -.implements.- Tiki[TikiConnector]
```

### 2. Template Method Pattern
```mermaid
graph TD
    Abstract[AbstractMarketplaceConnector<br/>Template Methods] --> Connect[connect<br/>- authenticate*<br/>- cacheToken]
    Abstract --> MakeRequest[makeApiRequest<br/>- buildUrl<br/>- retry logic<br/>- handle errors]
    Abstract --> Refresh[refreshAccessToken*]
    
    style Abstract fill:#f96,stroke:#333,stroke-width:3px
```

### 3. Strategy Pattern
```mermaid
graph LR
    Context[MarketplaceService] -->|uses| Strategy[MarketplaceConnectorInterface]
    Strategy -.implemented by.- S1[ShopeeConnector]
    Strategy -.implemented by.- S2[LazadaConnector]
    Strategy -.implemented by.- S3[TikiConnector]
```
