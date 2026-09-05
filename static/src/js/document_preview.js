/** @odoo-module **/

import { onMounted, onWillUnmount } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);

        this._documentPreviewClickHandler = null;

        onMounted(() => {
            this._documentPreviewClickHandler = (event) => {

                const image = event.target.closest(
                    ".o_document_preview img"
                );

                if (!image) {
                    return;
                }

                if (!image.src) {
                    return;
                }

                this._openDocumentImage(image.src);
            };

            this.el.addEventListener(
                "click",
                this._documentPreviewClickHandler
            );
        });

        onWillUnmount(() => {
            if (this._documentPreviewClickHandler) {
                this.el.removeEventListener(
                    "click",
                    this._documentPreviewClickHandler
                );
            }
        });
    },

    _openDocumentImage(src) {

        const overlay = document.createElement("div");

        overlay.className = "o_document_image_overlay";

        overlay.innerHTML = `
            <div class="o_document_image_container">

                <button
                    type="button"
                    class="o_document_image_close"
                    aria-label="Cerrar"
                >
                    ×
                </button>

                <img
                    src="${src}"
                    class="o_document_image_large"
                />

            </div>
        `;

        document.body.appendChild(overlay);

        const close = () => {
            overlay.remove();
        };

        overlay
            .querySelector(".o_document_image_close")
            .addEventListener("click", close);

        overlay.addEventListener("click", (event) => {
            if (event.target === overlay) {
                close();
            }
        });

        document.addEventListener(
            "keydown",
            function escapeHandler(event) {

                if (event.key === "Escape") {
                    close();

                    document.removeEventListener(
                        "keydown",
                        escapeHandler
                    );
                }
            }
        );
    },
});