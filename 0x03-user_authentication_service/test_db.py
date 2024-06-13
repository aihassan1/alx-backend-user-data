import unittest
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.user1 = self.db.add_user(
            email="user1@example.com", hashed_password="password1"
        )
        self.user2 = self.db.add_user(
            email="user2@example.com", hashed_password="password2"
        )

    def tearDown(self):
        self.db._session.rollback()

    def test_find_user_by_existing_email(self):
        user = self.db.find_user_by(email="user1@example.com")
        self.assertEqual(user, self.user1)

    def test_find_user_by_non_existing_email(self):
        with self.assertRaises(NoResultFound):
            self.db.find_user_by(email="nonexisting@example.com")

    def test_find_user_by_invalid_key(self):
        with self.assertRaises(InvalidRequestError):
            self.db.find_user_by(invalid_key="value")


if __name__ == "__main__":
    unittest.main()
