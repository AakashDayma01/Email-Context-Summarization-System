from apps.emails.models import Email


def get_emails_for_user(user, client=None):
    """
    Central permission layer for email access
    """

    # 👑 SUPER ADMIN
    if user.is_superuser:
        if client:
            return Email.objects.filter(client=client)
        return Email.objects.all()

    # 🏢 FIRM BASED ACCESS
    if user.firm:
        qs = Email.objects.filter(client__firm=user.firm)

        if client:
            qs = qs.filter(client=client)

        return qs

    return Email.objects.none()