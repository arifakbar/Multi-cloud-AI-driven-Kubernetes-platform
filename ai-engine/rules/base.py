class Violation:
    def __init__(self, resource, rule, severity, message):
        self.resource = resource
        self.rule = rule
        self.severity = severity
        self.message = message

    def to_dict(self):
        return {
            "resource": self.resource,
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
        }