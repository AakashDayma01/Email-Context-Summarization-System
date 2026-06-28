from django.core.management.base import BaseCommand
from apps.firms.models import Firm
from apps.accounts.models import Account
from apps.clients.models import Client
from apps.emails.models import Email
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Seed mock email data"

    def handle(self, *args, **kwargs):

        firms = [
            "Ascend CPA",
            "Elite Tax Consultants",
        ]

        for firm_name in firms:
            firm, created = Firm.objects.get_or_create(
                name=firm_name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Firm created: {firm.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Firm already exists: {firm.name}"
                    )
                )
        users = [
            {
                "username": "ascend_admin",
                "email": "admin@ascend.com",
                "password": "Admin@123",
                "role": Account.Role.ADMIN,
                "firm": "Ascend CPA",
                "first_name": "Rahul",
                "last_name": "Sharma",
            },
            {
                "username": "john",
                "email": "john@ascend.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Ascend CPA",
                "first_name": "John",
                "last_name": "Doe",
            },
            {
                "username": "elite_admin",
                "email": "admin@elite.com",
                "password": "Admin@123",
                "role": Account.Role.ADMIN,
                "firm": "Elite Tax Consultants",
                "first_name": "Priya",
                "last_name": "Patel",
            },
            {
                "username": "alice",
                "email": "alice@elite.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Elite Tax Consultants",
                "first_name": "Alice",
                "last_name": "Johnson",
            },
        ]

        for user_data in users:

            firm = Firm.objects.get(name=user_data["firm"])

            user, created = Account.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "role": user_data["role"],
                    "firm": firm,
                },
            )

            if created:
                user.set_password(user_data["password"])
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {user.email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {user.email}"
                    )
                )

        clients = [
            {
                "firm": "Ascend CPA",
                "name": "ABC Pvt Ltd",
                "email": "contact@abcpvt.com",
                "phone": "9876543210",
            },
            {
                "firm": "Ascend CPA",
                "name": "XYZ Technologies",
                "email": "info@xyztech.com",
                "phone": "9876543211",
            },
            {
                "firm": "Elite Tax Consultants",
                "name": "Bright Solutions",
                "email": "admin@brightsolutions.com",
                "phone": "9876543212",
            },
            {
                "firm": "Elite Tax Consultants",
                "name": "Green Enterprises",
                "email": "contact@greenenterprises.com",
                "phone": "9876543213",
            },
        ]

        for client_data in clients:

            firm = Firm.objects.get(name=client_data["firm"])

            client, created = Client.objects.get_or_create(
                email=client_data["email"],
                defaults={
                    "firm": firm,
                    "name": client_data["name"],
                    "phone": client_data["phone"],
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created client: {client.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Client already exists: {client.name}"
                    )
                )

        emails = [
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Request for Form-16",
                "body": "Please upload your Form-16 for FY 2025-26.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "admin@ascend.com",
                "subject": "Bank Statements",
                "body": "Kindly share your bank statements from April to March.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Investment Proof",
                "body": "We are still waiting for your investment proof documents.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "john@ascend.com",
                "subject": "GST Documents",
                "body": "Please send the GST returns for the last quarter.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "admin@ascend.com",
                "subject": "Acknowledgement",
                "body": "Thank you for sharing the GST documents.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "alice@elite.com",
                "subject": "Salary Slips",
                "body": "Please upload salary slips for all directors.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "admin@elite.com",
                "subject": "Reminder",
                "body": "This is a reminder to submit pending salary slips.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "alice@elite.com",
                "subject": "ITR Documents",
                "body": "Please upload all documents required for ITR filing.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "admin@elite.com",
                "subject": "Verification",
                "body": "We have received your documents. Verification is in progress.",
            },
        ]

        for index, email_data in enumerate(emails):
            client = Client.objects.get(name=email_data["client"])

            accountant = Account.objects.get(email=email_data["accountant"])

            email, created = Email.objects.get_or_create(
                client=client,
                accountant=accountant,
                subject=email_data["subject"],
                defaults={
                    "body": email_data["body"],
                    "sent_at": timezone.now() - timedelta(days=len(emails) - index),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Email created: {email.subject}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Email already exists: {email.subject}"
                    )
                )
        self.stdout.write(
            self.style.SUCCESS("Firm seeding completed.")
        )