from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient


# Test for customer user
class UsersManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.client = APIClient()
        self.admin = self.User.objects.create_superuser(
            email='admin_1@mail.com',
            username='admin_1',
            password='admin_1'
        )
        self.admin.save()
        self.agent = self.User.objects.create_agent(
            email='agent_1@mail.com',
            username='agent_1',
            password='agent_1'
        )
        self.agent.save()
        self.customer = self.User.objects.create_customer(
            email='customer_1@mail.com',
            username='customer_1',
            password='customer_1'
        )
        self.customer.save()
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'admin_1@mail.com',
            'password': 'admin_1'
        })
        self.token_admin = response.json()['token']
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'agent_1@mail.com',
            'password': 'agent_1'
        })
        self.token_agent = response.json()['token']
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'customer_1@mail.com',
            'password': 'customer_1'
        })
        self.token_customer = response.json()['token']

    def test_create_user(self):
        user = self.User.objects.create_user(
            email='normal@user.com', username='normal', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.username, 'normal')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='', username='', password="foo")

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            email='super@user.com', username='super', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'super')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNotNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com',
                username='super',
                password='foo',
                is_superuser=False
            )

    def test_registerAgent(self):
        res = self.client.post(reverse_lazy('user:agent_register'), {
            'username': 'agent_3',
            'email': 'agent_3@mail.com',
            'password': 'agent_3',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['user_type'], 'agent')
        self.assertEqual(self.User.agentmanager.count(), 2)

    def test_registerCustomer(self):
        res = self.client.post(reverse_lazy('user:customer_register'), {
            'username': 'customer_3',
            'email': 'customer_3@mail.com',
            'password': 'customer_3',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['user_type'], 'customer')
        self.assertEqual(self.User.customermanager.count(), 2)

    def test_get_user_list(self):
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 2)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_customer}")
        res = self.client.get(reverse_lazy('user:user_list'))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_view(self):
        admin_id = self.admin.id
        agent_id = self.agent.id
        customer_id = self.customer.id
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': agent_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': customer_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': agent_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': customer_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_customer}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': agent_id}))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': customer_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_edit(self):
        admin_id = self.admin.id
        agent_id = self.agent.id
        customer_id = self.customer.id

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_customer}")
        res = self.client.get(reverse_lazy(
            'user:user_view', kwargs={'id': admin_id}))
