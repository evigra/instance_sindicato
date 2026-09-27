from lxml import etree

from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(
            view_id=view_id,
            view_type=view_type,
            **options
        )

        if view_type != "form":
            return result

        arch = etree.fromstring(result["arch"])

        # El campo dinámico de Tipo de usuario
        field_name = "sel_groups_1_10_11"

        # Si ya existe, no lo agregamos otra vez
        if arch.xpath(f"//field[@name='{field_name}']"):
            return result

        # Lo colocamos en la sección de permisos
        groups = arch.xpath("//page[@name='access_rights']/group")

        if groups:
            field = etree.Element("field")
            field.set("name", field_name)
            field.set("widget", "radio")

            groups[0].append(field)

            result["arch"] = etree.tostring(
                arch,
                encoding="unicode"
            )

        return result