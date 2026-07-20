Giai đoạn 1: Khởi tạo kết nối từ Giao diện người dùng (UI)

   1. Bước 1: Người dùng nhấn "Create" trong Filament
       * File: Filament/Admin/Resources/MarketplaceConnectionResource/Pages/CreateMarketplaceConnection.php
       * Người dùng điền các thông tin như Connection Name, Service ID (chính là shop_id của TikTok), API Key, API Secret và nhấn nút "Create".
       * Hành động này kích hoạt phương thức mutateFormDataBeforeCreate().

   2. Bước 2: `CreateMarketplaceConnection` gọi đến `TikTokShopService`
       * File: Filament/Admin/Resources/MarketplaceConnectionResource/Pages/CreateMarketplaceConnection.php
       * Phương thức mutateFormDataBeforeCreate không tạo bản ghi trong database ngay. Thay vào đó, nó kiểm tra platform là tiktokshop và gọi đến service tương ứng, sau đó dừng tiến
         trình của Filament.

   1     if ($platform === MarketplaceType::TIKTOKSHOP->value) {
   2         app(TikTokShopService::class)->validateAndConnect($data);
   3         $this->halt(); // <-- Dừng việc tạo record, chờ xử lý OAuth
   4     }

   3. Bước 3: `TikTokShopService` chuẩn bị và lấy URL xác thực
       * File: src/Services/TikTokShopService.php
       * Phương thức validateAndConnect() được gọi. Nó thực hiện các việc sau:
           * Tạo một đối tượng ConnectionConfig (DTO) từ dữ liệu form.
           * Gọi đến MarketplaceService để khởi tạo luồng OAuth và lấy URL xác thực của TikTok.
           * Quan trọng: Lưu trữ thông tin cấu hình (config) và dữ liệu form (data) vào session, được khóa bằng một chuỗi state ngẫu nhiên. Việc này để lấy lại thông tin ở bước
             callback.
           * Chuyển hướng (redirect) người dùng đến URL xác thực của TikTok.

    1     // trong TikTokShopService.php
    2     public function validateAndConnect(array $data): array
    3     {
    4         // ... tạo $config
    5         $authUrl = $this->marketplaceService->initiateOAuth($data['platform'], $config);
    6 
    7         // Lưu config vào session để dùng ở callback
    8         $state = Str::uuid()->();
    9         session()->put("tiktokshop_oauth.$state", [
   10             'config' => $config->toArray(),
   11             'data'   => $data,S
   12         ]);                   t
   13                               r
   14         redirect($authUrl.'&state='.$state); // <-- Chuyển hướng người dùng
   15                               n
   16         return [];            g
   17     }

   4. Bước 4: `TikTokShopConnector` tạo URL xác thực
       * File: src/Connectors/TikTokShopConnector.php
       * MarketplaceService đã dùng Factory để tạo ra TikTokShopConnector. Sau đó, phương thức getAuthUrl() của connector này được gọi để tạo URL chính xác theo tài liệu của TikTok.

   1     // trong TikTokShopConnector.php
   2     public function getAuthUrl(): string
   3     {
   4         return 'https://services.tiktokshop.com/open/authorize?'.http_build_query([
   5             'service_id'   => $this->config->shopId,
   6         ]);
   7     }

  Giai đoạn 2: Người dùng cấp quyền và xử lý Callback

   5. Bước 5: Người dùng cấp quyền trên TikTok Shop
       * Người dùng được chuyển hướng đến trang của TikTok, đăng nhập và chấp nhận cấp quyền cho ứng dụng.
       * Sau khi thành công, TikTok sẽ chuyển hướng người dùng trở lại redirect_uri đã đăng ký, đính kèm theo một code (mã xác thực) và state (chuỗi ngẫu nhiên đã gửi đi ở Bước 3).

   6. Bước 6: `TikTokShopCallbackController` nhận yêu cầu
       * File: routes/web.php định nghĩa route cho callback:

   1         Route::get('tiktok/callback', [TikTokShopCallbackController::class, 'handleCallback'])->name('tiktok.callback');
       * File: src/Http/Controllers/TikTokShopCallbackController.php
       * Phương thức handleCallback() được kích hoạt. Nó lấy code từ request và gọi TikTokShopService để xử lý phần logic phức tạp.

    1     // trong TikTokShopCallbackController.php
    2     public function handleCallback(Request $request): RedirectResponse
    3     {
    4         // ...
    5         $code = $request->get('code');
    6         // ...
    7         $this->tiktokShopService->handleCallback($code);
    8         // ...
    9         return redirect()->route('filament.admin.resources.marketplace.connections.index');
   10     }

   7. Bước 7: `TikTokShopService` xử lý Callback và lấy Access Token
       * File: src/Services/TikTokShopService.php
       * Đây là bước quan trọng nhất, phương thức handleCallback() thực hiện:
           * Xác thực `state`: Lấy state từ URL và dùng nó để lấy lại dữ liệu đã lưu trong session ở Bước 3. Nếu không có hoặc không khớp, luồng sẽ dừng lại (chống tấn công CSRF).
           * Đổi `code` lấy `access_token`: Gọi đến MarketplaceService::handleOAuthCallback(), service này sẽ tiếp tục gọi generateAccessToken() trong TikTokShopConnector.
           * `TikTokShopConnector` gọi API của TikTok: Phương thức generateAccessToken() trong TikTokShopConnector.php gửi request đến API của TikTok để đổi code lấy access_token và
             refresh_token.

   1     // trong TikTokShopConnector.php
   2     public function generateAccessToken(string $code): TokenDTO
   3     {
   4         // ... chuẩn bị params
   5         $response = Http::get(self::AUTH_URL.$endpoint, $params);
   6         // ... xử lý response
   7         return new TokenDTO(...); // Trả về DTO chứa token
   8     }

   8. Bước 8: Lưu thông tin kết nối vào Database
       * File: src/Services/TikTokShopService.php
       * Sau khi đã có TokenDTO (chứa access token), phương thức handleCallback() tiếp tục:
           * Chuẩn bị một mảng dữ liệu $updateData chứa các thông tin từ form ban đầu (đã lấy lại từ session) và các thông tin mặc định (status, user_id, last_connected_at).
           * Gọi MarketplaceService::buildCredentialUpdateData() để mã hóa các thông tin nhạy cảm (token, secret, key) bằng Crypt::encryptString().
           * Sử dụng MarketplaceConnection::updateOrCreate() để tạo mới hoặc cập nhật bản ghi trong database.
           * Xóa session đã dùng.
           * Toàn bộ quá trình này được bọc trong một DB::transaction để đảm bảo tính toàn vẹn dữ liệu.

  Sau khi hoàn tất, người dùng được chuyển về trang danh sách Connections trong Filament và thấy kết nối mới đã được tạo với trạng thái "Active".

  Các thành phần chính và vai trò

   * Filament Resource (`CreateMarketplaceConnection`): Điểm bắt đầu, thu thập thông tin và kích hoạt luồng.
   * Controller (`TikTokShopCallbackController`): Endpoint để TikTok gọi về, vai trò rất mỏng, chỉ điều phối request cho Service.
   * Service (`TikTokShopService`): Chứa logic nghiệp vụ chính cho TikTok, điều phối luồng đi và về, quản lý session.
   * Core Service (`MarketplaceService`): Chứa logic OAuth chung có thể tái sử dụng cho nhiều sàn (Lazada, Shopee...).
   * Connector (`TikTokShopConnector`): Lớp "thực thi", chịu trách nhiệm tạo URL và gọi API trực tiếp đến TikTok.
   * DTO (`ConnectionConfig`, `TokenDTO`): Các đối tượng truyền dữ liệu, giúp code sạch và type-safe.
   * Model (`MarketplaceConnection`): Đại diện cho bảng dữ liệu, nơi lưu trữ cuối cùng.