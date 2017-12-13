from subprocess import Popen, PIPE, STDOUT


class Certificate(object):
    def __init__(self):
        # attribution for cert
        pass

    def set_cert(self):
        pass

    def create(self):
        pass

    def revoke(self):
        pass

    # convert the certificate to string
    @staticmethod
    def get_cert_id_and_status_and_public(cert_encoded_str):
        p = Popen(['java', '-jar', './CertToolKit.jar', '-c', cert_encoded_str], stdout=PIPE, stderr=STDOUT)
        cert_id, is_valid, public_key = p.stdout.readline()
        return cert_id, is_valid, public_key

