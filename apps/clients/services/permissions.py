from apps.clients.models import Client


def get_clients_for_user(user):
    """
    Central permission layer for clients access
    """

    # 👑 Super Admin → sees everything
    if user.is_superuser:
        return Client.objects.all()

    # 🏢 Firm-based access
    if user.firm:
        return Client.objects.filter(firm=user.firm)

    return Client.objects.none()