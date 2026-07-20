// Copyright (c) 2026, DCNET Cloud and contributors
// For license information, please see license.txt

frappe.ui.form.on("DCNet Marketplace Connection", {
    refresh(frm) {
        // Không dùng nút top-bar nữa, chuyển sang dùng nút trong form
    },

    platform(frm) {
        // Reset fields when platform changes...
        const platform = frm.doc.platform;
        if (platform !== "Shopee") {
            frm.set_value("shop_id", "");
            frm.set_value("partner_id", "");
            frm.set_value("api_key", "");
            frm.set_value("api_secret", "");
            frm.set_value("access_token", "");
            frm.set_value("token_expires_at", null);
        }

        if (platform !== "Lazada") {
            frm.set_value("api_key_lazada", "");
            frm.set_value("api_secret_lazada", "");
        }

        if (platform !== "TikTok Shop") {
            frm.set_value("service_id", "");
            frm.set_value("api_key_tiktok", "");
            frm.set_value("api_secret_tiktok", "");
        }

        if (platform !== "Woocommerce") {
            frm.set_value("store_url", "");
            frm.set_value("consumer_key", "");
            frm.set_value("consumer_secret", "");
        }
    },

    /**
     * Hàm chung để xử lý việc lưu và chuyển hướng OAuth.
     */
    initiate_oauth_flow(frm) {
        console.log("initiate_oauth_flow triggered for platform:", frm.doc.platform);
        
        try {
            // 1. Validate nhanh dựa trên Platform
            console.log("Checking connection_name:", frm.doc.connection_name);
            if (!frm.doc.connection_name) {
                frappe.msgprint(__("Vui lòng điền <b>Connection Name</b>."));
                return;
            }

            const platform_fields = {
                "Shopee": [
                    { field: "api_key", label: "API Key" },
                    { field: "api_secret", label: "API Secret" },
                    { field: "shop_id", label: "Shop ID" },
                    { field: "partner_id", label: "Partner ID" }
                ],
                "Lazada": [
                    { field: "api_key_lazada", label: "App Key" },
                    { field: "api_secret_lazada", label: "App Secret" }
                ],
                "TikTok Shop": [
                    { field: "api_key_tiktok", label: "App Key" },
                    { field: "api_secret_tiktok", label: "App Secret" },
                    { field: "service_id", label: "Service ID" }
                ],
                "Woocommerce": [
                    { field: "consumer_key", label: "Consumer Key" },
                    { field: "consumer_secret", label: "Consumer Secret" },
                    { field: "store_url", label: "Store URL" }
                ]
            };

            const required = platform_fields[frm.doc.platform] || [];
            for (let req of required) {
                if (!frm.doc[req.field]) {
                    console.log(`Validation FAILED: ${req.label} is empty for ${frm.doc.platform}`);
                    frappe.msgprint(__("Vui lòng điền <b>{0}</b> cho {1}.", [__(req.label), frm.doc.platform]));
                    return;
                }
            }

            // 2. Lưu và Redirect
            console.log("Validation PASSED. Freezing UI...");
            frappe.dom.freeze(__("Đang chuẩn bị kết nối..."));
        
            const perform_redirect_call = () => {
                console.log("Form is clean. Calling get_auth_url...");
                frm.call({
                    method: "get_auth_url",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    callback: (r) => {
                        console.log("get_auth_url server response:", r);
                        frappe.dom.unfreeze();
                        if (r.message) {
                            console.log("Redirecting to:", r.message);
                            frappe.msgprint(__("Nhận được Auth URL: {0}", [r.message]));
                            
                            frappe.show_alert({message: __("Đang chuyển hướng sang {0}...", [frm.doc.platform]), indicator: 'green'});
                            setTimeout(() => {
                                window.location.href = r.message;
                            }, 800);
                        } else {
                            console.error("No URL returned from server. Response:", r);
                            frappe.msgprint(__("Lỗi: Không nhận được Auth URL từ hệ thống."));
                        }
                    }
                });
            };

            if (frm.is_dirty()) {
                console.log("Form is dirty. Calling frm.save()...");
                frm.save().then(() => {
                    console.log("Form saved successfully.");
                    perform_redirect_call();
                }).catch((err) => {
                    console.error("frm.save() failed:", err);
                    frappe.dom.unfreeze();
                });
            } else {
                perform_redirect_call();
            }
        } catch (e) {
            console.error("Runtime error in initiate_oauth_flow:", e);
        }
    },

    // Sự kiện cho nút Connect trong form Lazada
    connect_lazada(frm) {
        console.log("connect_lazada clicked");
        frm.events.initiate_oauth_flow(frm);
    },

    // Sự kiện cho nút Connect trong form Shopee
    connect_shopee(frm) {
        console.log("connect_shopee clicked");
        frm.events.initiate_oauth_flow(frm);
    },

    // Sự kiện cho nút Connect trong form TikTok Shop
    connect_tiktok(frm) {
        console.log("connect_tiktok clicked");
        frm.events.initiate_oauth_flow(frm);
    },

    // Sự kiện cho nút Connect trong form WooCommerce
    connect_woocommerce(frm) {
        console.log("connect_woocommerce clicked");
        frm.events.initiate_oauth_flow(frm);
    }
});
