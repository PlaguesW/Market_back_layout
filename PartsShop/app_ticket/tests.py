from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_account.models import User
from app_ticket.models import Ticket, TicketMessage
from datetime import datetime, timedelta


# Tests for Ticket and TicketMessage
class TicketModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')

    def test_create_ticket(self):
        ticket = Ticket.objects.create(
            owner=self.user,
            category='T',
            subject='Technical Issue',
            open_date=datetime.now(),
            is_open=True,
        )
        self.assertEqual(ticket.owner, self.user)
        self.assertEqual(ticket.category, 'T')
        self.assertTrue(ticket.is_open)

    def test_create_ticket_message(self):
        ticket = Ticket.objects.create(
            owner=self.user,
            category='T',
            subject='Technical Issue',
            open_date=datetime.now(),
            is_open=True,
        )
        message = TicketMessage.objects.create(
            ticket=ticket,
            message="This is a test message.",
            register_date=datetime.now(),
        )
        self.assertEqual(message.ticket, ticket)
        self.assertEqual(message.message, "This is a test message.")


# Tests for views 
class TicketViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_ticket_view(self):
        data = {
            "category": "T",
            "subject": "Technical Issue",
        }
        response = self.client.post(reverse('tickets:create_ticket'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'ticket created.')

    def test_create_ticket_message_view(self):
        ticket = Ticket.objects.create(
            owner=self.user,
            category='T',
            subject='Technical Issue',
            open_date=datetime.now(),
            is_open=True,
        )
        data = {
            "message": "This is a reply message.",
        }
        response = self.client.post(reverse('tickets:create_ticket_massage', args=[ticket.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'ticket message created.')

    def test_create_ticket_message_closed_ticket(self):
        ticket = Ticket.objects.create(
            owner=self.user,
            category='T',
            subject='Technical Issue',
            open_date=datetime.now(),
            is_open=False,
        )
        data = {
            "message": "This is a reply message.",
        }
        response = self.client.post(reverse('tickets:create_ticket_massage', args=[ticket.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'this ticket is already closed, open a new')

    def test_list_tickets_view(self):
        Ticket.objects.create(owner=self.user, category='T', subject='Technical Issue', open_date=datetime.now())
        Ticket.objects.create(owner=self.user, category='F', subject='Financial Issue', open_date=datetime.now())
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_ticket_messages_view(self):
        ticket = Ticket.objects.create(owner=self.user, category='T', subject='Technical Issue', open_date=datetime.now())
        TicketMessage.objects.create(ticket=ticket, message="Message 1", register_date=datetime.now())
        TicketMessage.objects.create(ticket=ticket, message="Message 2", register_date=datetime.now())
        response = self.client.get(reverse('tickets:ticket_massage_list', args=[ticket.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)