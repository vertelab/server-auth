##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2020 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from odoo import models, api, fields, _

_logger = logging.getLogger(__name__)


class AuthSamlProvider(models.Model):
    _inherit = 'auth.saml.provider'

    create_user = fields.Boolean(string='Create User')
    name_attribute = fields.Char(
        default='subject.nameId'
    )

    @api.multi
    def get_saml_user(self, server):
        user = super(AuthSamlProvider, self).get_saml_user(server)
        if not user and self.create_user:
            user = self._create_saml_user(server)
        return user

    @api.multi
    def _get_saml_user_values(self, server):
        """ Get the attributes for a new SAML user.
        """
        login = name = None
        if self.matching_attribute == 'subject.nameId':
            login = server.get_nameid()
        else:
            login = server.get_attribute(self.matching_attribute)
        if type(login) == list:
            login = login[0]
        if self.name_attribute:
            name = server.get_attribute(self.name_attribute)
        if type(name) == list:
            name = name[0]
        if self.env['res.users'].search_count(['|', ('login', '=', login), ('saml_uid', '=', login)]):
            raise Warning(_("Username is already taken. Please contact your administrator."))
        values = {
            'login': login,
            'name': name or login,
            'saml_uid': login,
            'saml_provider_id': self.id,
            'active': True,
        }
        return values

    @api.multi
    def _create_saml_user(self, server):
        """ Create a new SAML user.
        """
        template_user = self.env.ref('auth_saml_ol_create_user.template_saml_user_id')
        if not template_user.exists():
            raise ValueError(_('Signup: invalid template user'))
        values = self._get_saml_user_values(server)
        _logger.debug('SAML create user values: %s' % values)
        if not values.get('login'):
            raise ValueError(_('Signup: no login given for new user'))
        if not values.get('partner_id') and not values.get('name'):
            raise ValueError(_('Signup: no name or partner given for new user'))
        user = template_user.with_context(no_reset_password=True).copy(values)
        self.env.cr.commit()
        return user
