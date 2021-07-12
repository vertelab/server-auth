# © 2019 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo.exceptions import AccessDenied

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResUser(models.Model):
    """Add SAML login capabilities to Odoo users.
    """

    _inherit = 'res.users'

    def get_saml_data(self, provider, server):
        self.write({
            'groups_id': provider._get_user_groups(self, server),
        })
        return super(ResUser, self).get_saml_data(provider, server)
