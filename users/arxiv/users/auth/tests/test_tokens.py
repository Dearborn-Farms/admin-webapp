"""Tests for :mod:`arxiv.users.auth.tokens`."""

from unittest import TestCase
from datetime import datetime

from .. import tokens
from ... import domain
from ...auth import scopes


class TestEncodeDecode(TestCase):
    """Tests for :func:`tokens.encode` and :func:`tokens.decode`."""

    def test_encode_session(self):
        """Encode a typical user session."""
        session = domain.Session(
            session_id='asdf1234',
            start_time=datetime.now(), end_time=datetime.now(),
            user=domain.User(
                user_id='12345',
                email='foo@bar.com',
                username='emanresu',
                name=domain.UserFullName('First', 'Last', 'Lastest'),
                profile=domain.UserProfile(
                    affiliation='FSU',
                    rank=3,
                    country='us',
                    default_category=domain.Category('astro-ph', 'CO'),
                    submission_groups=['grp_physics']
                )
            ),
            authorizations=domain.Authorizations(
                scopes=[scopes.VIEW_SUBMISSION, scopes.CREATE_SUBMISSION],
                endorsements=[domain.Category('astro-ph', 'CO')]
            )
        )
        secret = 'foosecret'
        token = tokens.encode(session, secret)

        data = tokens.decode(token, secret)
        self.assertEqual(session, data)

    def test_mismatched_secrets(self):
        """Secret used to encode is not the same as the one used to decode."""
        session = domain.Session(
            session_id='asdf1234',
            start_time=datetime.now(), end_time=datetime.now(),
            user=domain.User(
                user_id='12345',
                email='foo@bar.com',
                username='emanresu',
                name=domain.UserFullName('First', 'Last', 'Lastest'),
                profile=domain.UserProfile(
                    affiliation='FSU',
                    rank=3,
                    country='us',
                    default_category=domain.Category('astro-ph', 'CO'),
                    submission_groups=['grp_physics']
                )
            ),
            authorizations=domain.Authorizations(
                scopes=[scopes.VIEW_SUBMISSION, scopes.CREATE_SUBMISSION],
                endorsements=[domain.Category('astro-ph', 'CO')]
            )
        )
        secret = 'foosecret'
        token = tokens.encode(session, secret)

        with self.assertRaises(tokens.exceptions.InvalidToken):
            tokens.decode(token, 'not the secret')
