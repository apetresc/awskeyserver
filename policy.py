class PolicyHandler:

    def handle(self, request):
        raise 'Abstract method, policy handlers must override'


class PolicyResponseCode:
    ACCEPT=1
    CHALLENGE=2
    DENY=3

