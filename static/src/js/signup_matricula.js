/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SindicatoSignupMatricula = publicWidget.Widget.extend({

    selector: '.oe_signup_form',

    events: {
        'blur input[name="matricula"]': '_onMatriculaBlur',
    },

    start: function () {

        console.log("SINDICATO: formulario signup encontrado");

        console.log(
            "SINDICATO: campo matrícula:",
            this.el.querySelector('input[name="matricula"]')
        );

        return this._super.apply(this, arguments);
    },

    _onMatriculaBlur: async function (ev) {

        console.log("SINDICATO: BLUR matrícula");

        const input = ev.currentTarget;
        const matricula = input.value.trim();

        console.log(
            "SINDICATO: matrícula capturada:",
            matricula
        );

        const feedback = this.el.querySelector('#matricula_feedback');

        if (!matricula) {

            this._setName('');

            if (feedback) {
                feedback.innerHTML = '';
            }

            return;
        }


        try {

            console.log(
                "SINDICATO: consultando matrícula en servidor..."
            );

            /*
             * Usamos fetch directamente para evitar
             * problemas con la API RPC de Odoo 18.
             */

            const response = await fetch(
                '/sindicato/buscar_matricula',
                {
                    method: 'POST',

                    headers: {
                        'Content-Type': 'application/json',
                    },

                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {
                            matricula: matricula
                        },
                        id: Date.now()
                    })
                }
            );

            console.log(
                "SINDICATO: HTTP status:",
                response.status
            );

            const data = await response.json();

            console.log(
                "SINDICATO: respuesta completa:",
                data
            );

            /*
             * Odoo puede devolver el resultado
             * dentro de result.
             */

            const result = data.result || data;

            console.log(
                "SINDICATO: resultado:",
                result
            );

            if (result.encontrado) {

                console.log(
                    "SINDICATO: MATRÍCULA ENCONTRADA"
                );

                console.log(
                    "Nombre:",
                    result.name
                );

                console.log(
                    "Categoría:",
                    result.function
                );

                this._setName(
                    result.name || ''
                );

            } else {

                console.log(
                    "SINDICATO: MATRÍCULA NO ENCONTRADA"
                );

                this._setName('');

            }

        } catch (error) {

            console.error(
                "SINDICATO: ERROR buscando matrícula:",
                error
            );

        }
    },

    _setName: function (name) {

        const nameInput =
            this.el.querySelector('input[name="name"]');

        console.log(
            "SINDICATO: campo name:",
            nameInput
        );

        if (!nameInput) {

            console.error(
                "SINDICATO: NO se encontró input[name='name']"
            );

            return;
        }

        nameInput.value = name;

        nameInput.dispatchEvent(
            new Event('input', {
                bubbles: true
            })
        );

        nameInput.dispatchEvent(
            new Event('change', {
                bubbles: true
            })
        );

        console.log(
            "SINDICATO: nombre colocado:",
            name
        );
    },
});