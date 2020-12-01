# © 2019 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models
from odoo.exceptions import AccessDenied
_logger = logging.getLogger(__name__)

class ResUser(models.Model):
    """Add SAML login capabilities to Odoo users.
    """

    _inherit = 'res.users'

    @api.multi
    def get_saml_data(self, provider, server):
        self.write({
            'groups_id': provider._get_user_groups(self, server),
        })
        return super(ResUser, self).get_saml_data(provider, server)