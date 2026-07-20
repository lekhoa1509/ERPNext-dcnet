# Module NhatMinh Connect - Diagrams

> **Nguồn:** Phân tích bravo-connect codebase
> **Lưu ý:** Diagrams dựa trên hệ thống HIỆN TẠI đang chạy production

---

## 1. Activity Diagram - Order Push Complete Flow

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
flowchart TD
    A[Khách hàng đặt hàng] --> B[WooCommerce tạo Order]
    B --> C[Order status = pending]

    C --> D{Phương thức<br/>thanh toán?}

    D -->|COD| E[Auto chuyển status<br/>→ processing]
    D -->|Online payment| F[Status → on-hold]

    F --> G[Admin xác nhận<br/>đã nhận tiền]
    G --> H[Status → completed]

    E --> I[Hook triggered:<br/>woocommerce_order_status_changed]
    H --> I

    I --> J{new_status in<br/>[processing, completed]?}

    J -->|No| K[Plugin ignore<br/>không push]
    J -->|Yes| L[Plugin execute<br/>push order]

    L --> M[Call bravoAuth]
    M --> N[POST /token<br/>username, password]

    N --> O{Auth<br/>success?}

    O -->|No| P[Log error:<br/>Auth failed]
    O -->|Yes| Q[Receive access_token]

    Q --> R[Build order payload]

    R --> S[Loop through<br/>order items]

    S --> T{Product<br/>has SKU?}

    T -->|Yes| U[Add to DetailInfo:<br/>ItemCode, Quantity,<br/>OriginalAmount9,<br/>OriginalAmount]
    T -->|No| V[Add to Description:<br/>SP không SKU:<br/>Product name x Qty]

    U --> W{More<br/>items?}
    V --> W

    W -->|Yes| S
    W -->|No| X[Detect USER_PREFIX<br/>from subdomain]

    X --> Y{Subdomain?}

    Y -->|shop| Z[USER_PREFIX = SHOP]
    Y -->|origin/other| AA[USER_PREFIX = ORIGIN]

    Z --> AB[Build DocNo:<br/>SHOP + Order#]
    AA --> AC[Build DocNo:<br/>ORIGIN + Order#]

    AB --> AD[Set OrderSource:<br/>SHOP]
    AC --> AE[Set OrderSource:<br/>ORIGIN]

    AD --> AF{Order status?}
    AE --> AF

    AF -->|processing| AG[PaymentStatus = COD]
    AF -->|completed| AH[PaymentStatus =<br/>Đã chuyển khoản]

    AG --> AI[Complete payload JSON]
    AH --> AI

    AI --> AJ[POST /api/BravoWebApi/execute]
    AJ --> AK[Header:<br/>Authorization: Bearer token]

    AK --> AL{Bravo API<br/>response?}

    AL -->|200 OK| AM[Log success:<br/>Push Order To Bravo OK]
    AL -->|Error| AN[Log error:<br/>API call failed]

    AM --> AO[End]
    AN --> AO
    P --> AO
    K --> AO
```

---

## 2. Activity Diagram - Stock Update Flow

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
flowchart TD
    A[Bravo ERP chuẩn bị<br/>danh sách stock update] --> B[POST /wp-json/api/v1/stock]

    B --> C[Plugin nhận request]

    C --> D{Validate<br/>API key}

    D -->|Invalid| E[Return:<br/>401 Unauthorized]
    D -->|Valid| F{Validate<br/>JSON payload}

    F -->|Invalid| G[Return:<br/>400 Bad Request]
    F -->|Valid| H[Parse JSON array]

    H --> I[Initialize<br/>response array]

    I --> J[Loop through<br/>each item]

    J --> K[Extract:<br/>itemCode, quantity]

    K --> L[wc_get_product_id_by_sku<br/>itemCode]

    L --> M{Product<br/>found?}

    M -->|No| N[Add to response:<br/>status=ERROR<br/>message=Product not found]

    M -->|Yes| O[Load product object<br/>by ID]

    O --> P[Set product properties]

    P --> Q[set_manage_stock<br/>true]
    Q --> R[set_stock_quantity<br/>quantity]
    R --> S[set_stock_status<br/>instock]

    S --> T[product->save]

    T --> U{Save<br/>success?}

    U -->|No| V[Add to response:<br/>status=ERROR<br/>message=Save failed]

    U -->|Yes| W[Add to response:<br/>status=OK<br/>message=Updated successfully<br/>product_id]

    N --> X{More<br/>items?}
    V --> X
    W --> X

    X -->|Yes| J
    X -->|No| Y[Return:<br/>200 OK<br/>response array JSON]

    E --> Z[End]
    G --> Z
    Y --> Z
```

---

## 3. Activity Diagram - Bulk Update Tool Flow

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
flowchart TD
    A[Admin navigate to<br/>WordPress Admin] --> B[Tools → Cập nhật kho]

    B --> C[Display tool page]

    C --> D[Admin click<br/>Cập nhật kho button]

    D --> E[Initialize:<br/>page = 1<br/>limit = 100<br/>updated_count = 0]

    E --> F[Query products<br/>page, limit]

    F --> G{Products<br/>found?}

    G -->|No products| H[Display result:<br/>Đã cập nhật 0 sản phẩm]

    G -->|Yes| I[Loop through<br/>products in page]

    I --> J[Get product type]

    J --> K{Product<br/>type?}

    K -->|grouped| L[Skip product]
    K -->|external| L
    K -->|simple| M[Check stock status]
    K -->|variation| M

    M --> N[Get:<br/>manage_stock<br/>stock_quantity]

    N --> O{manage_stock=false<br/>OR<br/>stock_quantity<=0?}

    O -->|No| P[Skip product<br/>already managed correctly]

    O -->|Yes| Q[Update product]

    Q --> R[set_manage_stock<br/>true]
    R --> S[set_stock_quantity<br/>0]
    S --> T[set_stock_status<br/>outofstock]

    T --> U[product->save]

    U --> V{Save<br/>success?}

    V -->|No| W[Log error]
    V -->|Yes| X[Increment:<br/>updated_count++]

    L --> Y{More products<br/>in page?}
    P --> Y
    W --> Y
    X --> Y

    Y -->|Yes| I
    Y -->|No| Z[page++]

    Z --> AA{More<br/>pages?}

    AA -->|Yes| F
    AA -->|No| AB[Display result:<br/>Đã cập nhật X sản phẩm]

    H --> AC[End]
    AB --> AC
```

---

## 4. Flowchart - Multi-site USER_PREFIX Detection

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
flowchart TB
    A[Start:<br/>Order status changed] --> B[Get site URL<br/>from WordPress]

    B --> C[Parse URL<br/>extract subdomain]

    C --> D{Match<br/>subdomain}

    D -->|shop.nhatminhsports.vn| E[USER_PREFIX = SHOP]
    D -->|nhatminhsports.vn| F[USER_PREFIX = ORIGIN]
    D -->|Other subdomain| F

    E --> G[Build order data]
    F --> G

    G --> H[DocNo =<br/>USER_PREFIX + Order Number]

    H --> I[Example:<br/>SHOP12345]
    H --> J[Example:<br/>ORIGIN12346]

    I --> K[OrderSource = SHOP]
    J --> L[OrderSource = ORIGIN]

    K --> M[Complete order payload]
    L --> M

    M --> N[Push to Bravo API]

    N --> O[Bravo receives order<br/>with source identifier]

    O --> P[End]

    style E fill:#90EE90
    style F fill:#87CEEB
    style I fill:#90EE90
    style J fill:#87CEEB
```

---

## 5. Flowchart - Product SKU Handling Logic

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
flowchart TD
    A[Start:<br/>Processing order items] --> B[Initialize:<br/>DetailInfo = []<br/>Description = Customer note]

    B --> C[Get all order items]

    C --> D[Loop item by item]

    D --> E[Get product from item]

    E --> F{Product<br/>exists?}

    F -->|No| G[Skip item]

    F -->|Yes| H[Get product SKU]

    H --> I{SKU<br/>empty?}

    I -->|No - Has SKU| J[Extract item data]

    J --> K[ItemCode = SKU<br/>Quantity = item qty<br/>OriginalAmount9 = subtotal<br/>OriginalAmount = total]

    K --> L[Create item object]

    L --> M[Add to DetailInfo array]

    I -->|Yes - No SKU| N[Get product name<br/>and quantity]

    N --> O[Format string:<br/>SP không SKU:<br/>Product name x Qty]

    O --> P[Append to<br/>Description string]

    M --> Q{More<br/>items?}
    P --> Q
    G --> Q

    Q -->|Yes| D
    Q -->|No| R[Build final payload]

    R --> S[Payload contains:<br/>DetailInfo array<br/>with SKU items only]

    S --> T[Payload contains:<br/>Description string<br/>with no-SKU items]

    T --> U[Push to Bravo]

    U --> V[Bravo processes:<br/>DetailInfo automatically]

    V --> W[Bravo processes:<br/>Description manually]

    W --> X[End]

    style M fill:#90EE90
    style P fill:#FFB6C1
    style S fill:#90EE90
    style T fill:#FFB6C1
```

---

## 6. Component Diagram - Plugin Architecture

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
graph TB
    subgraph WordPress["WordPress Core"]
        WP[WordPress<br/>Core Functions]
        WP_Hooks[Hooks System<br/>Actions & Filters]
        WP_REST[REST API<br/>Framework]
    end

    subgraph WooCommerce["WooCommerce"]
        WC_Core[WooCommerce<br/>Core]
        WC_Orders[Order<br/>Management]
        WC_Products[Product<br/>Management]
        WC_Hooks[WooCommerce<br/>Hooks]
    end

    subgraph Plugin["Bravo Connect Plugin"]
        Entry[index.php<br/>Plugin Header<br/>Activation/Deactivation]

        Init[Inc/Init.php<br/>Service Registration<br/>Dependency Injection]

        subgraph Core["Inc/Core/"]
            API[Api.php<br/>- REST endpoints registration<br/>- Order status hook handler<br/>- Stock update endpoint<br/>- Product list endpoint]

            Helpers[Helpers.php<br/>- bravoAuth<br/>- orderToBravo<br/>- getUserPrefix<br/>- HTTP client wrapper]

            Stock[StockUpdater.php<br/>- Admin menu registration<br/>- Bulk update logic<br/>- Product scanner]

            MW[Middleware.php<br/>- API key validation<br/>- Request authentication]
        end

        Logger[Monolog Logger<br/>logs.log<br/>- Order push logs<br/>- Stock update logs<br/>- Error logs]
    end

    subgraph External["External Systems"]
        Bravo[Bravo ERP API<br/>222.252.4.126:60124<br/>- /token OAuth2<br/>- /api/BravoWebApi/execute]
    end

    subgraph Dependencies["Composer Dependencies"]
        Monolog[monolog/monolog<br/>v3.9]
        Guzzle[guzzlehttp/guzzle<br/>v7.9<br/>HTTP Client]
    end

    %% Connections
    Entry --> Init
    Init --> API
    Init --> Stock
    Init --> MW

    API --> Helpers
    API --> Logger
    Stock --> Logger
    Helpers --> Logger

    WP_Hooks --> API
    WP_REST --> API
    WP --> Stock

    WC_Hooks --> API
    WC_Orders --> API
    WC_Products --> API
    WC_Products --> Stock

    Helpers --> Bravo
    Helpers --> Guzzle

    Logger --> Monolog

    API --> MW

    %% Styling
    style Entry fill:#FFE4B5
    style Init fill:#FFE4B5
    style API fill:#87CEEB
    style Helpers fill:#87CEEB
    style Stock fill:#87CEEB
    style MW fill:#87CEEB
    style Logger fill:#98FB98
    style Bravo fill:#FFB6C1
```

---

## 7. Sequence Diagram - Authentication Flow

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
sequenceDiagram
    participant P as Plugin
    participant G as Guzzle Client
    participant B as Bravo API

    Note over P: Order status changed<br/>Need to push order

    P->>P: Call bravoAuth()

    P->>G: Create HTTP client
    Note over G: Base URI:<br/>http://222.252.4.126:60124

    P->>G: Prepare POST request<br/>/token

    G->>B: POST /token
    Note over G,B: Body (form-data):<br/>username=NMAPI<br/>password=***<br/>grant_type=password

    alt Success
        B-->>G: 200 OK
        Note over B: Response body:<br/>{<br/> "access_token": "...",<br/> "token_type": "bearer",<br/> "expires_in": 1209599<br/>}

        G-->>P: Return response

        P->>P: Parse JSON<br/>Extract access_token

        P->>P: Return access_token

        Note over P: Token ready<br/>for orderToBravo()

    else Auth Failed
        B-->>G: 401 Unauthorized
        Note over B: Invalid credentials

        G-->>P: Return error response

        P->>P: Log error:<br/>Auth failed

        P->>P: Return NULL

        Note over P: Order push<br/>aborted
    end
```

---

## 8. Sequence Diagram - Error Recovery (or Lack Thereof)

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
sequenceDiagram
    participant WC as WooCommerce
    participant P as Plugin
    participant L as Logs
    participant A as Admin

    WC->>P: Order status → processing

    P->>P: Attempt to push order

    alt Scenario 1: Auth Failed
        P->>P: bravoAuth() fails
        P->>L: Log: Auth failed
        Note over P,L: Order NOT pushed<br/>NO retry<br/>NO notification
    end

    alt Scenario 2: API Timeout
        P->>P: orderToBravo() timeout
        P->>L: Log: API timeout
        Note over P,L: Order NOT pushed<br/>NO retry<br/>NO notification
    end

    alt Scenario 3: Bravo 500 Error
        P->>P: Bravo returns 500
        P->>L: Log: Bravo error
        Note over P,L: Order NOT pushed<br/>NO retry<br/>NO notification
    end

    Note over A: Hours/days later...

    A->>L: Admin checks logs<br/>(via FTP/SSH)
    L-->>A: Discovers failed orders

    A->>WC: Manual intervention required
    Note over A: Admin must:<br/>1. Fix root cause<br/>2. Manually export orders<br/>3. Import to Bravo<br/>OR<br/>Manually change order status<br/>to trigger re-push<br/>(but no guarantee it works)

    rect rgb(255, 200, 200)
        Note over WC,A: PAIN POINT:<br/>No automatic recovery<br/>No admin notification<br/>Order "lost" in sync<br/>Manual reconciliation needed
    end
```

---

## 9. State Machine Diagram - Order Sync States

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
stateDiagram-v2
    [*] --> NotEligible: Order created<br/>status=pending

    NotEligible --> Eligible: Status changed<br/>→ processing/completed

    Eligible --> Authenticating: Hook triggered<br/>Plugin start

    Authenticating --> AuthSuccess: POST /token<br/>→ 200 OK
    Authenticating --> AuthFailed: POST /token<br/>→ Error

    AuthSuccess --> BuildingPayload: Extract order data

    BuildingPayload --> PushingOrder: POST /api/BravoWebApi/execute

    PushingOrder --> SyncSuccess: API → 200 OK
    PushingOrder --> SyncFailed: API → Error

    SyncSuccess --> [*]: Log success<br/>Order synced

    SyncFailed --> [*]: Log error<br/>Order NOT synced

    AuthFailed --> [*]: Log error<br/>Order NOT synced

    NotEligible --> [*]: Status changed<br/>→ cancelled/failed

    note right of NotEligible
        States:
        - pending
        - on-hold
        - cancelled
        - failed
        - refunded
    end note

    note right of Eligible
        States:
        - processing
        - completed
    end note

    note right of SyncFailed
        NO RETRY
        Manual intervention required
    end note

    note right of AuthFailed
        NO RETRY
        Manual intervention required
    end note
```

---

## 10. Data Flow Diagram - Complete Integration

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
flowchart TB
    subgraph Customer["Customer Journey"]
        C1[Customer visits website]
        C2[Add products to cart]
        C3[Checkout]
        C4[Select payment method]
        C5[Place order]
    end

    subgraph WooCommerce["WooCommerce System"]
        WC1[Order created<br/>status: pending]
        WC2{Payment<br/>method?}
        WC3[Status: processing<br/>COD]
        WC4[Status: on-hold<br/>Online payment]
        WC5[Admin confirms<br/>→ completed]
    end

    subgraph Plugin["Bravo Connect"]
        P1[Hook listener<br/>order_status_changed]
        P2{Status in<br/>processing/completed?}
        P3[Extract order data]
        P4[Detect USER_PREFIX]
        P5[Process items<br/>SKU vs No-SKU]
        P6[Build payload]
        P7[Authenticate]
        P8[Push to Bravo]
        P9[Log result]
    end

    subgraph Bravo["Bravo ERP"]
        B1[/token endpoint<br/>OAuth2 Auth]
        B2[/api/BravoWebApi/execute<br/>Receive order]
        B3[Create SalesOrder<br/>in Bravo DB]
        B4[Calculate inventory]
        B5[Prepare stock data]
        B6[Call WooCommerce<br/>stock update API]
    end

    subgraph StockSync["Stock Sync"]
        S1[POST /api/v1/stock]
        S2[Validate API key]
        S3[Loop items]
        S4[Find product by SKU]
        S5[Update stock quantity]
        S6[Save product]
        S7[Return response]
    end

    C1 --> C2 --> C3 --> C4 --> C5
    C5 --> WC1
    WC1 --> WC2
    WC2 -->|COD| WC3
    WC2 -->|Online| WC4
    WC4 --> WC5

    WC3 --> P1
    WC5 --> P1

    P1 --> P2
    P2 -->|Yes| P3
    P2 -->|No| P9

    P3 --> P4 --> P5 --> P6 --> P7

    P7 --> B1
    B1 --> P8
    P8 --> B2

    B2 --> B3
    B3 --> P9

    B3 --> B4
    B4 --> B5
    B5 --> B6

    B6 --> S1
    S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7

    S7 --> B5

    style C5 fill:#FFE4B5
    style WC3 fill:#90EE90
    style WC5 fill:#87CEEB
    style P8 fill:#FFB6C1
    style B3 fill:#FFB6C1
    style S6 fill:#98FB98
```

---

## 11. Deployment Diagram - System Topology

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
graph TB
    subgraph Internet["Internet"]
        Customers[Customers<br/>Web Browsers]
    end

    subgraph Hosting["Web Hosting Server"]
        subgraph WordPress["WordPress Installation"]
            WP_Core[WordPress Core]
            WC_Plugin[WooCommerce Plugin]
            BC_Plugin[Bravo Connect Plugin]
            DB[(MySQL Database<br/>wp_posts<br/>wp_postmeta<br/>wp_woocommerce_*)]
        end

        Files[File System<br/>bravo-connect/<br/>├── index.php<br/>├── Inc/<br/>├── logs.log<br/>└── vendor/]
    end

    subgraph BravoServer["Bravo ERP Server<br/>222.252.4.126:60124"]
        Bravo_API[Bravo API<br/>/token<br/>/api/BravoWebApi/execute]
        Bravo_DB[(Bravo Database<br/>SalesOrders<br/>Inventory<br/>Customers)]
    end

    Customers -->|HTTPS| WP_Core
    WP_Core --> WC_Plugin
    WC_Plugin --> BC_Plugin
    BC_Plugin --> Files
    WC_Plugin --> DB
    BC_Plugin --> DB

    BC_Plugin -->|HTTP<br/>Port 60124| Bravo_API
    Bravo_API --> Bravo_DB

    Bravo_API -->|HTTPS<br/>/wp-json/api/v1/stock| BC_Plugin

    style Customers fill:#FFE4B5
    style BC_Plugin fill:#87CEEB
    style Bravo_API fill:#FFB6C1
    style Files fill:#98FB98
```

---

## 12. Mindmap - Plugin Feature Overview

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
mindmap
  root((Bravo Connect<br/>Plugin))
    Order Sync
      Push to Bravo
        COD orders
          Status processing
          PaymentStatus COD
        Online payment orders
          Status completed
          PaymentStatus Đã chuyển khoản
      Multi-site support
        SHOP prefix
          shop.nhatminhsports.vn
        ORIGIN prefix
          nhatminhsports.vn
      Item handling
        Items with SKU
          Add to DetailInfo
        Items without SKU
          Add to Description
      Authentication
        OAuth2 password grant
        POST /token
        Access token

    Stock Management
      Receive from Bravo
        POST /api/v1/stock
        API key auth
        JSON payload
      Update WooCommerce
        Find by SKU
        Set manage_stock true
        Set stock quantity
        Set stock status
      Bulk Update Tool
        WordPress admin tool
        Scan all products
        Fix stock status
        100 products per page

    Product Data
      Read-only API
        GET /api/v1/product
        Pagination support
        Return product info
      Bravo can read
        ID, Name, SKU
        Price, Stock
        Categories, Images
      No write operations
        Cannot create
        Cannot update
        Manual management

    Logging
      Monolog library
      logs.log file
      Log entries
        Order push
        Stock updates
        Errors
      No admin UI
        FTP/SSH access needed

    Pain Points
      No retry mechanism
      No error notification
      Hardcoded credentials
      No sync status UI
      Blocking operations
      No performance optimization
```

---

## 13. Comparison Diagram - Current vs Proposed FlowNext

**Nguồn:** Phân tích bravo-connect codebase + Đề xuất

```mermaid
graph TB
    subgraph Current["Current: Bravo Connect"]
        C1[WooCommerce]
        C2[Bravo Connect Plugin]
        C3[Bravo ERP<br/>222.252.4.126]

        C1 -->|Hook: Sync| C2
        C2 -->|HTTP: Push Order| C3
        C3 -->|HTTP: Update Stock| C2
        C2 -->|Direct: Update DB| C1

        C_Issues[Issues:<br/>❌ No retry<br/>❌ No notification<br/>❌ Hardcoded keys<br/>❌ Blocking calls<br/>❌ No admin UI]
    end

    subgraph Proposed["Proposed: FlowNext Connect"]
        P1[WooCommerce]
        P2[FlowNext Connect Plugin]
        P3[Queue System<br/>WP Cron/Redis]
        P4[FlowNext API<br/>api.flownext.dcnet.vn]
        P5[FlowNext Database]
        P6[Admin Dashboard]

        P1 -->|Hook: Enqueue| P2
        P2 -->|Async: Add to Queue| P3
        P3 -->|Background: Process| P4
        P4 -->|RESTful API| P5
        P4 -->|Webhook: Stock Update| P2
        P2 -->|Update| P1
        P2 -->|UI: Status| P6
        P6 -->|View/Retry| P2

        P_Benefits[Benefits:<br/>✅ Auto retry (3 attempts)<br/>✅ Email notifications<br/>✅ Environment config<br/>✅ Non-blocking<br/>✅ Full admin UI<br/>✅ Sync status tracking<br/>✅ Manual retry button<br/>✅ Error dashboard]
    end

    Current -.->|Migration Path| Proposed

    style C_Issues fill:#FFB6C1
    style P_Benefits fill:#90EE90
```

---

## 14. Timeline Diagram - Order Sync Lifecycle

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
gantt
    title Order Sync Lifecycle (Current Implementation)
    dateFormat  HH:mm:ss
    axisFormat %H:%M:%S

    section Customer
    Place order           :a1, 08:00:00, 5s
    Order pending         :a2, after a1, 10s

    section WooCommerce
    Status → processing   :b1, after a2, 1s
    Hook triggered        :b2, after b1, 1s

    section Plugin
    Receive hook          :c1, after b2, 1s
    Auth request          :c2, after c1, 2s
    Build payload         :c3, after c2, 3s
    Push to Bravo         :crit, c4, after c3, 5s

    section Bravo
    Process order         :d1, after c4, 8s
    Save to DB            :d2, after d1, 2s
    Return response       :d3, after d2, 1s

    section Plugin
    Receive response      :e1, after d3, 1s
    Write log             :e2, after e1, 1s
    Complete              :milestone, e3, after e2, 0s

    section Total
    Total time: ~45s      :active, after a1, 45s
```

**Note:** Blocking nature means WooCommerce admin/checkout page waits for entire process to complete.

---

## 15. Risk Matrix Diagram

**Nguồn:** Phân tích bravo-connect codebase

```mermaid
quadrantChart
    title Risk Assessment - Bravo Connect Plugin
    x-axis Low Impact --> High Impact
    y-axis Low Probability --> High Probability
    quadrant-1 Critical Risks
    quadrant-2 Monitor
    quadrant-3 Low Priority
    quadrant-4 Significant Risks

    No retry mechanism: [0.8, 0.7]
    Hardcoded API keys: [0.9, 0.5]
    No error notification: [0.7, 0.8]
    Blocking operations: [0.6, 0.6]
    No admin UI: [0.5, 0.7]
    Single point of failure: [0.9, 0.4]
    No rate limiting: [0.7, 0.3]
    Performance issues: [0.5, 0.5]
    No monitoring: [0.6, 0.8]
    Token not cached: [0.4, 0.3]
```

**Legend:**
- **Quadrant 1 (Critical):** High probability, high impact - immediate action needed
- **Quadrant 2 (Monitor):** Low impact, high probability - keep watching
- **Quadrant 3 (Low Priority):** Low probability, low impact - accept risk
- **Quadrant 4 (Significant):** High impact, low probability - contingency plan

---

**Nguồn:** Phân tích bravo-connect codebase tại `/Users/vovanduc/Code/dcnet/bravo-connect`
**Ngày cập nhật:** 10/01/2026
**Trạng thái:** Production system documentation - All diagrams based on actual codebase analysis
