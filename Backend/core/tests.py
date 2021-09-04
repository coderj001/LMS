from datetime import datetime

from core.models import Loan
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient


class LoansManagersTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.Loan = Loan
        self.client = APIClient()
        # create admin user
        self.admin = self.User.objects.create_superuser(
            email='admin_1@mail.com',
            username='admin_1',
            password='admin_1'
        )
        self.admin.save()
        # create agent user
        self.agent = self.User.objects.create_agent(
            email='agent_1@mail.com',
            username='agent_1',
            password='agent_1'
        )
        self.agent.save()
        # create customer user
        self.customer = self.User.objects.create_customer(
            email='customer_1@mail.com',
            username='customer_1',
            password='customer_1'
        )
        self.customer.save()
        # admin token
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'admin_1@mail.com',
            'password': 'admin_1'
        })
        self.token_admin = response.json()['token']
        # agent token
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'agent_1@mail.com',
            'password': 'agent_1'
        })
        self.token_agent = response.json()['token']
        # customer token
        response = self.client.post(reverse_lazy('user:user_login'), {
            'email': 'customer_1@mail.com',
            'password': 'customer_1'
        })
        self.token_customer = response.json()['token']

    def test_create_loan(self):
        """
        test case for loan model
        """
        loan = self.Loan.objects.create(
            amount=10000,
            interest_rate=5.3,
            start_date=datetime(2021, 10, 11, 0, 0, 0),
            agent=self.agent,
            customer=self.customer
        )
        self.assertEqual(loan.amount, 10000)
        self.assertEqual(loan.interest_rate, 5.3)
        self.assertEqual(loan.emi, None)
        self.assertEqual(loan.agent, self.agent)
        self.assertEqual(loan.customer, self.customer)
        loan.duration = 24
        loan.save()
        self.assertEqual(loan.duration, 24)
        self.assertEqual(loan.emi, 440.06)

        with self.assertRaises(TypeError):
            self.Loan.objects.create(
                interest_rate=5.3,
                start_date=datetime(2021, 10, 11, 0, 0, 0),
                duration=24,
            )

    def test_request_loan(self):
        """
        test case for request loan
        """
        # None type user
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        # can't request loan
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # admin type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        # can't request loan
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # customer type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_customer}")
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        # can't request loan
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # agent type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        # can request loan
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['amount'], 10000)
        self.assertEqual(res.json()['duration'], 15)
        self.assertEqual(res.json()['interest_rate'], 5)
        self.assertEqual(res.json()['start_date'], '2021-11-10T00:00:00Z')
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_loan(self):
        """
        test case for edit loan view
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.put(reverse_lazy('core:edit_loan', kwargs={'id': res.json()['id']}), {
            'amount': '15000',
            'start_date': '2021/11/10',
            'duration': '12',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['amount'], 15000)
        self.assertEqual(res.json()['duration'], 12)
        self.assertEqual(res.json()['interest_rate'], 5)
        self.assertEqual(res.json()['start_date'], '2021-11-10T00:00:00Z')

    def test_list_loan(self):
        """
        test case of list of loan with filter
        """
        # create 3 different loan
        self.Loan.objects.create(
            amount=15500,
            start_date=datetime(2021, 11, 10),
            duration=4,
            interest_rate=6,
            agent=self.agent,
            customer=self.customer,
        ).save()
        self.Loan.objects.create(
            amount=15500,
            start_date=datetime(2021, 11, 10),
            duration=4,
            interest_rate=6,
            agent=self.agent,
            customer=self.customer,
            status='rejected',
        ).save()
        self.Loan.objects.create(
            amount=15500,
            start_date=datetime(2021, 11, 10),
            duration=4,
            interest_rate=6,
            agent=self.agent,
            customer=self.customer,
            status='approved',
        ).save()

        # admin type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.get(reverse_lazy('core:list_loan'))  # without filter
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 3)

        # filter by status

        res = self.client.get(reverse_lazy(
            'core:list_loan'), {'status': 'new'})  # with filter -new
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

        res = self.client.get(reverse_lazy(
            'core:list_loan'), {'status': 'rejected'})  # with filter - rejected

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

        res = self.client.get(reverse_lazy(
            'core:list_loan'), {'status': 'approved'})  # with filter - approved
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

        # filter by created_at

        res = self.client.get(reverse_lazy(
            'core:list_loan'), {'created_at': datetime.today().strftime("%Y/%m/%d")})  # with filter - created_at
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 3)

        res = self.client.get(reverse_lazy(
            'core:list_loan'), {'updated_at': datetime.today().strftime("%Y/%m/%d")})  # with filter - updated_at
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 3)

        # agent type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.get(reverse_lazy('core:list_loan'))  # without filter
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 3)

        # customer type user
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_customer}")
        res = self.client.get(reverse_lazy('core:list_loan'))  # without filter
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 3)

    def test_request_loan_approved(self):
        """
        test case for approved loan can be done by admin type user.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        id = res.json()['id']
        res = self.client.post(reverse_lazy(
            'core:approved_loan', kwargs={'id': id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.post(reverse_lazy(
            'core:approved_loan', kwargs={'id': id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_request_loan_rejected(self):
        """
        test case for rejected loan can be done by admin type user.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_agent}")
        res = self.client.post(reverse_lazy('core:create_loan'), {
            'amount': '10000',
            'start_date': '2021/11/10',
            'duration': '15',
            'interest_rate': '5',
            'customer': 'customer_1',
            'agent': 'agent_1',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        id = res.json()['id']
        res = self.client.post(reverse_lazy(
            'core:rejected_loan', kwargs={'id': id}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token_admin}")
        res = self.client.post(reverse_lazy(
            'core:rejected_loan', kwargs={'id': id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
