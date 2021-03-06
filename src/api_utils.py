import requests
import json
from ConfigParser import SafeConfigParser
import time
import os
import sys
import random
import inspect
import filecmp


class Config:
    def __init__(self):
        """Creating object of SafeConfigParser() class to get access to it's methods and attributes"""
        self.parser = SafeConfigParser()
        """Checking if config file exists"""
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            print('No config.ini found under root folder.')
            # Shut down Python
            sys.exit()
        # Creating variables with values from config.ini
        self.domain = self.parser.get('Server', 'domain')
        self.admin_login = self.parser.get('Server', 'admin')
        self.password = self.parser.get('Server', 'password')
        self.test_path = self.parser.get('Server', 'testpath')
        self.puser = self.parser.get('Server', 'puser')
        self.test_files = './test_files'


# Define class for sexy looking response object
class Response:
    def __init__(self):
        self.http_code = None
        self.body = dict()
        self.headers = dict()


# Define class to store all methods we need for framework
class Calls:
    def __init__(self):
        # Creating object of class Config()
        self.config = Config()
        # Creating variable with string to return it in case there is no json
        self.no_json = 'NoJSON'

    def create_folder(self, folder_name, domain=None, username=None, password=None,
                      content_type=None, accept=None, method=None, test_path=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/fs'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['action'] = 'add_folder'
        data = json.dumps(data)
        # Request method returning server response to r
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            data=data,
            method=method
        )

        # Fist: Trying to parse json and convert it to Pythonic dict.
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            # If parsing failed then check, maybe method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            # And finally return no_json string to json_resp variable
            else:
                json_resp = self.no_json
        # Putting processed r.content into r.json
        r.json = json_resp
        # Creating object of class Response()
        self.nice_print_out(call_name='Create Folder', r=r, caller=inspect.stack()[1][3])
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        print('\n' + str(response.http_code))
        return response

    def delete_folder(self, folder_name, domain=None, username=None, password=None,
                      content_type=None, accept=None, method=None, test_path=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'DELETE'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/fs'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            method=method
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'OPTIONS':
                json_resp = r.content
            else:
                json_resp = self.no_json

        r.json = json_resp
        self.nice_print_out(call_name='Delete Folder', r=r, caller=inspect.stack()[1][3])
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        return response

    def set_perms(self, folder_name, permission, user, domain=None, username=None, password=None,
                  content_type=None, accept=None, method=None, test_path=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/perms/folder'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['permission'] = permission
        data['users'] = list()
        data['users'].append(user)
        data = json.dumps(data)
        # Request method returning server response to r
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            data=data,
            method=method
        )

        # Fist: Trying to parse json and convert it to Pythonic dict.
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            # If parsing failed then check, maybe method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            # And finally return no_json string to json_resp variable
            else:
                json_resp = self.no_json
        # Putting processed r.content into r.json
        r.json = json_resp
        # Creating object of class Response()
        self.nice_print_out(call_name='Set Perms', r=r, caller=inspect.stack()[1][3])
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        return response

    def upload(self, filename, path=None, domain=None, method=None, username=None, password=None):
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if path is None:
            path = self.config.test_path
        if domain is None:
            domain = self.config.domain

        url = domain + '/public-api/v1/fs-content' + path + '/' + filename
        local_file_path = '%s/%s' % (self.config.test_files, filename)
        r = requests.request(
            url=url,
            data=open(local_file_path, 'rb'),
            method=method,
            auth=(username, password)
        )
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            # If parsing failed then check, maybe method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            # And finally return no_json string to json_resp variable
            else:
                json_resp = self.no_json
        # Putting processed r.content into r.json
        r.json = json_resp
        # Creating object of class Response()
        self.nice_print_out(call_name='Upload File', r=r, caller=inspect.stack()[1][3])
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        return response

    def download(self, filename=None, path=None, domain=None, username=None, password=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if path is None:
            path = self.config.test_path

        url = domain + '/public-api/v1/fs-content' + path + filename

        r = requests.get(
            url=url,
            stream=True,
            auth=(username, password)
        )

        try:
            body = json.loads(r.content)
        except ValueError:
            file1 = self.gen_random_name()
            if not os.path.isdir(self.config.test_files):
                os.mkdir(self.config.test_files)
            with open(self.config.test_files + '/' + file1, 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            body = file1
        r.json = body
        self.nice_print_out(call_name='Download File', r=r, caller=inspect.stack()[1][3])
        response = Response()
        response.http_code = r.status_code
        response.body = body
        response.headers = r.headers
        return response

    @staticmethod
    def nice_print_out(call_name, r, caller):
        header_string = ''
        for key in r.request.headers:
            header_string += '-H "%s: %s" ' % (key, r.request.headers[key])
        print('\n*TestCase Name: %s, API Call: %s*' % (caller, call_name))
        if r.request.body:
            print('Curl is:\n curl %s "%s" -d \'%s\' -X %s' % (header_string, r.request.url, r.request.body,
                                                               r.request.method))
        else:
            print('Curl is:\n curl %s "%s" -X %s' % (header_string, r.request.url, r.request.method))
        print('\nResponse status code: %s' % r.status_code)
        if r.json != 'NoJSON':
            try:
                print('\nResponse body:\n %s' % json.dumps(r.json, indent=2))
            except TypeError:
                print('\nResponse body:\n %s' % r.json)
        else:
            print('\nNo body in the response.')

    # Defining static(nothing to do with parent class) method, which generates random
    @staticmethod
    def gen_random_name():
        return 'dynamic_name_%s%s' % (str(random.randint(10000, 99999)), str(time.time()).replace('.', ''))

    def gen_file(self, file_name=None, block_size=None, num_blocks=None):
        if block_size is None:
            block_size = 200
        if num_blocks is None:
            num_blocks = 1
        if file_name is None:
            file_name = 'test_filename_%s.txt' % str(time.time()).replace('.', '')
        file_path = '%s/%s' % (self.config.test_files, file_name)
        # Check if there is a directory we need, if not then - create
        if not os.path.exists(self.config.test_files):
                cmd = 'mkdir %s' % self.config.test_files
                os.system(cmd)
        # Check if there is a file we need, if not then - generate
        if not os.path.isfile('%s/%s' % (self.config.test_files, file_name)):
            # Linux command to generate file(ZAPOMNIT!!!!111')
            cmd = "dd if=/dev/urandom of='%s' bs=%d count=%d 2>/dev/null" % (file_path, block_size, num_blocks)
            os.system(cmd)
        return file_name

    def delete_test_files(self):
        if os.path.exists(self.config.test_files):
                cmd = 'rm -rf %s' % self.config.test_files
                os.system(cmd)

    @staticmethod
    def compare(file1, file2):
        return filecmp.cmp(Config().test_files + '/' + file1, Config().test_files + '/' + file2)