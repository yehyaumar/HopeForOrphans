import hashlib


class PAYU(object):
    def generate_hash(self, hash_string):
        hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return hash

    def initiate_transaction(self, merchant_key, payu_salt, payu_key, success_url, failure_url, mode,  data):
        self.test_url = "https://sandboxsecure.payu.in/_payment"
        self.secure_url = 'https://secure.payu.in/_payment'
        self.base_url = self.test_url if mode == 'TEST' else self.secure_url
        self.mechent_key = merchant_key
        self.salt = payu_salt
        self.key = payu_key
        self.success_url = success_url
        self.failure_url = failure_url

        data['key'] = self.mechent_key
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string += str(data[i])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += self.salt
        # Generate Hash
        hashh = self.generate_hash(hash_string)

        data['merchant_key'] = self.mechent_key
        data['surl'] = self.success_url
        data['furl'] = self.failure_url
        data['hashh'] = hashh
        data['hash_string'] = hash_string
        data['service_provider'] = 'payu_paisa'
        data['action'] = self.base_url
        return data

    def check_hash(self, data):
        response = {}
        for item in data:
            data[item] = data[item][0]
        status = data.get("status")
        firstname = data.get("firstname")
        amount = data.get("amount")
        txnid = data.get("txnid")
        posted_hash = data.get("hash")
        key = data.get("key")
        productinfo = data.get("productinfo")
        email = data.get("email")
        if data.get('additionalCharges'):
            additional_charges = data["additionalCharges"]
            ret_hash_seq = additional_charges + '|' + self.salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        else:
            ret_hash_seq = self.salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        hashh = hashlib.sha512(ret_hash_seq.encode('utf-8')).hexdigest().lower()
        response['data'] = data
        response['hash_string'] = ret_hash_seq
        response['generated_hash'] = hashh
        response['recived_hash'] = posted_hash
        response['verify_hash'] = hashh == posted_hash
        return response