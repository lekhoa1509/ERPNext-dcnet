frappe.ui.form.on("Item", {
    refresh(frm) {
        if (!frm.doc.name) {
            return;
        }
        
        if (!frm.fields_dict.custom_image_manager) {
            return;
        }
        
        render_image_manager(frm);
    }
});

/* ========================================
MAIN UI
======================================== */

function render_image_manager(frm) {
    let wrapper = frm.fields_dict.custom_image_manager.$wrapper;
    
    wrapper.empty();
    
    wrapper.html(`
        <div class="item-image-manager">
            <div style="margin-bottom:25px">
                <h3>Item Image</h3>
                <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                    <button class="btn btn-primary upload-main">
                        <i class="fa fa-upload"></i> Upload Item Image
                    </button>
                    <button class="btn btn-danger delete-selected-main" style="display: none;">
                        <i class="fa fa-trash"></i> Delete Selected (<span class="selected-count-main">0</span>)
                    </button>
                </div>
                <div class="image-grid main-grid"></div>
            </div>
            
            <div>
                <h3>Item Gallery</h3>
                <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                    <button class="btn btn-primary upload-gallery">
                        <i class="fa fa-upload"></i> Upload Gallery Images
                    </button>
                    <button class="btn btn-danger delete-selected-gallery" style="display: none;">
                        <i class="fa fa-trash"></i> Delete Selected (<span class="selected-count-gallery">0</span>)
                    </button>
                </div>
                <div class="image-grid gallery-grid"></div>
            </div>
        </div>
    `);
    
    render_images(frm);
    
    init_upload(frm, wrapper);
    
    // Initialize selection state
    frm.image_selection = {
        main: new Set(),
        gallery: new Set()
    };
}

/* ========================================
RENDER IMAGES
======================================== */

function render_images(frm) {
    let wrapper = frm.fields_dict.custom_image_manager.$wrapper;
    let images = frm.doc.custom_item_images || [];
    
    let mainGrid = wrapper.find(".main-grid");
    let galleryGrid = wrapper.find(".gallery-grid");
    
    mainGrid.empty();
    galleryGrid.empty();
    
    // Reset selection sets
    frm.image_selection = frm.image_selection || { main: new Set(), gallery: new Set() };
    frm.image_selection.main.clear();
    frm.image_selection.gallery.clear();
    
    images.forEach((img, index) => {
        if (!img.file_url && !img.image_file) {
            return;
        }
        
        let card = image_card(frm, img, index);
        
        if (img.image_type === "Item Gallery") {
            galleryGrid.append(card);
        } else if (img.image_type === "Item Image") {
            mainGrid.append(card);
        }
    });
    
    bind_image_events(frm, wrapper);
    
    // Update delete buttons visibility
    update_delete_buttons(frm, wrapper);
}

/* ========================================
IMAGE CARD
======================================== */

function image_card(frm, img, index) {
    let file_url = img.file_url || img.image_file;
    if (!file_url) {
        return "";
    }
    
    
    let display_name = img.image_name || file_url.split("/").pop();
    let type_class = img.image_type === "Item Image" ? "main" : "gallery";

    let safe_url = frappe.utils.escape_html(file_url);
    let safe_name = frappe.utils.escape_html(display_name);
    
    return `
        <div class="image-card" data-url="${safe_url}" data-idx="${index}" data-type="${type_class}">
            <div class="img-preview">
                <div class="image-checkbox">
                    <input type="checkbox" class="image-select" data-url="${safe_url}" data-type="${type_class}">
                </div>
                <img src="${safe_url}" class="preview-image" 
                     onerror="this.onerror=null; this.src='/assets/frappe/images/ui-states/placeholder-image.png';">
                ${img.image_type === "Item Image" 
                    ? `<span class="image-badge">Item Image</span>` 
                    : ""}
            </div>
            <div class="img-controls">
                <input
                    type="text"
                    class="form-control image-name"
                    value="${safe_name}"
                    placeholder="Image name"
                >
                <button class="btn btn-danger btn-xs delete-image">
                    <i class="fa fa-trash"></i> Delete
                </button>
            </div>
        </div>
    `;
}

/* ========================================
IMAGE EVENTS
======================================== */

function bind_image_events(frm, wrapper) {
    // Preview image
    wrapper.find(".preview-image").off("click").on("click", function () {
        let src = $(this).attr("src");
        let safe_src = frappe.utils.escape_html(src);
        
        frappe.msgprint({
            title: "Image Preview",
            message: `<img src="${safe_src}" style="max-width:100%; max-height:80vh;">`,
            wide: true
        });
    });
    
    // Select checkbox
    wrapper.find(".image-select").off("change").on("change", function() {
        let checkbox = $(this);
        let url = checkbox.data("url");
        let type = checkbox.data("type");
        let isChecked = checkbox.prop("checked");
        
        if (isChecked) {
            frm.image_selection[type].add(url);
        } else {
            frm.image_selection[type].delete(url);
        }
        
        update_delete_buttons(frm, wrapper);
    });
    
    // Delete image
    wrapper.find(".delete-image").off("click").on("click", function () {
        let card = $(this).closest(".image-card");
        let url = card.data("url");
        let idx = card.data("idx");
        let type = card.data("type");
        
        delete_single_image(frm, url, type);
    });
    
    // Rename image
    wrapper.find(".image-name").off("change").on("change", function () {
        let card = $(this).closest(".image-card");
        let url = card.data("url");
        let newName = $(this).val().trim();
        let oldName = $(this).data("original-name");
        
        if (!newName) {
            frappe.msgprint("Image name cannot be empty");
            $(this).val(oldName);
            return;
        }
        
        if (/[<>:"/\\|?*]/.test(newName)) {
            frappe.msgprint("Invalid characters in image name");
            $(this).val(oldName);
            return;
        }
        
        let updated = false;
        (frm.doc.custom_item_images || []).forEach(row => {
            if (row.file_url === url || row.image_file === url) {
                let old = row.image_name;
                row.image_name = newName;
                updated = true;
            }
        });
        
        if (updated) {
            frm.dirty();
            $(this).data("original-name", newName);
            
            frappe.show_alert({
                message: "Image renamed successfully",
                indicator: "green"
            }, 2);
        }
    }).on("focus", function() {
        // Store original value on focus
        let currentVal = $(this).val();
        $(this).data("original-name", currentVal);
    });
    
    // Delete selected buttons
    wrapper.find(".delete-selected-main").off("click").on("click", function() {
        delete_selected_images(frm, "main");
    });
    
    wrapper.find(".delete-selected-gallery").off("click").on("click", function() {
        delete_selected_images(frm, "gallery");
    });
}

/* ========================================
DELETE FUNCTIONS
======================================== */

function update_delete_buttons(frm, wrapper) {
    let mainCount = frm.image_selection.main.size;
    let galleryCount = frm.image_selection.gallery.size;
    
    // Update main delete button
    let mainBtn = wrapper.find(".delete-selected-main");
    if (mainCount > 0) {
        mainBtn.show();
        mainBtn.find(".selected-count-main").text(mainCount);
    } else {
        mainBtn.hide();
    }
    
    // Update gallery delete button
    let galleryBtn = wrapper.find(".delete-selected-gallery");
    if (galleryCount > 0) {
        galleryBtn.show();
        galleryBtn.find(".selected-count-gallery").text(galleryCount);
    } else {
        galleryBtn.hide();
    }
}

function delete_selected_images(frm, type) {
    let typeDisplay = type === "main" ? "Item Image" : "Item Gallery";
    let selectedUrls = Array.from(frm.image_selection[type]);
    
    if (selectedUrls.length === 0) {
        return;
    }
    
    frappe.confirm(
        `Are you sure you want to delete ${selectedUrls.length} selected ${typeDisplay} image(s)?`,
        () => {
            let deletedCount = 0;
            
            selectedUrls.forEach(url => {
                // Tìm row theo file_url hoặc image_file
                let row = (frm.doc.custom_item_images || [])
                    .find(r => r.file_url === url || r.image_file === url);
                
                if (row) {
                    frappe.model.clear_doc(row.doctype, row.name);
                    deletedCount++;
                }
            });
            
            frm.refresh_field("custom_item_images");
            frm.dirty();
            
            render_images(frm);
            
            frappe.show_alert({
                message: `${deletedCount} image(s) deleted successfully`,
                indicator: "green"
            });
        }
    );
}

function delete_single_image(frm, url, type) {
    frappe.confirm("Are you sure you want to delete this image?", () => {
        // find row by file_url or image_file
        let row = (frm.doc.custom_item_images || [])
            .find(r => r.file_url === url || r.image_file === url);
        
        if (!row) {
            frappe.msgprint("Image not found");
            return;
        }
        
        frappe.model.clear_doc(row.doctype, row.name);
        frm.refresh_field("custom_item_images");
        frm.dirty();
        
        // Remove from selection if present
        if (frm.image_selection && frm.image_selection[type]) {
            frm.image_selection[type].delete(url);
        }
        
        render_images(frm);
        
        frappe.show_alert({
            message: "Image deleted successfully",
            indicator: "green"
        });
    });
}

/* ========================================
UPLOAD HANDLER
======================================== */

function init_upload(frm, wrapper) {
    // Upload Item Image
    wrapper.find(".upload-main").off("click").on("click", () => {
        open_uploader(frm, wrapper, "Item Image");
    });
    
    // Upload Gallery Images
    wrapper.find(".upload-gallery").off("click").on("click", () => {
        open_uploader(frm, wrapper, "Item Gallery");
    });
}

/* ========================================
FILE UPLOADER
======================================== */

function open_uploader(frm, wrapper, type) {

    let prefix = null;
    let totalFiles = 0;
    let uploadedCount = 0;

    const uploader = new frappe.ui.FileUploader({

        allow_multiple: true,

        restrictions: {
            allowed_file_types: ["image/*"],
            max_file_size: 10 * 1024 * 1024
        },

        on_success(file) {

            uploadedCount++;

            if (!prefix) {

                let name = file.file_name;
                let dot = name.lastIndexOf(".");
                prefix = dot > 0 ? name.substring(0, dot) : name;
            }

            add_row(frm, file, type, prefix);

            if (uploadedCount === totalFiles) {

                render_images(frm);

                frappe.show_alert({
                    message: `Uploaded ${uploadedCount} image(s)`,
                    indicator: "green"
                });

                uploader.dialog.hide();
            }

            render_images(frm);
        },

        on_error(error) {

            frappe.show_alert({
                message: "Error uploading file",
                indicator: "red"
            });

        }
    });


    // Hook file select
    setTimeout(() => {

        const fileInput = uploader.dialog.$wrapper.find("input[type='file']")[0];
        const uploadBtn = uploader.dialog.$wrapper.find(".btn-primary")[0];

        if (!fileInput) {
            return;
        }

        fileInput.addEventListener("change", function(e) {

            const files = e.target.files;

            totalFiles = files.length;
            uploadedCount = 0;

            if (totalFiles > 10) {

                frappe.msgprint({
                    title: "Upload Limit",
                    message: "Maximum 10 images can be uploaded at once.",
                    indicator: "red"
                });

                if (uploadBtn) {

                    uploadBtn.disabled = true;
                    uploadBtn.style.opacity = "0.5";
                    uploadBtn.style.cursor = "not-allowed";
                }

                return;
            }

            if (uploadBtn) {

                uploadBtn.disabled = false;
                uploadBtn.style.opacity = "1";
                uploadBtn.style.cursor = "pointer";
            }

            frappe.show_alert({
                message: `Selected ${totalFiles} image(s)`,
                indicator: "blue"
            });

        });

    }, 200);

}

/* ========================================
ADD CHILD ROW
======================================== */

function add_row(frm, file, type, prefix) {
    let row = frm.add_child("custom_item_images");
    
    // save URL and file name
    row.file_url = file.file_url;
    row.image_file = file.file_url;  // For backward compatibility
    row.image_type = type;
    
    // count existing images of the same type to determine naming
    let currentCount = (frm.doc.custom_item_images || [])
        .filter(img => img.image_type === type).length;
    
    let fileName = file.file_name;
    let lastDot = fileName.lastIndexOf('.');
    let nameWithoutExt = lastDot > 0 ? fileName.substring(0, lastDot) : fileName;
    let ext = lastDot > 0 ? fileName.substring(lastDot) : '';
    
    if (currentCount === 1) {
        // First image keeps the original name
        row.image_name = fileName;
    } else {
        // Subsequent images: prefix_count.extension
        row.image_name = `${prefix}_${currentCount}${ext}`;
    }
    
    frm.refresh_field("custom_item_images");
    frm.dirty();
}