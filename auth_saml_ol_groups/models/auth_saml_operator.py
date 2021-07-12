# © 2019 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, models


class AuthSamlProviderOperator(models.AbstractModel):
    """Define operators for group mappings"""

    _name = "auth.saml.provider.operator"
    _description = "Auth SAML Provider Operator"

    @api.model
    def operators(self):
        """Return names of function to call on this model as operator"""
        return ('contains', 'equals')

    def contains(self, attrs, mapping):
        values = attrs.get(mapping.saml_attribute)
        if values:
            for value in values:
                if mapping.value in value:
                    return True
        return False

    def equals(self, attrs, mapping):
        values = attrs.get(mapping.saml_attribute)
        if values:
            for value in values:
                if mapping.value == value:
                    return True
        return False
