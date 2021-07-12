# © 2019 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)


class AuthSamlProvider(models.Model):
    _inherit = 'auth.saml.provider'

    group_mapping_ids = fields.One2many(
        'auth.saml.provider.group_mapping',
        'saml_id',
        'Group mappings',
        help='Define how Odoo groups are assigned to SAML users',
    )
    only_saml_groups = fields.Boolean(
        'Only SAML groups',
        default=False,
        help=(
            'If this is checked, manual changes to group membership are '
            'undone on every login (so Odoo groups are synchronous on login'
            'with SAML groups). If not, manually added groups are preserved.'
        ),
    )

    def _get_user_groups(self, user, server):
        groups = []
        to_remove = set()
        attrs = server.get_attributes()

        if self.only_saml_groups:
            _logger.debug('deleting all groups from user %d', user_id)
            groups.append((5, False, False))

        for mapping in self.group_mapping_ids:
            operator = self.env['auth.saml.provider.operator']
            operator = getattr(operator, mapping.operator)
            _logger.debug('checking mapping %s', mapping)
            if operator(attrs, mapping):
                _logger.debug(
                    'adding user %d to group %s', user, mapping.group_id.name,
                )
                groups.append((4, mapping.group_id.id, False))
            elif mapping.autoremove and (mapping.group_id in user.groups_id):
                to_remove.add(mapping.group_id.id)
        for group_id in to_remove:
            groups.append((3, group_id))
        return groups
